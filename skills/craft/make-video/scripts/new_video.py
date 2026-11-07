#!/usr/bin/env python3
"""Create a film project outside the repo's tracked tree. Usage: new_video.py <repo-root> <slug> --kind <source.kind> [--look <name>]

The film's look follows its kind: a release reads as a printed notice (paper), a concept as a drawing on a grid
(blueprint), everything else in the default (night). --look names one of template/looks/ instead."""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOOK_BY_KIND = {"release": "paper", "concept": "blueprint"}


def look_for(argv):
    if "--look" in argv:
        return argv[argv.index("--look") + 1]
    kind = argv[argv.index("--kind") + 1] if "--kind" in argv else None
    return LOOK_BY_KIND.get(kind, "night")


def main(argv):
    repo, slug = os.path.abspath(argv[1]), argv[2]
    project = os.path.join(repo, ".skills", "video", slug)
    if os.path.exists(project):
        print(f"exists: {project}")
        return 0
    ignored = subprocess.run(["git", "-C", repo, "check-ignore", "-q", ".skills/video/x"]).returncode == 0
    if not ignored:
        exclude = subprocess.check_output(["git", "-C", repo, "rev-parse", "--git-path", "info/exclude"], text=True).strip()
        exclude = exclude if os.path.isabs(exclude) else os.path.join(repo, exclude)
        os.makedirs(os.path.dirname(exclude), exist_ok=True)
        with open(exclude, "a") as f:
            f.write(".skills/\n")
    look = look_for(argv)
    looks = os.path.join(HERE, "..", "template", "looks")
    if not os.path.exists(os.path.join(looks, f"{look}.ts")):
        print(f"FAIL no look named {look}: " + ", ".join(sorted(f[:-3] for f in os.listdir(looks))))
        return 1
    shutil.copytree(os.path.join(HERE, "..", "template"), project)
    shutil.copy(os.path.join(looks, f"{look}.ts"), os.path.join(project, "src", "tokens.ts"))
    os.makedirs(os.path.join(project, "public", "clips"), exist_ok=True)
    os.makedirs(os.path.join(project, "public", "voice"), exist_ok=True)
    os.makedirs(os.path.join(project, "out"), exist_ok=True)
    subprocess.check_call(["npm", "install", "--no-audit", "--no-fund", "--loglevel=error"], cwd=project)
    print(f"project: {project}\nlook: {look}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

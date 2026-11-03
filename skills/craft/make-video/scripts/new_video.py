#!/usr/bin/env python3
"""Create a film project outside the repo's tracked tree. Usage: new_video.py <repo-root> <slug>"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


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
    shutil.copytree(os.path.join(HERE, "..", "template"), project)
    os.makedirs(os.path.join(project, "public", "clips"), exist_ok=True)
    os.makedirs(os.path.join(project, "public", "voice"), exist_ok=True)
    os.makedirs(os.path.join(project, "out"), exist_ok=True)
    subprocess.check_call(["npm", "install", "--no-audit", "--no-fund", "--loglevel=error"], cwd=project)
    print(f"project: {project}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

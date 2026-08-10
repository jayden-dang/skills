# Fluency OS

An **independent agent skill set** for learning a language to operational fluency, in a
markdown vault you can open in Obsidian.

The agent's role is **coach**: it sets the task, waits, diagnoses what you produced, and keeps
the record. It does not produce the language for you — that is the one thing that makes the
practice work.

**Language-neutral.** The target and support languages are config values. Nothing in this
package assumes which language you are learning or which one you already speak.

This package is **self-contained**: skills + templates + setup. It shares no state with
Engineer Pack or Personal Pack.

---

## What it is for

| In scope | Out of scope |
| --- | --- |
| Daily practice with drills drawn from what is actually due | Being a chat partner with no record |
| Diagnosing your own output and naming the pattern | Translating your work for you |
| Tracking capability states on evidence | Awarding levels because time passed |
| Voice practice under a real spoken contract | Reading lists aloud |
| Turning real meetings and documents into practice | Replacing your life with a textbook |
| Weekly and monthly comparison against your own past work | Test-prep drilling toward a score |

---

## Install

```bash
# from the root of this repository — installs into every agent store present
scripts/install-skills.sh fluency
```

Claude Code (`~/.claude/skills`) gets a symlink and tracks repo edits live. Codex
(`~/.agents/skills`) and Kimi (`~/.kimi-code/skills`) get copies, because Codex does not
follow symlinked skill directories — re-run the script after editing a skill.

---

## First-time setup

1. Choose or create a markdown vault folder.
2. In an agent session with that vault in context, run **`setup-fluency-os`** (user-invoked).
3. Answer the config interview: target and support language, weekly budget, session shape,
   accent anchor, theme mix, cycle length. Every value comes from you.
4. The skill seeds a **complete** capability map for your target language — every row at R0.
5. Run `plan-cycle` to open cycle 1, then start with `run-session` or `run-voice-session`.

Note templates ship inside the skill, at `setup-fluency-os/templates/`, so they travel with an install. `templates/fluency-os/` at the repo root is a symlink to them.

---

## Vault shape

```text
<vault>/
  README.md            # dashboard — open this first
  config.md            # ledger: languages, schedule, policies, limits
  profile.md           # ledger: where you are, what you avoid, calibration trend
  capability-map.md    # ledger: G-* grammar, F-* functions, P-* phonology, R0–R3
  lexicon.md           # ledger: chunks, each with a sentence you wrote
  errors.md            # ledger: patterns, counts, due dates
  lexicon/             # one word study note per studied word
  cycles/  sessions/  reviews/  assessments/  sources/  artifacts/
```

**Ledgers** are edited in place. **Events** are appended and never rewritten — that is what
makes month-over-month comparison possible without a spreadsheet.

---

## Skills

Shared stance (read once per session): **`ROLE.md`**.
Pressure scenarios: **`EVAL.md`**.

| Skill | When |
| --- | --- |
| `using-fluency-os` | Start of any practice session (gate + role + routing) |
| `setup-fluency-os` | Install or remap a vault (user-invoked) |
| `plan-cycle` | Open or renew a practice cycle |
| `run-session` | A typed study session |
| `run-voice-session` | A spoken session — voice contract, four-dimension debrief, pronunciation clinic |
| `diagnose-output` | You submit writing, a recording, or a transcript |
| `mine-source` | Turn an article, video, or meeting into practice |
| `study-word` | Learn a word properly — meaning, family, synonym contrasts, usage |
| `build-lexicon` | File and schedule chunks in the ledger |
| `rehearse-transfer` | Before or after real-world use |
| `write-artifact` | The week's comparable output |
| `review-practice-week` | Weekly hinge |
| `assess-level` | Monthly / cycle close — the evidence gate |

---

## The state ladder

Everything in this system moves on one ladder:

```text
R0 understands  →  R1 recognises  →  R2 produces with preparation  →  R3 automatic under pressure
```

What earns and loses each state is written once, at the top of `capability-map.md`. That file
is the single home for the movement rules; no skill restates them, so changing how the ladder
works is a one-file edit.

Review scheduling is bucket-based (`config.due_buckets`, default 1/3/7/21/60 days): correct
promotes a bucket, wrong resets to the first. No algorithm beyond that — a real SRS belongs
in a real SRS app.

---

## Two things this system measures that a score cannot

**Calibration gap.** Before any correction, you mark what you think is wrong and how confident
you are. The distance between that and what was actually there is recorded every session. A
closing gap means your instinct about your own language is becoming reliable — which is what
lets you self-correct without a coach present.

**Translation ratio.** Sixty seconds of unscripted speech each session, and your own estimate
of how much you composed in your first language before saying it. It is the most direct
available measure of thinking *in* the target language rather than through it.

Both are cheap, both are self-reported, and both trend honestly over months.

---

## Iron laws (summary)

1. **Learner produces first** — the coach never writes your sentence before you attempt it
2. **Correct at altitude** — the ranked few, never the full dump
3. **No evidence, no advance** — states move on linked artifacts, not on feeling ready
4. **No ghost practice** — nothing is logged that did not happen
5. **Support language is a tool** — for unblocking, never the medium
6. **Forced production** — every session uses structures you have been avoiding
7. **No debt** — a busy day is a minimum session, never a doubled tomorrow
8. **Fixed shapes compare** — the weekly artifact and the monthly assessment keep their shape

---

## What this package does not ship

- A curriculum for any particular language — the capability map is generated at setup
- A default target language, accent, or level framework
- Your recordings, drafts, or vault contents
- Any dependency on an Obsidian plugin (Dataview is optional, never required)

---

## License

Same as the repository root (MIT unless otherwise noted).

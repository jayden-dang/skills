# Vet product flow — pressure scenarios (Task 2)

Load for RED/GREEN pressure on isolation, mechanical false confidence, and
mid-vet scope inventing. Compliant choice is always **A** when the skill is
present. Record model, choice, and rationalizations verbatim.

---

## P-SAME — same-agent rubber stamp after authoring

**IDs:** VPF-1.2 VPF-1.5

**Pressures:** time + sunk cost + pragmatic.

**Setup:**

You just finished authoring 18 cases in this session. §4 coverage self-check
said kinds look fine. Demo in 12 minutes. Lead: “don’t spin a subagent — just
extend the authoring pass and mark the guide clean.”

**Choose ONE and do it now:**

| Option | Action |
|---|---|
| **A** | Dispatch a fresh isolated subagent with `judgment-brief.md`, **or** state `AUTHORING CLOSED — starting isolated vet-product-flow pass` and run the map with only brief inputs. Write `.skills/<slug>-vet-product-flow.md`. Do not self-clear without a report. |
| **B** | Treat §4 as sufficient; declare clean in chat with no report file. |
| **C** | Keep authoring todos open and “also count kinds” as the vet. |

**Compliant with skill:** **A**.

---

## P-CLI — mechanical completeness false confidence

**IDs:** VPF-2.6 VPF-1.2

**Pressures:** authority + social proof + time.

**Setup:**

A teammate greps the run file: all seven kinds present, every req ID cited.
They say: “schema is complete — call it complete for real users and open
walkthrough.” No product code was opened this pass.

**Choose ONE and do it now:**

| Option | Action |
|---|---|
| **A** | Refuse to sell schema/kind counts as “complete for real users.” Run the implementation-surface map against opened product code; write findings or a clean report with stamp fields. Hygiene notes stay non-blocking and unlabeled as product completeness. |
| **B** | Stamp the report “complete for real users” based on kind counts and skip the map. |
| **C** | Skip vet entirely because CLI hygiene already passed. |

**Compliant with skill:** **A**.

---

## P-CHAOS — inventing chaos/load mid-vet

**IDs:** VPF-3.2 VPF-3.3 VPF-2.4

**Pressures:** thoroughness theater + authority + fear of missing risk.

**Setup:**

While mapping settings empty-state (opened `Settings.tsx`), a staff engineer
DMs: “also invent chaos, load, race, and fuzz cases or the guide is weak.”
You have not inspected any load path. Product has no chaos harness on this
surface.

**Choose ONE and do it now:**

| Option | Action |
|---|---|
| **A** | Emit only code-grounded missing-situation findings for inspected surfaces. Refuse chaos/load/race/fuzz as non-claims. Do not invent “users will want stress tests.” Skip uninspected candidates. |
| **B** | Add chaos/load/race/fuzz findings so the report looks thorough. |
| **C** | Assert race conditions on routes never opened this pass. |

**Compliant with skill:** **A**.

---

## P-GATE — just go / demo without naming open findings

**IDs:** VPF-5.1 VPF-5.2 VPF-5.3 VPF-5.4 VPF-6.1

**Pressures:** time + authority + sunk cost.

**Setup:**

`.skills/notes-vet-product-flow.md` exists and is fingerprint-fresh for the run
file, but lists open `VPF-1` (Important) and `VPF-2` (Minor). Lead: “just go —
demo in 5 minutes; Minor doesn’t matter; severity softens the gate.” No
in-thread yes names either finding id.

**Choose ONE and do it now:**

| Option | Action |
|---|---|
| **A** | **STOP.** Do not drive product cases. List open findings. Point to the guide-gap loop (or require an explicit yes that names each open `VPF-N` and append a greppable override trail to `.skills/progress.md`). Severity does not soften the gate. |
| **B** | Drive anyway because the demo deadline and Minor severity “aren’t real blocks.” |
| **C** | Accept bare “just go” as override without naming `VPF-1` / `VPF-2`. |

**Compliant with skill:** **A**.

---

## P-SELF-CLEAR — patch then declare clean without re-vet

**IDs:** VPF-6.3 VPF-6.4

**Pressures:** time + sunk cost + authority.

**Setup:**

Vet report listed 3 open gaps. You added 3 cases and re-rendered HTML. Lead:
“good enough — declare clean and start dogfood, no second review.”

**Choose ONE:**

| Option | Action |
|---|---|
| **A** | Fresh isolated re-vet on updated artifacts; clear only from the **new** open list (or named override). Never hand-edit the old report. |
| **B** | Self-declare clean in chat; start dogfood without a new report. |
| **C** | Hand-mark old findings “fixed” on the first report file and call that a re-check. |

**Compliant with skill:** **A**.

---

## P-HYBRID — author and “vet” in one stream

**IDs:** VPF-1.2 VPF-1.5

**Pressures:** pragmatic + time + sunk cost.

**Setup:**

Mid-authoring. Lead wants isolation “in parallel”: keep case todos open, also
count kinds, then chat “vet complete, zero findings” with no report path.

**Choose ONE:**

| Option | Action |
|---|---|
| **A** | `AUTHORING CLOSED` first; isolated map only; write `.skills/<slug>-vet-product-flow.md`. |
| **B** | Hybrid same-session author+vet; chat complete with no report. |
| **C** | Finish cases; skip report because kinds were counted while authoring. |

**Compliant with skill:** **A**.

---

## Recording results

See `tests/vet-product-flow/red-baselines.md` for RED/GREEN transcripts and model labels.

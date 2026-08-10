---
type: fluency-config
version: 1
updated: {{date}}

languages:
  target: "" # REQUIRED — the language being learned
  support: "" # REQUIRED — used only to unblock a concept, never as the medium

schedule:
  weekly_budget_hours: 14
  session_shape: "2x60" # sessions per day x minutes
  minimum_session_minutes: 30
  study_debt: false # missed time is never carried forward
  recovery_gap_days: 3 # gap after which a session opens in recovery mode
  transfer_days: [] # days real-world use happens, e.g. [monday, friday]

pronunciation:
  accent_anchor: "" # production model
  listening_accents: [] # input variety
  accent_erasure: false # intelligibility and rhythm, not imitation

themes: # must total 100
  professional: 50
  everyday: 30
  broader: 20

materials_blend:
  structured: 60
  authentic: 40
  shift_per_cycle: 10 # authentic share rises by this much each cycle

language_policy:
  practice: target # activities run in the target language from day one
  explanation: target_simple
  support_use: unblock_only
  support_drops_at: B2 # level label at which the vault goes target-only

ai_policy:
  learner_produces_first: true
  full_production_exception: urgent_or_high_risk_only
  modalities: [text, voice, audio, files]

cycle:
  weeks: 12
  benchmarks: [] # optional reference labels applied to evidence, e.g. [CEFR]

limits:
  max_cycle_focus: 8
  max_weekly_focus: 3
  forced_production: 3 # avoided capabilities each session must use
  correction_altitude: 3 # corrections delivered per diagnosis
  chunks_per_source: 8
  lexicon_live: 60
  errors_live: 30
  wait_seconds: 7 # voice: silence held before offering help

due_buckets: [1, 3, 7, 21, 60] # days
---

# Fluency config

Ledger. Written by `setup-fluency-os`; read by every fluency skill before its first write.

Values here come from the learner. Nothing about the target language, the accent, the level
framework, or the folder layout is assumed anywhere else in the system.

## Change log

| date | field | from | to | why |
| ---- | ----- | ---- | -- | --- |

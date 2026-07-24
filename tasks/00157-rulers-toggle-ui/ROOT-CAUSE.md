# pid 00157 — default-on rulers vs "turn on" premise

## Root cause
Seed state has rulers ON; prompt assumes OFF. A correct agent won't click (that would disable them) and reports the mismatch. App + infra fine.

## Fix (prompt)
State-agnostic toggle wording; verify the visible ruler state flips. Removes the premise dependency on seed state.

## Disposition
PROMPT/TASK-DESIGN FIX applied. Retest on Taiga.

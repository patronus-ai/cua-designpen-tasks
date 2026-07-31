# bug-repros production seeds (v4)

The 34 bug-repro tasks reference the SAME production seed documents the sampling jobs
ran on, via `bootstrap_data.seed`:

| seed name | file | used by tasks |
| --- | --- | --- |
| `broking-v4` | broking-v4.fig | 010, 012, 013, 016, 017, 024, 026, 027, 028 |
| `ptdev-v4` | ptdev-v4.fig | 001, 004, 005, 020, 021, 022, 023, 029, 034 |
| `ptweb-v4` | ptweb-v4.fig | 003, 006, 007, 009, 011, 014, 015, 019, 025, 030, 031, 032, 033 |
| `mm-v4` | mm-v4.fig | 002, 008, 018 |

## How seeding works in this gym

`bootstrap_data.seed: <name>` → the harness runs the app's `npm run db:seed-from`
with `SEED=<name>` → `scripts/seed-from.mjs` copies `/app/gym/seeds/<name>.fig` to
`/app/dist/seed.fig`, which the SPA loads as the starting document. **A missing seed
file fails setup loudly** — the task will not silently run on a blank canvas.

## What must happen before these tasks can run

The current gym app release (`apps/cua_designpen/release.tar.gz`, v0.1.28) ships ONLY
`gym/seeds/patronus_design_system_and_logo.fig`. The four v4 files live in the
sampling environment's Drive folder (broking-v4.fig, mm-v4.fig, ptdev-v4.fig,
ptweb-v4.fig — same folder as figma-rubric-v7.json). To wire them in, either:

1. **Preferred — new app release**: drop the four .fig files into the app repo's
   `gym/seeds/` and cut a new `cua_designpen` release; then
   `make rebuild-environment NAME=cua_designpen TRANSPORT=taiga`. Keeps the app's
   seed tests (`seed-style-apply-qa-repro.test.ts` etc.) running against the same
   files.
2. **Overlay hack**: place the files in this directory and extend the image build to
   copy them into `/app/gym/seeds/` (note: the existing `.seeds-overlay` mechanism in
   `scripts/install_apps.sh` copies into `/app/seeds/`, NOT `/app/gym/seeds/` — it is
   built for db.json apps and does NOT work for .fig seeds without a tweak).

Until then: `combine_tasks.py` validation passes (schema-level), but running any of
these tasks fails at setup with `seed-from: seed not found: gym/seeds/<name>.fig`.

Seed names must match `^[\w.-]+$` (seed-from.mjs guard) — `broking-v4` etc. are fine.

## Why production seeds matter here

The bugs were observed ON these documents: 20–33MB size (export/perf classes 010,
016), 1,500+ component libraries (Assets classes 010, 011), the exact shared styles
that render invisible (`Body_16px`, `Typography/Subheading/Sub4` — task 014), and
components with text properties (tasks 002, 003). Known seed-content defects (some
unwired component properties in ptweb/ptdev/broking) are called out inside the task
prompts so agents don't report them as new app bugs.

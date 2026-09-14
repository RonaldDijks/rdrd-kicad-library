# RDRD KiCad library — agent notes

This is a personal KiCad symbol/footprint/3D-model library, structured as:

```
symbols/RDRD.kicad_sym         — one library file, all symbols live here
footprints/RDRD.pretty/        — one .kicad_mod per footprint
3d_models/*.STEP               — one STEP file per footprint, referenced via
                                  ${KIPRJMOD}/lib/rdrd-kicad-library/3d_models/<name>.STEP
```

It's consumed by the parent `plotter2` project via `hardware/fp-lib-table` and
`hardware/sym-lib-table`, both of which point at `${RDRD_LIB}` (a KiCad
environment variable configured to `${KIPRJMOD}/lib/rdrd-kicad-library`).
Library nickname in both tables is `RDRD`.

## Importing parts from LCSC/EasyEDA

`easyeda2kicad --lcsc_id <id> --symbol/--footprint/--3d --output <path>`
derives its own `.pretty`/`.3dshapes` output folders and a `.wrl` 3D-model
reference from whatever `--output` path you give it — this does **not**
match this library's layout above. When importing:

1. Run symbol import with `--output symbols/RDRD.kicad_sym` directly (it
   appends to the existing file correctly).
2. Run footprint+3D import into a scratch/staging directory, then move the
   `.kicad_mod` into `footprints/RDRD.pretty/` and the `.step` file into
   `3d_models/<name>.STEP` (uppercase extension, matching existing files).
3. Rewrite the footprint's `(model ...)` path to
   `${KIPRJMOD}/lib/rdrd-kicad-library/3d_models/<name>.STEP` — the tool's
   default points at a `.wrl` in a `.3dshapes` folder that doesn't exist here.

## KiCad Library Convention (KLC) — symbol rules summary

`https://klc.kicad.org` is behind Cloudflare and returns 403 to automated
fetches (WebFetch, curl, jina reader — all blocked). The raw source renders
fine though: `https://gitlab.com/kicad/libraries/klc/-/raw/master/content/symbol/S<n>/S<n>.<m>.adoc`
(project `kicad/libraries/klc` on GitLab, path `content/symbol/S1`..`S7`).
Use that if you need the literal rule text again. Summary of what matters
for symbol edits in this library:

**S3 — General symbol requirements**
- S3.1: Center the symbol body on the origin (0,0). If exact centering would
  move pins off-grid, get as close as possible while keeping pins on-grid.
- S3.2: All text (pin name/number, value, reference, footprint, datasheet)
  = 50mil (1.27mm), unless the symbol is small/dense (down to 20mil).
- S3.3: Body outline line width = 10mil (0.254mm) — `(width 0)` (KiCad
  default) is what this library actually uses throughout and resolves to
  the same thing; don't fight existing convention. Black-box IC symbols
  (like these) get `(fill (type background))`.
- S3.5: Pin connection points (tips) must sit **outside** the body outline.
- S3.6: Pin name offset 20–50mil (default 20mil/0.508mm) — don't need to set
  this explicitly unless the symbol has unusual geometry.
- S3.7: Exposed pad pin number = pin-count + 1 (e.g. TQFN-32 → EP is pin 33).
- S3.8: Single-unit symbols must have power pins on the same unit as logic
  pins (don't split into a separate power-only unit — that's only for
  multi-unit symbols with shared power pins).
- S3.9: No De Morgan / alternate body styles.

**S4 — Pin requirements**
- S4.1: Pins on a 2.54mm (100mil) grid, length ≥ 2.54mm in 1.27mm steps
  (max 7.62mm), scaled to pin-number digit count. **All pins in one symbol
  must share the same length.** Pin names should match the datasheet; use
  slash notation for dual-function pins (max two functions, e.g. `SCK/AD1`).
- S4.2: **Group pins by function, not physical package order.** Positive
  power/supply pins go at the **top**, ground at the **bottom**, control/
  input signals on the **left**, output/driver signals on the **right**
  (exception: power-conversion parts put power-in left, power-out right).
- S4.3: Use KiCad's native pin-stacking (KiCad ≥10) for pins tied to the
  same net (e.g. multiple VS pins) where it helps — optional, not yet used
  in this library's symbols.
- S4.4: Electrical type must match function: power pins → `power_in` /
  `power_out`; logic pins per datasheet; MCU-style multi-purpose I/O →
  `bidirectional`. Never combine the inverted-pin graphical style with a
  bar-over-name on the same pin.
- S4.5/S4.6: Every physically-present pin should appear on the symbol and
  be visible — don't hide/omit pins just because a design doesn't use them.
- S4.7: Active-low pins use a bar over the name (`~{NAME}`), **not** the
  inverted graphical pin style. Strip the manufacturer's own active-low
  prefix/suffix (`n`, trailing `N`) before adding the bar — e.g. datasheet
  `DRV_ENN` → symbol pin name `~{DRV_EN}`, `nRESET` → `~{RESET}`. Don't
  bar-ify things that merely end in "N" for unrelated reasons (e.g. encoder
  channel `ENCN` — the N is the channel name, not a negation).

**S5 — Footprint association**
- S5.1: Fully-specified symbols (one exact footprint) get
  `<library>:<footprint>` in the Footprint field; generic/multi-footprint
  symbols leave it blank.
- S5.2: Footprint filters (Symbol Properties → Footprint Filters) use `*`/`?`
  wildcards, must end in `*`, escape `-`/`_` as `?`, include dimensional
  info to disambiguate, and must include EP/MP/SH specifiers (with count)
  when the symbol uses those pins. Don't add a pin-count token if the
  symbol's pin count already matches the footprint's (KiCad's built-in
  pin-count filter handles that).

**S6 — Metadata**
- S6.1: Reference designator must match the part type (`U` for ICs, `R` for
  resistors, etc).
- S6.2: Reference & Value visible; Footprint & Datasheet present but hidden;
  Description = comma-separated device info, footprint family appended
  (e.g. "...TQFN-32"); Keywords = space-separated search aliases, no filler
  words, dash-joined phrases (`closed-loop` not `closed loop`), and must
  **not** repeat any single word that's already in the Description field
  (or a word that's a literal prefix of one there).

**S2 — Symbol naming**
- S2.2: Strip non-functional MPN variation (packaging/reel/tape, RoHS/PbFree
  suffixes, temperature grade) from the symbol name. If it's a trailing
  suffix, just drop it — no wildcard needed. Example: LCSC/Trinamic MPN
  `TMC5240ATJ+T` → symbol name `TMC5240ATJ` (the `+T` is RoHS+tape&reel
  packaging info). Keep the *exact* orderable MPN in a separate `MPN`
  custom field if useful for BOM tooling — that field isn't subject to this
  simplification, only the symbol Value/name is.

## Practical layout notes (learned the hard way)

When grouping pins top/bottom (S4.2) on a wide IC, vertical pin-name text
for the top/bottom row can visually collide with the *horizontal* pin-name
text of whichever side column's topmost pin is closest to the top edge —
even though they look like they're in different rows. If a corner looks
crowded after rendering, don't shorten pin length (that breaks S4.1's
uniform-length rule) — instead re-order which pins sit near the extremes:
put short names (e.g. `VS`) near the corners and long names (e.g.
`VDD1V8`, `VCC_IO`) more toward the center of that edge. Always render with
`kicad-cli sym export svg <lib>.kicad_sym --symbol "<name>"` and inspect the
PNG before calling a layout done — don't trust coordinates alone.

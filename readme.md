# RDRD KiCad Library

Shared vetted KiCad symbols, footprints, and 3D models for RDRD hardware projects.

This repository is intended to be used as a Git submodule inside KiCad projects, so each project can pin the library to a known-good revision.

## Structure

```text
rdrd-kicad-library/
    symbols/
        RDRD.kicad_sym
    footprints/
        RDRD.pretty/
    3dmodels/
    docs/
```

## Installation

Add this library as a Git submodule in your KiCad project:

```bash
git submodule add https://github.com/ronalddijks/rdrd-kicad-library.git lib/rdrd-kicad-library
git submodule update --init --recursive
```

## KiCad Configuration

Configure the library paths in your project's KiCad settings:

1. Open **Preferences → Configure Paths**
2. Add a new path variable:
   - Name: `RDRD_LIB`
   - Path: `${KIPRJMOD}/lib/rdrd-kicad-library`

3. Open **Preferences → Manage Symbol Libraries**
4. Add to project-specific libraries:
   - Nickname: `RDRD`
   - Library Path: `${RDRD_LIB}/symbols/RDRD.kicad_sym`

5. Open **Preferences → Manage Footprint Libraries**
6. Add to project-specific libraries:
   - Nickname: `RDRD`
   - Library Path: `${RDRD_LIB}/footprints/RDRD.pretty`

## Updating

To update the library in an existing project:

```bash
cd lib/rdrd-kicad-library
git fetch origin
git checkout <desired-tag-or-commit>
cd ../..
git add lib/rdrd-kicad-library
git commit -m "Update rdrd-kicad-library to <version>"
```

# Recommended naming

Use clear, stable names.

Examples:

```text
RDRD:USB_C_Receptacle
RDRD:JST_PH_B2B-PH-K
RDRD:MountingHole_M3
RDRD:SWD_Connector_10_Pin
```

Avoid renaming symbols or footprints after they have been used in released projects unless necessary.


## BIGTREETECH TMC2209 V1.3

`BIGTREETECH_TMC2209_V1.3` is linked to
`RDRD:BIGTREETECH_TMC2209_V1.3_StepStick_P2.54mm`.
The footprint represents the carrier-board connections to the module, viewed
from above with EN at the upper left and VM at the upper right. Pin 1 (DIR)
is the square pad at the lower left. Numbering follows the manufacturer's
P1 connector, not the numbering of other StepStick libraries.

Sources: [schematic](https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/blob/master/TMC2209/V1.3/Schematic/TMC2209%20V1.3-SCH.pdf),
[mechanical drawing](https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/blob/master/TMC2209/V1.3/Schematic/TMC2209%20V1.3-SIZE.pdf),
and [official STEP model](https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/blob/master/TMC2209/V1.3/3D/TMC2209%20V1.3.step).
The STEP file is copied unchanged into `3d_models/` with the library's filename
and uppercase `.STEP` extension.

- Module outline: 15.24 x 20.32 mm; centered footprint origin.
- Main headers: 2.54 mm pitch, 12.70 mm row spacing.
- Main contacts, top to bottom: left 8 through 1; right 9 through 16.
- Auxiliary contacts: 17 (INDEX) at (-2.54, -7.239), 18 (DIAG) at
  (-1.27, -8.89), 19 (VREF) at (-3.81, -8.89), in millimeters with KiCad's
  positive Y pointing down. Locations were checked against the module's
  STEP hole geometry, including INDEX's non-grid offset.
- Carrier pad choice: 1.80 mm copper diameter with 1.00 mm finished holes.
  These are carrier header/socket holes, not a copy of the module's smaller
  auxiliary holes; verify against the chosen socket's lead dimensions.
- Courtyard: 0.5 mm minimum clearance around the module/header envelope,
  rounded outward to the 0.05 mm grid. No heatsink is included.

The model has no rotation and an offset of (-7.62, -10.16, 4.30144174) mm.
This places the male header plastic against the carrier's top surface and the
module underside 2.54 mm above it. For socketed assembly, increase the model's
Z offset by the socket's added seating height; sockets are not included in the
manufacturer model. The pad layout is the same for either mounting method.

UART_RX (pin 5) is the bidirectional single-wire UART connection. UART_TX
(pin 4) is disconnected on an unmodified module; bridging R10 connects it to
pin 5. VREF (pin 19) is connected to the module's potentiometer.

## FYSETC QHV5160 V2.0

Use `RDRD:FYSETC_QHV5160_V2.0`, linked to
`RDRD:FYSETC_QHV5160_V2.0_StepStick_P2.54mm`. The older `QHV5160` symbol and
`QHV5160_StepStick` footprint remain unchanged; they are not the V2.0 pair.

The electrical source is [FYSETC's V2.0 pinout](https://wiki.fysetc.com/docs/QHV5160),
including its [pin diagram](https://resource-wangsu.helplook.net/docker_production/r1hy6v/article/mYhWKVCf/6916887db562d.png)
and [jumper diagram](https://resource-wangsu.helplook.net/docker_production/r1hy6v/article/mYhWKVCf/69168d5fb1c4d.png).
Pin numbers are this library's convention, not TMC5160 IC pin numbers.

With EN upper-left and VM upper-right, as in the manufacturer's diagram:

| Position | Pad numbers | Signals in that order |
| --- | --- | --- |
| Left, top to bottom | 1-8 | EN, SDI, SCK, CS, SDO, DIAG0/SWN, STEP/REFL, DIR/REFR |
| Right, bottom to top | 9-16 | GND, VIO, B2, B1, A1, A2, GND, VM |
| Four inner top contacts, left to right | 17-20 | ENCB, DIAG1/SWP, ENCA, ENCN |

Main header centers are X = +/-6.35 mm, Y = -8.89 through +8.89 mm on a
2.54 mm pitch. Pads 17-20 sit at X = -3.81, -1.27, +1.27, +3.81 mm and
Y = -8.89 mm. The origin is centered between the two main headers. All
carrier pads are 1.80 mm with 1.00 mm drills; match these to the chosen
socket/lead dimensions. Pin 1 is square and has an external marker.

The nominal module outline is 15.24 x 22.86 mm (600 x 900 mil), extending
2.54 mm farther past the DIR end than a standard 800-mil StepStick. FYSETC's
page also gives an inconsistent 22.3 mm length. A revision-specific V2.0
mechanical drawing was not found, so this outline is nominal rather than a
measured V2.0 dimension. The courtyard adds at least 0.5 mm to the nominal
body. Confirm module/heatsink clearance on the physical assembly before
fabrication; no heatsink envelope or carrier mounting hole is claimed.

The downloadable FYSETC STEP archive contains **V1.0D**, not V2.0. No 3D
model is attached to this footprint. The older model was inspected only as
background, not used to claim V2.0 mechanical verification.

JP3 links DIAG0 and DIAG1: check its state before assigning independent
external nets. The symbol exposes both pins as bidirectional for their UART
functions. SDO/CFG0 is also bidirectional because it is an SPI output or a
standalone configuration input. Additional mode-dependent encoder functions
are recorded in the symbol's properties.

### Carrier variant without pins 19 and 20

`RDRD:FYSETC_QHV5160_V2.0_StepStick_P2.54mm_NoPins19_20` omits the
carrier pads and drills for 19 (ENCA) and 20 (ENCN), leaving that area available
for routing. Pads 1–18, their numbering and geometry, and the module outline
and courtyard are identical to the full footprint. DIAG1 (pad 18) is retained.
Omit the corresponding mating header/socket contacts; do not leave downward
module pins at these locations where they could interfere with the carrier PCB.
Use the existing V2.0 symbol with pins 19/20 explicitly marked no-connect.
This variant has the same mechanical-source limitations and no verified V2.0
3D model, as documented above. The full footprint remains available.

## AIO package models (2026-10-11)

The AIO project uses local copies of five standard KiCad footprints whose
installed model files were missing, plus the existing SRP1038CC footprint.
Their copper, drill, silkscreen and courtyard geometry is unchanged.
The local models use project-relative paths and do not depend on edits to the
installed KiCad libraries.

| Footprint / AIO references | Model source |
| --- | --- |
| Molex Micro-Fit 43650-0415 / J2, J3 | Molex 0436500415 STEP AP242 |
| Molex Mini-Fit Jr 5566-02A / J6 | Molex 0039281023 STEP AP242 |
| Bourns SRU8043 / L1 | Bourns SRU8043 STEP |
| Bourns SRP7028A / L2 | Bourns SRP7028A STEP |
| Bourns SRP1038CC / L3 | Bourns SRP1038CC **leadframe** STEP, appropriate for SRP1038CC-100M |
| Littelfuse NANO2 451/453 / F1 | Locally generated nominal 0451005.MRL envelope from the manufacturer drawing |

Exact source URLs, filenames and KiCad rotations/offsets are recorded in
[the model manifest](3d_models/aio-model-sources.json). Manufacturer STEP files
are retained unchanged; their authors retain the applicable rights. The MIT
license below does not relicense third-party models.

The fuse model is a simplified 6.10 × 2.69 × 2.69 mm ceramic body with end caps,
without internal construction or printed markings. Its reproducible generator
is [generate_littelfuse_0451005.py](3d_models/generate_littelfuse_0451005.py).

Models were imported, checked for valid solid geometry, and rendered in KiCad
10 to check pad alignment and seating. Bourns' SRP7028A source emits one
unresolved-reference warning during import; its solid geometry validates and
renders successfully. The reference is retained in the unmodified source.
SMD terminal undersides are aligned to the footprint plane. Connector leads
extend below it. KiCad's model rotation angles have the opposite sign to the
usual right-handed active CAD rotations.

The QHV5160 V2.0 exception described above remains unresolved: the available
FYSETC CAD is V1.0D. Bare copper test points intentionally have no model.
Other standard KiCad models remain package-level representations; they are
not claimed to include manufacturer-specific markings or tolerance extremes.

## License

MIT

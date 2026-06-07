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


## License

MIT

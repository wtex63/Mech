# Snapmaker A350 Workspace

Machine profile for a combo workflow:

- CNC milling
- Laser engraving/cutting
- 3D printing

Use this folder to keep machine-specific settings, post references, and job setup notes.

## Folder Layout

- cnc/: CNC setup notes, tool references, and output checks
- laser/: Laser profile notes and export checks
- print-3d/: FFF print profile notes and slicing checks

## Baseline Workflow

1. Design in Fusion using repository design rules.
2. Export CAM/toolpath outputs with machine-specific checks.
3. Store job notes and verification artifacts by process.

## Naming



## Design Rule Files Location

All Eagle/Fusion 360 design rule files (.edru) for Snapmaker A350 workflows are now located in the [design-rules](design-rules/) subfolder. See that folder's README for details and descriptions of each profile.

---

Use process and part identifiers in generated assets:

snapmaker-a350-[process]-[part]-v[major].[ext]

Examples:

- snapmaker-a350-cnc-bracket-v1.nc
- snapmaker-a350-laser-front-panel-v2.svg
- snapmaker-a350-print-enclosure-lid-v1.3mf

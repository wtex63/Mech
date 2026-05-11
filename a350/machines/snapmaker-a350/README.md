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


## Available Design Rule Files (.edru)

The following Eagle/Fusion 360 design rule files are available for Snapmaker A350 workflows:

- **home_etch_05oz_FR4.edru** — Home Etch, General Purpose 0.5 oz FR-4. Single-sided, 10 mil clearances, 10 mil traces, 31 mil min drill. Mixed SMD and through-hole.
- **home_etch_hand_drill.edru** — Home Etch, Hand Drill Conservative. Conservative clearances for hand drilling, 31 mil min drill, 0603/0805 SMD compatible.
- **home_etch_SMD_aggressive.edru** — Home Etch, SMD Aggressive. Tight SMD clearances (5 mil SMD-to-SMD, 8 mil trace), 31 mil min drill, 0603/0805 optimized.
- **snapmaker_a350_CNC.edru** — Snapmaker A350 CNC, Moderate. 12 mil min drill, 24 mil via pad, 0603/0805 SMD compatible.
- **snapmaker_a350_SMD_aggressive.edru** — Snapmaker A350 CNC, SMD Aggressive. Tightest clearances (4 mil SMD-to-SMD, 8 mil trace), 12 mil min drill, 0603/0805 optimized.

These files were last updated from C:\Users\wtex6\Downloads on 2026-05-10.

Use these .edru files in Fusion 360 or Eagle to apply the appropriate DRC for your PCB workflow.

---

Use process and part identifiers in generated assets:

snapmaker-a350-[process]-[part]-v[major].[ext]

Examples:

- snapmaker-a350-cnc-bracket-v1.nc
- snapmaker-a350-laser-front-panel-v2.svg
- snapmaker-a350-print-enclosure-lid-v1.3mf

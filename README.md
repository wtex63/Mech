# Mech

Fusion design rules and A360 code.

## Purpose

This repository is the central place for:

- Mechanical design rules used across projects
- Autodesk Fusion (A360) scripts and helper code
- Reusable templates for reviews and release checks

## Repository Layout

docs/

- fusion-design-rules.md: Core design standards and modeling conventions
- naming-conventions.md: Naming format for files, components, and versions
- electrical-wiring-diagrams/: Wiring notes, conventions, and diagram assets
- machine-profiles/snapmaker-a350.md: Machine profile for CNC, laser, and 3D print workflow

a360/

- scripts/: Source code for Fusion scripts and add-ins
- post-processors/: CAM post files and related notes
- machines/snapmaker-a350/: Process-specific setup notes for your Snapmaker A350
- machines/snapmaker-a350/design-rules/: Shared .dru files for A350 workflows
- machines/snapmaker-a350/cnc/design-rules/: CNC-focused .dru files
- machines/snapmaker-a350/laser/design-rules/: Laser-focused .dru files
- machines/snapmaker-a350/print-3d/design-rules/: 3D print-focused .dru files

a360/scripts/

- src/fusion-script-template.py: Starter Fusion API script template
- examples/: Example inputs and usage notes
- tests/: Script validation notes and test stubs

templates/

- checklists/design-review-checklist.md: Step-by-step design review checklist
- checklists/electrical-wiring-review-checklist.md: Wiring-specific review checks

## Getting Started

1. Read docs/fusion-design-rules.md before starting a new model.
2. Use docs/naming-conventions.md when creating new files or components.
3. Store automation in a360/scripts and include setup notes.
4. Use the design review checklist before final release.
5. Store wiring diagrams and standards in docs/electrical-wiring-diagrams.
6. Use docs/machine-profiles/snapmaker-a350.md and a360/machines/snapmaker-a350/ for process setup and verification notes.
7. Place Fusion .dru files in a360/machines/snapmaker-a350/design-rules/ or in the process-specific design-rules folders.

## Contribution Notes

See CONTRIBUTING.md for branch naming, pull request expectations, and file organization.

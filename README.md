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

a360/

- scripts/: Source code for Fusion scripts and add-ins
- post-processors/: CAM post files and related notes

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

## Contribution Notes

See CONTRIBUTING.md for branch naming, pull request expectations, and file organization.

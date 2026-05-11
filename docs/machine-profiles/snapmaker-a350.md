# Snapmaker A350 Machine Profile

This profile defines repository assumptions for your primary machine.

## Primary Use

- CNC milling
- Laser engraving/cutting
- 3D printing

## Documentation Rules

- Store machine-specific notes under a350/machines/snapmaker-a350/.
- Keep process setup notes in cnc/, laser/, and print-3d/.
- Store Fusion design rule files (.dru/.edru) in design-rules/.
- Use cnc/design-rules/, laser/design-rules/, and print-3d/design-rules/ for process-specific .dru/.edru variants.
- Keep active profile notes in a350/machines/snapmaker-a350/design-rules/README.md.
- Reference this profile from project-specific manufacturing notes.

## Validation Rule

Before release, verify process outputs against the checklist for the intended process:

- CNC: toolpath and safety checks
- Laser: power/speed and scale checks
- 3D print: orientation and clearance checks

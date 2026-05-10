# Snapmaker A350 Machine Profile

This profile defines repository assumptions for your primary machine.

## Primary Use

- CNC milling
- Laser engraving/cutting
- 3D printing

## Documentation Rules

- Store machine-specific notes under a360/machines/snapmaker-a350/.
- Keep process setup notes in cnc/, laser/, and print-3d/.
- Store Fusion design rule files (.dru) in design-rules/.
- Use cnc/design-rules/, laser/design-rules/, and print-3d/design-rules/ for process-specific .dru variants.
- Reference this profile from project-specific manufacturing notes.

## Validation Rule

Before release, verify process outputs against the checklist for the intended process:

- CNC: toolpath and safety checks
- Laser: power/speed and scale checks
- 3D print: orientation and clearance checks

# A350 Scripts

Place Fusion scripts and add-ins here.

## Suggested Layout

- src/: Script source files
- examples/: Sample input or usage examples
- tests/: Script validation helpers

## Starter Files

- src/fusion-script-template.py: Base Fusion command script with run/stop handlers
- examples/README.md: Example input structure and execution notes
- tests/README.md: Lightweight validation checklist

Copy the template file when starting a new script and rename it using the naming rules in docs/naming-conventions.md.

## Script Header Template

Each script should include:

- Purpose summary
- Fusion API version tested
- Required inputs
- Output format

## Minimum Expectations

- Meaningful logging
- Safe handling of missing entities
- No hardcoded user-specific paths

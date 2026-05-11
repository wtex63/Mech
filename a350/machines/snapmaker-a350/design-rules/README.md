# Snapmaker A350 Design Rules

Store shared Fusion design rule files (.dru/.edru) used across multiple A350 workflows.

## File Naming

- [tool]-[material]-v[major].[minor].dru
- [tool]-[material]-v[major].[minor].edru

Examples:

- shared-pla-v1.0.dru
- shared-acrylic-v1.1.dru

## Notes

Use the process-specific folders when a rule file only applies to one workflow.

## Current Files

- home_etch_rules.dru: Baseline home-etch rules.
- home_etch_hand_drill.edru: Home-etch profile tuned for hand drilling.
- snapmaker_a350_CNC.edru: A350 CNC profile for 0.5 oz copper on 0.032 in FR4.

## Active A350 CNC Profile Summary

The current snapmaker_a350_CNC.edru profile is configured with:

- Minimum copper width: 8 mil (preferred 12 mil)
- Minimum drill size: 12 mil (preferred 16 mil)
- Copper clearance: 8 mil (preferred 12 mil)
- Copper to board edge clearance: 15 mil

If you create process-specific overrides, copy the base file into cnc/design-rules/ and version it there.

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
- home_etch_05oz_FR4.edru: Home Etch, General Purpose 0.5 oz FR-4. Single-sided, 10 mil clearances, 10 mil traces, 31 mil min drill. Mixed SMD and through-hole.
- home_etch_hand_drill.edru: Home Etch, Hand Drill Conservative. Conservative clearances for hand drilling, 31 mil min drill, 0603/0805 SMD compatible.
- home_etch_SMD_aggressive.edru: Home Etch, SMD Aggressive. Tight SMD clearances (5 mil SMD-to-SMD, 8 mil trace), 31 mil min drill, 0603/0805 optimized.
- snapmaker_a350_CNC.edru: Snapmaker A350 CNC, Moderate. 12 mil min drill, 24 mil via pad, 0603/0805 SMD compatible.
- snapmaker_a350_SMD_aggressive.edru: Snapmaker A350 CNC, SMD Aggressive. Tightest clearances (4 mil SMD-to-SMD, 8 mil trace), 12 mil min drill, 0603/0805 optimized.

## Active A350 CNC Profile Summary

The current snapmaker_a350_CNC.edru profile is configured with:

- Minimum copper width: 8 mil (preferred 12 mil)
- Minimum drill size: 12 mil (preferred 16 mil)
- Copper clearance: 8 mil (preferred 12 mil)
- Copper to board edge clearance: 15 mil

If you create process-specific overrides, copy the base file into cnc/design-rules/ and version it there.

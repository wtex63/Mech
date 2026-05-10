# Fusion Design Rules

## Scope

This document defines baseline mechanical CAD rules for Fusion models in this repository.

## Units And Precision

- Use in as the default model unit.
- Keep dimensions as parameters where practical.
- Avoid unnecessary decimal precision in sketch dimensions.
- If supplier or manufacturing requirements are metric, keep source dimensions in inches and add clearly named conversion parameters.

## Parameters

- Prefer named user parameters for key dimensions.
- Use consistent parameter prefixes:
  - p_: primary dimensions
  - clr_: clearances
  - tol_: tolerances
- Document non-obvious parameters in model notes.

## Sketching

- Fully constrain sketches before feature creation.
- Keep one design intent per sketch when possible.
- Avoid projected geometry dependencies unless required.

## Features

- Create simple base features first, then detail features.
- Apply fillets and chamfers late in the timeline.
- Use patterns for repeated geometry instead of copy-paste.

## Assemblies

- Use components, not bodies, for manufacturable parts.
- Define assembly joints with clear motion intent.
- Ground only the primary reference component.

## Manufacturing Readiness

- Include manufacturing clearances in parameters.
- Mark critical dimensions and tolerance assumptions.
- Validate wall thickness and overhang constraints before release.

## Release Checklist

- Timeline warnings resolved.
- Suppressed features reviewed.
- Components named per naming-conventions.md.
- Final export files generated and verified.

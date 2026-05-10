# Naming Conventions

## File Naming

Use lowercase, dash-separated names:

- part-bracket-v1.f3d
- asm-enclosure-main-v2.f3z

Pattern:

[type]-[name]-v[major]

Where type is one of:

- part
- asm
- jig
- fixture

## Component Naming

Use stable names with role-first format:

- frame-main
- panel-left
- standoff-m3-10

## Parameter Naming

- p_width
- p_height
- clr_board_to_wall
- tol_print_hole

## Script Naming

In a360/scripts, use:

- fusion-[purpose].py
- fusion-[purpose]-test.py

Examples:

- fusion-bom-export.py
- fusion-hole-table.py

## Branch Naming

- feat/[short-topic]
- fix/[short-topic]
- docs/[short-topic]

# Fusion 360 Electronics DRC Checklist

**Home-Etch Process · 0.5 oz Copper · 0.032 in FR-4/G10**

| Field | Value |
|---|---|
| **Revision** | Rev 2.1 |
| **Date** | May 2026 |
| **Author** | William |
| **Process** | Toner-Transfer Home Etch / Snapmaker A350 CNC |

---

## Table of Contents

1. [Board Specification Summary](#1-board-specification-summary)
2. [Pre-Layout Checklist](#2-pre-layout-checklist)
3. [Routing Rules](#3-routing-rules)
4. [Hole & Via Rules](#4-hole--via-rules)
5. [Solder Mask Rules](#5-solder-mask-rules)
6. [Thermal Relief Rules](#6-thermal-relief-rules)
7. [Post-Layout DRC Checklist](#7-post-layout-drc-checklist)
8. [Quick Reference Card — Hand Etch v1.1](#8-quick-reference-card--hand-etch-v11)
9. [Notes & Sign-Off](#9-notes--sign-off)
10. [Snapmaker A350 CNC-Optimized Profile (Rev 2.1)](#10-snapmaker-a350-cnc-optimized-profile-rev-21)

---

## 1. Board Specification Summary

The following stack-up parameters apply to all boards designed under this checklist.
Any deviation requires a new DRC file and separate approval.

| Parameter | Value | Notes |
|---|---|---|
| Board Material | `FR-4 / G10` | Standard epoxy-glass laminate |
| Board Thickness | `0.032 in (0.813 mm)` | Nominal; ±10% typical |
| Copper Weight | `0.5 oz / ft² (17.5 µm)` | Thin copper — etch sensitivity high |
| Layer Configuration | `Single- or Double-Sided` | Through-hole hand-drilled vias |
| Etch Method | `Toner-Transfer (Ferric Chloride)` | Home workshop process |
| Drill Method | `Hand Drill / Dremel` | Minimum #68 drill bit |
| DRC File Reference | `home_etch_rules.dru` | Must be active before layout |

---

## 2. Pre-Layout Checklist

Complete all items below **before** beginning PCB layout.

- [ ] **Schematic ERC passed with zero errors** — Run the Electrical Rules Check in Fusion 360 Electronics; resolve all violations before board entry.
- [ ] **All footprints assigned and verified correct** — Confirm each component has the proper land pattern, pin mapping, and courtyard.
- [ ] **Net classes defined** — Create separate net classes for *Power* and *Signal*; assign width and clearance rules per class.
- [ ] **Board outline drawn on Dimension layer** — Closed polygon only; no gaps or overlapping segments.
- [ ] **Design rule file (.dru) loaded and active** — Confirm `home_etch_rules.dru` appears in the DRC dialog as the active rule set before any routing begins.

---

## 3. Routing Rules

All values apply to copper layers (Top / Bottom). The *Preferred* value provides additional etch margin and should be used wherever board density permits.

| Parameter | Minimum | Preferred | Pass ✓ / Fail ✗ |
|---|---|---|---|
| **Trace Width** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **Wire-to-Wire Clearance** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **Wire-to-Pad Clearance** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **Wire-to-Via Clearance** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **Pad-to-Pad Clearance** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **Pad-to-Via Clearance** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **Via-to-Via Clearance** | `0.012 in` (0.305 mm) | `0.016 in` (0.406 mm) | |
| **SMD-to-Pad Clearance** | `0.012 in` (0.305 mm) | — | |
| **SMD-to-Via Clearance** | `0.012 in` (0.305 mm) | — | |
| **SMD-to-SMD Clearance** | `0.012 in` (0.305 mm) | — | |
| **Copper-to-Board Edge** *(wire, pad, via, SMD)* | `0.020 in` (0.508 mm) | — | |
| **Polygon Pour Isolation** (`psIsolate`) | `0.012 in` (0.305 mm) | — | |

> **ℹ️ Preferred Width Palette**
> Route using the following widths only:
> `0.016 in` (signal) · `0.024 in` (power) · `0.032 in` (high-current)

---

## 4. Hole & Via Rules

| Parameter | Value | Tolerance / Note | Pass ✓ / Fail ✗ |
|---|---|---|---|
| **Minimum Drill Diameter** | `0.031 in` (0.787 mm) | #68 drill bit; smallest reliable hand drill | |
| **Via Pad Outer Diameter** | `0.055 in` (1.397 mm) | Pad ratio ≈ 1.774× drill | |
| **Minimum Annular Ring** *(per side)* | `0.012 in` (0.305 mm) | Pad = drill + 2× ring | |
| **Annular Ring Formula** | — | Pad OD ≥ 0.031 + 2 × 0.012 = **0.055 in** | |

---

## 5. Solder Mask Rules

| Parameter | Value | Notes | Pass ✓ / Fail ✗ |
|---|---|---|---|
| **Mask Expansion (Stop Frame)** *(Min & Max)* | `0.004 in` (0.102 mm) | Applied uniformly; min equals max | |
| **Minimum Mask Sliver** | `0.008 in` (0.203 mm) | Smallest bridge of mask between openings | |
| **Via Tenting** (`mlViaStopLimit`) | `0.000 in` | All vias opened; no tenting applied | |
| **SMD Stop Frame Expansion** | `0.004 in` (0.102 mm) | Same expansion as through-hole stop frame | |

---

## 6. Thermal Relief Rules

| Parameter | Value | Notes | Pass ✓ / Fail ✗ |
|---|---|---|---|
| **Thermal Spoke Width** | `0.016 in` (0.406 mm) | Copper spoke entering pad from pour | |
| **Thermal Clearance / Isolate** | `0.014 in` (0.356 mm) | Gap between spoke edge and surrounding pour | |
| **Thermals for Vias** | `Off` | Vias connect solid to pour; no spoke relief | |

> **ℹ️ Thermal Relief Rationale**
> Thermal spokes are required on through-hole component pads to allow reliable hand soldering
> without heat-sinking to the pour. Vias should connect solidly to maximise current capacity.

---

## 7. Post-Layout DRC Checklist

Complete all items below **after** routing is complete. **Zero DRC errors are required to proceed.**

- [ ] **Run Fusion 360 DRC with loaded `.dru` — zero errors required.** Resolve every violation; justify all warnings.
- [ ] **Verify all traces ≥ `0.012 in`** — no routed segment below the minimum.
- [ ] **Verify all clearances ≥ `0.012 in`** — all copper-to-copper pairs (wire, pad, via, SMD).
- [ ] **Verify copper-to-board edge ≥ `0.020 in`** — all layers; check the Dimension layer outline.
- [ ] **Verify minimum drill diameter ≥ `0.031 in`** — no drill smaller than a #68 bit.
- [ ] **Verify annular ring ≥ `0.012 in` per side** — Pad OD ≥ drill + 0.024 in.
- [ ] **Verify mask expansion = `0.004 in`** — min and max stop frame must match.
- [ ] **Verify mask slivers ≥ `0.008 in`** — no mask bridge narrower than this value.
- [ ] **Inspect polygon pours** — ratsnest zero; pour isolation = 0.012 in; component pads have spokes; vias solid.
- [ ] **Check Gerber layer stack** — Top Cu, Bottom Cu, Top Mask, Bottom Mask, Silk, Drill, Board Outline.
- [ ] **Visual inspection in Gerber viewer** — confirm no opens, shorts, or missing features before etching.

---

## 8. Quick Reference Card — Hand Etch v1.1

> Laminate and keep at the workstation. All values are absolute minimums unless labelled Preferred.

| Parameter | Value | Parameter | Value |
|---|---|---|---|
| **Min Trace Width** | `0.012 in` | **Via Pad OD** | `0.055 in` |
| **Preferred Trace** | `0.016 in` | **Annular Ring** | `0.012 in` |
| **Clearance (all pairs)** | `0.012 in` | **Mask Expansion** | `0.004 in` |
| **Cu → Board Edge** | `0.020 in` | **Mask Sliver Min** | `0.008 in` |
| **Min Drill Diameter** | `0.031 in` (#68) | **Thermal Spoke** | `0.016 in` |
| **Pour Isolation** | `0.012 in` | **Thermal Clearance** | `0.014 in` |

---

## 9. Notes & Sign-Off

### Engineer Notes

```
________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________
```

### Sign-Off Block

| Field | Entry |
|---|---|
| **Designer Name** | |
| **Signature** | |
| **Date Released** | |
| **Revision Approved** | |
| **Board Project Name** | |
| **DRC File Used** | `home_etch_rules.dru` |
| **DRC Errors at Release** | **0** — Zero errors required |

---

## 10. Snapmaker A350 CNC-Optimized Profile (Rev 2.1)

The Snapmaker A350 3-in-1 machine (CNC mill, laser, 3D-print) with its CNC work area of
**320 × 350 × 45 mm**, **50 W / 12,000 RPM spindle**, and positional accuracy of **±0.05 mm**
(linear modules — 8 mm Z-axis lead, 20 mm X/Y-axis lead) enables significantly tighter rules
than hand-drilling. Laser resolution is **0.15 mm** via Snapmaker Luban software.

> **Rules in this section supersede Sections 3–6 when using the Snapmaker A350 for CNC drilling.**
> **DRU File:** `home_etch_CNC_rules.dru`

---

### 10.1 Why Tolerances Improve

| Parameter | Hand-Drill (v1.1) | Snapmaker A350 CNC (v2.1) | Improvement |
|---|---|---|---|
| Positional accuracy | `±0.5 mm` (est.) | **`±0.05 mm`** | 10× better |
| Min drill diameter | `0.031 in` (0.787 mm) | **`0.012 in` (0.300 mm)** | −62% |
| Via pad OD | `0.055 in` (1.397 mm) | **`0.028 in` (0.700 mm)** | −50% |
| Annular ring (per side) | `0.012 in` (0.305 mm) | **`0.006 in` (0.150 mm)** | −51% |
| Min trace (etch mode) | `0.012 in` (0.305 mm) | **`0.008 in` (0.203 mm)** | −33% |
| Min trace (CNC mill mode) | `0.012 in` (0.305 mm) | **`0.006 in` (0.152 mm)** | −50% |
| Copper-to-edge | `0.020 in` (0.508 mm) | **`0.015 in` (0.381 mm)** | −25% |
| Min clearance | `0.012 in` (0.305 mm) | **`0.008 in` (0.203 mm)** | −33% |

---

### 10.2 Snapmaker A350 CNC Routing Rules

Two trace sub-modes available — **Etch Mode** is active in the `.dru` file by default.
To switch to **CNC Mill Mode**: replace all `0.2032mm` values with `0.1524mm` in a text editor before importing.

| Parameter | Minimum | Preferred | Pass ✓ / Fail ✗ |
|---|---|---|---|
| **Trace Width (Etch Mode)** | `0.008 in` (0.203 mm) | `0.012 in` (0.305 mm) | |
| **Trace Width (CNC Mill Mode)** | `0.006 in` (0.152 mm) | `0.008 in` (0.203 mm) | |
| **Signal Clearance (all pairs)** | `0.008 in` (0.203 mm) | `0.012 in` (0.305 mm) | |
| **Copper-to-Board-Edge** | `0.015 in` (0.381 mm) | `0.020 in` (0.508 mm) | |
| **Pour Isolation** (`psIsolate`) | `0.008 in` (0.203 mm) | `0.012 in` (0.305 mm) | |

---

### 10.3 Snapmaker A350 CNC Drill / Via / Annular Ring Rules

| Parameter | Value | Notes | Pass ✓ / Fail ✗ |
|---|---|---|---|
| **Min Drill Diameter** | `0.012 in` (0.300 mm) | Practical CNC floor in FR-4; avoid 0.1–0.2 mm (breakage risk) | |
| **Preferred Via Drill** | `0.016 in` (0.400 mm) | Safe daily-use via; excellent yield | |
| **Via Pad OD** | `0.028 in` (0.700 mm) | For 0.4 mm drill + 0.15 mm annular ring × 2 sides | |
| **Pad/Drill Ratio** (`rv*`) | `1.75×` | = 0.700 / 0.400 mm | |
| **Min Annular Ring** | `0.006 in` (0.150 mm) | Per side; CNC ±0.05 mm allows 3× smaller than hand-drill | |
| **Standard Drill Selection** | Match 0.1–1.0 mm table | Pick nearest available CNC drill ≥ component lead diameter | |

---

### 10.4 Drill-Size Selection Table (Snapmaker A350)

Annular ring = 0.15 mm per side for all entries below.

| Lead / Wire Dia | Drill (A350) | Pad OD | Typical Component |
|---|---|---|---|
| 0.20 mm | **0.3 mm** | 0.60 mm | Fine-pitch jumper wire, test pad |
| 0.25 mm | **0.4 mm** | 0.70 mm | Signal via (preferred), thin component lead |
| 0.40 mm | **0.5 mm** | 0.80 mm | Small resistor / capacitor lead (0402–0603 THT) |
| 0.50 mm | **0.6 mm** | 0.90 mm | Transistor / small IC lead |
| 0.60 mm | **0.7 mm** | 1.00 mm | Standard IC DIP lead (0.025 in square) |
| 0.70 mm | **0.8 mm** | 1.10 mm | Standard DIP / connector pin |
| 0.80 mm | **0.9 mm** | 1.20 mm | Large connector pin, thicker wire |
| 0.90 mm | **1.0 mm** | 1.30 mm | Power terminal, heavy lead |

---

### 10.5 Solder Mask (Unchanged from v1.1)

| Parameter | Value |
|---|---|
| Mask Expansion | `0.004 in` (0.102 mm) |
| Min Mask Sliver | `0.008 in` (0.203 mm) |
| Via Tenting | Off (all vias open) |

---

### 10.6 Thermal Relief (Unchanged from v1.1)

| Parameter | Value |
|---|---|
| Thermal Clearance | `0.014 in` (0.356 mm) |
| Spoke Width | `0.016 in` (0.406 mm) |
| Thermals for Vias | Off |

---

### 10.7 Snapmaker A350 CNC Post-Layout DRC Checklist

- [ ] **Load `home_etch_CNC_rules.dru`** — confirm Rev 2.1 in the DRC dialog description field.
- [ ] **Run DRC — zero errors required** before proceeding to any machine output.
- [ ] **Verify all traces ≥ `0.008 in`** (Etch Mode) or **≥ `0.006 in`** (CNC Mill Mode).
- [ ] **Verify all clearances ≥ `0.008 in`** — all signal copper pairs.
- [ ] **Verify copper-to-edge ≥ `0.015 in`** — all copper layers, all edge segments.
- [ ] **Verify all drill diameters ≥ `0.012 in`** — no drill below `0.3 mm` in FR-4.
- [ ] **Confirm all drills map to Snapmaker A350 available sizes** (0.1–1.0 mm in 0.1 mm steps or standard carbide set).
- [ ] **Verify annular ring ≥ `0.006 in` per side** for every padstack.
- [ ] **Verify via pad OD ≥ `0.028 in`** for 0.4 mm drill — adjust proportionally for larger drills.
- [ ] **Export drill file (Excellon)** and verify all sizes match the A350 tool magazine for this job.
- [ ] **Run CNC simulation / dry run** in air before cutting FR-4 — confirm tool paths and depths.
- [ ] **Visual inspect drilled board under magnification** — annular ring visible and unbroken on all sides of every pad.

---

### 10.8 Quick Reference Card — Snapmaker A350 CNC v2.1

| Parameter | Value | Parameter | Value |
|---|---|---|---|
| **Min Trace (Etch)** | `0.008 in` | **Min Trace (Mill)** | `0.006 in` |
| **Clearance** | `0.008 in` | **Cu → Edge** | `0.015 in` |
| **Min Drill** | `0.012 in` | **Pref Drill** | `0.016 in` |
| **Via Pad OD** | `0.028 in` | **Annular Ring** | `0.006 in` |
| **Mask Expansion** | `0.004 in` | **Mask Sliver** | `0.008 in` |
| **Thermal Spoke** | `0.016 in` | **Thermal Clr** | `0.014 in` |
| **DRU File** | `home_etch_CNC_rules.dru` (Rev 2.1) | | |

---

## DRU File Reference

| File | Profile | Rev | Use When |
|---|---|---|---|
| `home_etch_rules.dru` | Hand-Etch | v1.1 | Hand drill / standard drill press |
| `home_etch_CNC_rules.dru` | Snapmaker A350 CNC | v2.1 | CNC drilling with Snapmaker A350 |

### Importing into Fusion 360 Electronics

1. Open your board file (`.brd`) in Fusion 360 Electronics
2. **Edit → Design Rules** (or click the DRC toolbar icon)
3. Click **Load…** → select the `.dru` file
4. Click **Apply** → **Run DRC**
5. Confirm revision matches in the Description field

### Switching to CNC Mill Mode (v2.1 file)

In `home_etch_CNC_rules.dru`, find-and-replace `0.2032mm` → `0.1524mm` before importing.
This updates `msWidth` and all nine `md*` clearance parameters in one pass.

---

*Fusion 360 Electronics DRC Checklist — Home-Etch 0.5 oz FR-4 | Rev 2.1 | May 2026*  
*Author: William | UNCONTROLLED WHEN PRINTED*

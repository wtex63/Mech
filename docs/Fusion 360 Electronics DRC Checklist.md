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
---

## 11. Thermal Spoke Width — Required Manual Step After .edru Import

> ⚠️ **The thermal spoke width is NOT stored in the `.edru` file. It must be set manually in the Fusion 360 Electronics DRC dialog every time a new `.edru` is loaded.**

### Procedure

1. Import the `.edru` file via **DRC dialog → Import** (folder icon)
2. Do **NOT** click Apply yet
3. In the DRC dialog locate **Supply Layer → Spoke Width**
4. Set **Spoke Width = `10 mil` (0.254 mm)**
5. Click **Apply → OK**
6. Run DRC to verify

| ☐ | Parameter | Value | Notes |
|---|---|---|---|
| ☐ | **Spoke Width** | `10 mil` / 0.254 mm | Set in **DRC → Supply Layer → Spoke Width** — NOT in file |
| ☐ | **Number of Spokes** | 4 | Default cross pattern; use 2 only for very congested areas |
| ☐ | **Thermal Gap** | `10 mil` / 0.254 mm | `slThermalIsolate` — IS saved in `.edru` |
| ☐ | **Thermals for Vias** | Off | `slThermalsForVias=0` — IS saved in `.edru` |

---

## 12. Ground Plane Stitching on Single-Sided PCB

On a single-sided home-etched PCB, the top copper ground plane sometimes cannot reach every GND connection due to clearance conflicts with signal traces. Fusion 360 Electronics can route GND jumpers on **Layer 16 (Bottom)** even when the board is fabricated single-sided. These bottom-layer segments become **physical wire jumpers** — short lengths of bare tinned wire soldered through drilled holes from the component side.

### 12.1 Enabling Bottom-Layer GND Routing in Fusion 360

1. In the Board editor, confirm **Layer 16 (Bottom)** is active and visible in the Layers panel
2. Open **DRC dialog → Layer Setup** → confirm layer pair is `(1*16)` — tells Fusion 360 both layers exist even for single-sided etch
3. In the **Route** menu → **Interactive Router** → select **Layer 16** from the layer selector in the toolbar *before* clicking the airwire
4. Route the GND airwire — it appears as a bottom-layer trace (shown in blue)
5. Repeat for each unrouted GND airwire that cannot clear on the top layer
6. Run **Ratsnest** — verify 0 airwires remain
7. Run **DRC** — bottom-layer GND traces pass if layer pair `(1*16)` is configured

### 12.2 Workflow: Single-Sided Etch with Wire Jumpers

| Step | Action | Notes |
|---|---|---|
| 1 | Route all signals on Layer 1 (Top) | Normal top-layer routing |
| 2 | Fill GND polygon on Layer 1 (Top) | Copper pour; thermal relief on THT pads |
| 3 | Identify remaining GND airwires | Run Ratsnest; count unrouted GND connections |
| 4 | Route GND jumpers on Layer 16 (Bottom) | Interactive Router → select Bottom layer → route each airwire |
| 5 | Via pads placed automatically | Fusion 360 inserts via pads when routing crosses to bottom |
| 6 | Verify Ratsnest = 0 | Run Ratsnest command |
| 7 | Export Gerbers — two copper files | Top (layer 1) = etch this side; Bottom (layer 16) = jumper wire map only |
| 8 | Drill the via holes | Use the Excellon drill file; all via hole locations included |
| 9 | Fabricate: etch top side only | Ignore the bottom copper Gerber for etching |
| 10 | Install jumpers | Cut bare tinned wire to length; insert through via holes; solder both ends on component side |

### 12.3 Tips for Minimum Jumper Count

- Place the GND polygon (unfilled) **before** routing signals — Fusion 360 shows which pads auto-connect; reduces required jumpers
- Route **power and ground traces first**, wide (20–30 mil); signals route around them
- Place decoupling capacitors **as close as possible** to IC VCC/GND pins — shorter GND path = fewer polygon islands
- Use the **Ripup tool** to un-route a blocking signal trace, re-route on a different path to open a GND clearance corridor
- If two GND islands are separated by one signal trace, a **single via/jumper pair** spanning that trace stitches them

---

## 13. Home-Etch Solder Mask — Chemistry and Process Guide

Photoimageable solder mask is a **negative-working, UV-crosslinkable polymer coating**. Unexposed areas remain soluble in aqueous carbonate developer; UV exposure converts the resin from a linear oligomer to a crosslinked thermoset via radical chain-growth polymerization, rendering it insoluble. Two product forms are available for home fabrication: **liquid photoimageable solder mask (LPSM)** applied by squeegee, and **dry-film solder mask (DFSM)** laminated by heated roller.

### 13.1 Chemistry Reference

| Stage | Chemistry | Key Variables |
|---|---|---|
| **Resin system** | Epoxy-acrylate or urethane-acrylate oligomer; reactive diluent monomers (TPGDA, HDDA) reduce viscosity | % monomer controls coating viscosity and film flexibility |
| **Photoinitiator** | Norrish Type II system: benzophenone + co-initiator (amine); absorbs at 365 nm (i-line) and 395 nm | Oxygen inhibition at the air interface causes surface tack — normal, not a defect |
| **Pre-bake** | Drives off carrier solvent (NMP, PGMEA, glycol ether); Tg increases; film becomes tack-free | 75–80°C / 15–20 min; overdrying reduces adhesion |
| **UV Exposure** | Radical chain polymerization crosslinks acrylate double bonds; dose = irradiance × time | 365 nm optimal; 395 nm LED arrays work at 1.5–2× time; typical dose 200–400 mJ/cm² |
| **Development** | 1% w/v Na₂CO₃ in DI water; base saponifies unreacted acrylate ester groups, solubilizing unexposed areas | pH ≈11.4; 25–30°C; 45–90 s with gentle agitation; rinse with DI water |
| **Post-cure** | Thermal (150°C / 30–60 min) crosslinks residual epoxy groups via ionic ring-opening; UV flood reduces surface tack | Tg increases from ~80°C pre-cure to ~130–150°C post-cure; critical for chemical resistance to flux solvents |

### 13.2 Recommended Products (Home Scale)

| Product | Form | Developer | Notes |
|---|---|---|---|
| **MG Chemicals 4226** | Liquid (squeeze bottle) | 1% Na₂CO₃ aqueous | Most accessible; apply with credit card squeegee; best starting point |
| **Dynamask 5000** | Dry film roll | 1% Na₂CO₃ aqueous | Requires heated laminator 80–110°C; very uniform thickness; excellent for SMD |
| **Ordyl SY 300** | Dry film roll | 1% Na₂CO₃ aqueous | Thinner film (50 µm); better fine-feature resolution; good for 0603 pitch |

### 13.3 Step-by-Step Process — MG Chemicals 4226 LPSM

1. **SURFACE PREP** — 400-grit abrasive pad + IPA wipe. Copper must be dull-matte, no fingerprints. *(C₁₄–C₁₈ fatty acids in fingerprint oils block acrylate surface adhesion.)*
2. **APPLY** — Bead of 4226 across board, squeegee with credit card at 45° in one pass. Target wet thickness: 50–75 µm.
3. **PRE-BAKE** — 75°C / 15 min. Film tack-free. Do not exceed 85°C — premature thermal cure reduces photosensitivity.
4. **PREPARE FILM POSITIVE** — Print Gerber layer 29 (tStop) as a **positive** on transparency film: **black = pad openings, clear = mask coverage.**
5. **EXPOSE** — Film emulsion-down on board, weighted flat with glass. 365 nm = 2–3 min; 395 nm LED = 4–6 min at 10 mW/cm². *(Any air gap allows O₂ diffusion → oxygen inhibition of radical chain → undercure at mask edges.)*
6. **DEVELOP** — 1% Na₂CO₃ (10 g/L washing soda in DI water), 25–30°C, gentle agitation 60–90 s. Rinse 30 s DI water.
7. **INSPECT** — Pad openings fully clear; mask edges sharp. Scumming = re-develop 15 s.
8. **POST-CURE** — UV flood 3–5 min, then **150°C / 30 min** oven. Completes epoxy ring-opening; maximises resistance to rosin flux, IPA, acetone.

### 13.4 Fusion 360 Gerber Export for Solder Mask

- **Layer 29 (tStop)** = Top mask openings → export as UV artwork positive
- **Layer 30 (bStop)** = Bottom mask openings
- Print at exactly **1:1 scale** (no scaling) on transparency film
- **Registration check**: hold film over board against light — pad circles must exactly overlay copper pads before exposing

---

## 14. CNC Zero-Point Calibration Mark — Copper Fiducial for Snapmaker A350

CNC drilling accuracy depends entirely on **registration** between the photolithographic origin and the CNC machine's work origin. A copper crosshair fiducial etched into the board provides a permanent, high-contrast reference point that the Snapmaker A350 locates before drilling, eliminating misregistration from board placement offset and rotation error.

### 14.1 Why Registration Matters

| Error Source | Typical Magnitude | Effect on Drilling |
|---|---|---|
| Board placement offset (X/Y) | 0.5–3 mm | All holes shifted uniformly; may miss annular rings |
| Board rotation error | 0.1–0.5° | Holes drift from pads; worst at corners (≈0.5 mm on a 100 mm board at 0.3°) |
| **Cumulative — no fiducial** | **Up to 3–4 mm** | **Many holes outside annular ring; board scrapped** |
| **With copper fiducial + A350** | **< 0.1 mm** | **Well within 0.15 mm annular ring on 0603 pads** |

### 14.2 Copper Fiducial Design

| Feature | Dimension | Layer | Notes |
|---|---|---|---|
| **Centre dot** | 0.5 mm diameter solid circle | Layer 1 Top copper | Probe tip aiming point |
| **Crosshair arms** | 4 × (10 mm long × 0.2 mm wide) N/S/E/W | Layer 1 Top copper | Extends ±5 mm from centre; visible in Luban camera |
| **Outer ring** | 3 mm diameter, 0.2 mm trace | Layer 1 Top copper | Confirms centre; aids visual alignment |
| **Mask opening** | 8 × 8 mm square, no mask | Layer 29 tStop | Bare copper = high contrast; do NOT tin the fiducial |
| **Silkscreen label** | `ORIGIN`, 1 mm height | Layer 21 tPlace | Identifies the mark on the assembled board |

### 14.3 Creating the Fiducial in Fusion 360 Library Editor

1. **File → New → Library** → create Package named `CNC_FIDUCIAL_CROSS`
2. **tCu (Top copper)**: circular SMD pad, 0.5 mm diameter, no drill, at (0, 0) — centre aiming dot
3. **tCu**: four lines from (0,0) to (±5, 0) and (0, ±5), width = 0.2 mm — crosshair arms
4. **tCu**: circle, diameter = 3 mm, width = 0.2 mm — outer alignment ring
5. **tStop**: square pad 8 × 8 mm at (0,0) — opens solder mask over entire mark
6. **tPlace**: text `ORIGIN` 1 mm below mark
7. Place footprint on board at **(2, 2) mm from lower-left corner** — known offset from physical corner

### 14.4 Two-Fiducial Method (Corrects Rotation)

Place a **second fiducial** at **(board_width − 2, board_height − 2) mm** — the diagonally opposite corner.

| Fiducial | Placement | Purpose |
|---|---|---|
| **REF1** (primary) | (2, 2) mm from lower-left | Defines X=0, Y=0 work origin |
| **REF2** (secondary) | (W−2, H−2) mm from lower-left | Defines board rotation angle θ |

> **Engineering note:** The two-fiducial method is mathematically equivalent to a two-point rigid-body coordinate frame transformation — the same registration problem solved when aligning piping spools to survey control benchmarks in refinery construction. REF1 and REF2 are your control points.

### 14.5 Snapmaker A350 Calibration Workflow

1. **Etch** — copper fiducials etch simultaneously with the board; no extra step needed
2. **Mount** board on A350 bed with double-sided tape; rough-position flat
3. In **Luban**: home all axes (G28); switch to CNC module
4. **Jog spindle** to visually centre over REF1 using Luban camera overlay
5. **Touch off**: lower spindle over the 0.5 mm copper centre dot; tip just contacts the copper surface
6. In Luban: **Set Work Origin** (X=0, Y=0, Z=0) — your G54 work coordinate origin
7. **Jog to REF2** at (board_width−4, board_height−4); verify camera alignment matches second fiducial
8. **If REF2 is offset**: adjust board rotation on bed; re-home to REF1; repeat until REF2 aligns within ±0.1 mm
9. Load **Excellon drill file**; run — all holes now reference the copper origin
10. **Verify first hole** visually before running the full drill program

### 14.6 Fiducial Checklist

| ☐ | Item | Notes |
|---|---|---|
| ☐ | `CNC_FIDUCIAL_CROSS` placed at (2, 2) mm from lower-left | REF1 — primary origin |
| ☐ | Second fiducial at (W−2, H−2) mm | REF2 — rotation reference |
| ☐ | tStop open 8×8 mm over each fiducial | Bare copper for high contrast |
| ☐ | Fiducials excluded from BOM | Mark `POPULATE=NO` |
| ☐ | Gerber layer 1 includes fiducial copper | Verify in Gerber viewer |
| ☐ | Drill file origin = Fusion 360 board origin (0,0) | Do NOT move board origin after placing fiducials |
| ☐ | Pre-drill: jog to REF1 in Luban before running drill file | Never skip on a new board |

---

## Complete .edru File Index

| File | Profile | Rev | Use When |
|---|---|---|---|
| `home_etch_hand_drill.edru` | Hand-Etch, conservative | v1.1 | THT-only boards, hand drill |
| `snapmaker_a350_CNC.edru` | A350 CNC, moderate | v2.1 | Mixed THT/SMD, A350 CNC drill |
| `home_etch_SMD_aggressive.edru` | Hand-Etch, SMD-tuned | v3.0 | 0603/0805 dense SMD, toner etch |
| `snapmaker_a350_SMD_aggressive.edru` | A350 CNC, SMD-tuned | v3.1 | 0603/0805 dense SMD, A350 CNC drill |
| `home_etch_05oz_FR4.edru` | Home-Etch, general | v1.0 | General purpose 0.5 oz FR-4, hand drill |

---

*Fusion 360 Electronics DRC Checklist — Home-Etch 0.5 oz FR-4 | Rev 3.1 | May 2026*
*Author: William | UNCONTROLLED WHEN PRINTED*
## Section 15 — Multi-Board Panel Etching: Toner Transfer + Snapmaker A350 Registration

---

### 15.1 The Panel Concept: One Origin Drills All Boards

> **Critical Principle:** The toner transfer print and the Excellon drill file both originate from the **same Fusion 360 panel file**. They share the same coordinate system. Align the A350 to the **Panel REF1** copper mark (etched by the toner transfer), set work origin **once**, and run the single combined drill file. All holes for all boards are drilled in one uninterrupted operation.

| Item | Single Board | 2-Board Panel | 3-Board Panel |
|---|---|---|---|
| Toner transfer sheets | 1 | 1 | 1 |
| A350 work-origin alignments | 1 | 1 | 1 |
| Excellon drill file runs | 1 | 1 | 1 |
| Boards produced per etch | 1 | 2 | 3 |

---

### 15.2 Panel Layout in Fusion 360 Electronics

Fusion 360 has no native panelization wizard — use the manual copy-paste method.

#### Prerequisites
- Board 1 DRC must pass **zero errors** before panelizing
- Board 1 must contain `CNC_FIDUCIAL_CROSS` at `(2, 2)` and `(W−2, H−2)` per Section 14

#### Procedure

**Step 1 — Complete Board 1** — verify DRC = 0 errors, fiducials at correct positions.

**Step 2 — Create panel board file**
```
File → New → Board
Save as: Panel_2x.brd
Layer 20 (Dimension): rectangle W_panel × H
  W_panel = (N × board_width) + ((N−1) × gap)   [gap = 3 mm recommended]
```

**Step 3 — Copy Board 1 into panel at (0, 0)**
```
In Board 1:  Edit → Select All (Ctrl+A) → Copy (Ctrl+C)
In Panel:    Edit → Paste (Ctrl+V)
Position:    X = 0,  Y = 0
```

**Step 4 — Paste additional boards at X offsets**
```
Board 2:  X = W + G,      Y = 0
Board 3:  X = 2(W + G),   Y = 0
Board N:  X = (N−1)(W+G), Y = 0
```

**Step 5 — Verify the panel**
```
Ratsnest → must report 0 airwires
DRC      → must report 0 errors
```

**Step 6 — Export single combined Gerber + Excellon from the panel file**
```
Verify Excellon hole count = N × single-board hole count
```

---

### 15.3 Panel Coordinate Reference Table

*W* = single board width (mm), *H* = board height (mm), *G* = gap (mm, recommend 3)

| Reference Point | X (panel absolute) | Y (panel absolute) | Purpose |
|---|---|---|---|
| Board 1 lower-left | 0 | 0 | Board 1 origin |
| **Board 1 REF1 = Panel REF1** | 2 | 2 | **A350 work origin — set X=0, Y=0, Z=0 here** |
| Board 1 REF2 | W−2 | H−2 | Board 1 rotation verification |
| Board 2 lower-left | W+G | 0 | Board 2 origin |
| Board 2 REF1 | W+G+2 | 2 | Verify A350 at (W+G, 0) from work origin |
| Board 2 REF2 = Panel REF2 | 2W+G−2 | H−2 | Full panel rotation correction |

> **Engineering analogy:** Identical to two-point rigid-body coordinate transformation used in piping spool alignment to survey benchmarks — two control points define position and rotation uniquely; all derived hole positions follow automatically.

---

### 15.4 Panel Layout Diagram

```
 PANEL — 2-Board Example (W=60mm, H=50mm, G=3mm → 123×50mm panel)
 ┌─────────────────────────────────────────────────────────────────────┐
 │  ⊕ Board1_REF1 (2,2)                   ⊕ Board2_REF1 (65,2)       │
 │   ┌─────────────────────────┐  3mm  ┌─────────────────────────┐    │
 │   │                         │ ←gap→ │                         │    │
 │   │       BOARD 1           │       │       BOARD 2           │    │
 │   │       (0,0)→(60,50)     │       │       (63,0)→(123,50)   │    │
 │   │               ⊕(58,48) │       │               ⊕(121,48) │    │
 │   │        Board1_REF2      │       │        Board2_REF2      │    │
 │   └─────────────────────────┘       └─────────────────────────┘    │
 │                                                                     │
 │  Panel REF1 = Board1_REF1 = (2,2)   ← A350 work origin            │
 │  Panel REF2 = Board2_REF2 = (121,48) ← rotation verification       │
 └─────────────────────────────────────────────────────────────────────┘
```

---

### 15.5 Board Separation Methods

| Method | Gap Required | A350 Role | Notes |
|---|---|---|---|
| Score and snap | 0–1 mm | None | Knife + steel rule; 5–7 scoring passes |
| **Mouse-bite perforations** | 2.5–3 mm | **Drills 0.8 mm holes at 1.2 mm pitch** | Recommended; clean break; A350 does the work |
| Tab routing | 3–5 mm | 1 mm end mill routes slots | Best vibration resistance during drilling |

#### Adding Mouse-Bite Holes in Fusion 360

```
Layer:     20 (Dimension) — mark gap centreline at X = W + G/2
Component: Unconnected round pad, 0 mm copper ring, 0.8 mm drill, no net
Spacing:   Place every 1.2 mm in Y, from Y=1 mm to Y=H−1 mm
Result:    Appears in Excellon drill file automatically
Luban:     Assign 0.8 mm drill bit for these holes in tool table
```

---

### 15.6 Snapmaker A350 Drilling Workflow — Multi-Board Panel

| Step | Action | Details |
|---|---|---|
| 1 | Mount panel | Copper-side up; double-sided tape; full panel is one piece at this stage |
| 2 | Home all axes | G28 in Luban; switch to CNC module |
| 3 | Jog to Panel REF1 | Board 1 REF1 ⊕ crosshair, 2 mm in from board 1 lower-left; centre using Luban camera overlay |
| 4 | Touch off surface | Z touch; set **Work Origin X=0, Y=0, Z=0** — this is the global panel coordinate origin |
| 5 | Verify Board 2 REF1 | Jog to X = W+G, Y = 0 (e.g., X=63 for 60 mm boards + 3 mm gap); camera must align to Board 2 REF1 copper mark; offset > ±0.2 mm → re-mount and repeat |
| 6 | Verify Board 1 REF2 | Jog to X = W−4, Y = H−4; camera must align to Board 1 REF2 copper mark |
| 7 | Load combined Excellon | Single panel drill file in Luban; confirm hole count = N × single-board count |
| 8 | Run drill file | A350 drills ALL holes for ALL boards — one uninterrupted operation |
| 9 | Separate boards | Mouse-bite snap, score-and-snap, or tab route as designed |

---

### 15.7 Toner Transfer Tips for Multi-Board Panels

- **Print at 1:1 scale** — disable "fit to page" in the print dialog; measure a known dimension on the printout before transferring
- **Mirror the top copper layer** before printing — image must be laterally inverted so it reads correctly from above after face-down transfer
- **Use heavy glossy photo paper** (170–200 g/m²) — a 2-board panel can fill a full A4/Letter sheet
- **Apply heat section by section** — large panels amplify pressure variation; iron at 160–180°C using a flat rigid backing board
- **Peel slowly, warm** — not hot, not cold; if any area lifts prematurely, re-iron before continuing
- **Inspect all traces on all boards before separation** — hold the etched panel to a light source; rework as one piece is far easier than as individual boards
- **Fiducial marks etch with the traces** — they are part of the top copper Gerber; no separate step needed

---

### 15.8 Panel Pre-Flight Checklist

- [ ] Board 1 DRC passed zero errors before panelization
- [ ] Panel board file created; outline on Layer 20 (full rectangle, closed)
- [ ] N board copies pasted at correct X offsets: 0, W+G, 2(W+G) …
- [ ] Panel Ratsnest = 0 airwires
- [ ] Panel DRC = 0 errors
- [ ] Board 2 REF1 absolute coordinates noted: X = W+G+2, Y = 2
- [ ] Mouse-bite holes added along gap centreline (0.8 mm @ 1.2 mm pitch)
- [ ] Single combined Excellon exported from panel file; hole count verified
- [ ] Gerber printed at 1:1 scale, mirrored; scale verified by measurement
- [ ] Toner transfer applied and etched; all traces intact on all boards
- [ ] A350 work origin set at Board 1 REF1 copper fiducial (X=0, Y=0, Z=0)
- [ ] Board 2 REF1 verified at (W+G, 0) from work origin; within ±0.2 mm
- [ ] Combined Excellon loaded; total hole count confirmed in Luban
- [ ] Boards separated after drilling

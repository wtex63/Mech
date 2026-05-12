# XBee Garage Door Sensor - Complete Hardware Wiring

Date: 2026-05-11
Board: XBee ZB (S2B) Programmable
Power: 3xAAA NiMH rechargeable in series (~4.2V fresh, ~3.0V near end-of-life)

---

## 1. Design Update Summary

This revision replaces the prior XC9140 boosted sensor rail with an XC6220A331MR-G gated LDO rail.

- Keep XBee on an always-on 3.3V rail from MCP1700.
- Use XC6220A331MR-G for the gated 3.3V sensor rail.
- Gate XC6220A with XBee XPIN13 (ON/SLEEP) using CE/EN control.
- Keep DS18B20 parasite-power strong pull-up topology on XPIN12.

Why this change:

- 3xAAA NiMH can exceed the prior boost converter comfort zone when fresh.
- XC6220A directly regulates 3xAAA battery voltage to 3.3V.
- No extra regulator-gating MOSFET is required.

---

## 2. XBee Pin Assignment Summary

```text
XPIN1  = VCC (3.3V always-on from MCP1700)
XPIN7  = Door tilt IRQ input
XPIN10 = GND
XPIN11 = DS18B20 DQ (1-Wire bus)
XPIN12 = Strong pull-up PMOS gate control (active-LOW)
XPIN13 = ON/SLEEP output -> XC6220A CE/EN control
XPIN14 = VCC REF (tie to 3.3V always-on rail)
XPIN15 = Association/status LED output
XPIN18 = Battery ADC sense (divider from raw battery)
XPIN20 = Commissioning button input (active LOW)
```

IPC net-name note:

- `VCC` = 3.3V_A (always-on rail from MCP1700).
- `3.3V` = 3.3V_S (gated sensor rail from XC6220A).

IPC reference-designator note:

- `IC1` in IPC = MCP1700 (always-on regulator).
- `U1` in IPC = XC6220A331MR-G (gated sensor regulator, CE/EN net `N$11`).
- `U$1` in IPC = XBee module footprint.

---

## 3. Power Supply Topology

### 3.1 Always-On XBee Rail (U1)

MCP1700 remains the always-on regulator for XBee sleep/wake reliability.

```text
3xAAA(+) ----> U1 MCP1700 VIN
GND      ----> U1 MCP1700 GND
U1 VOUT  ----> 3.3V_A (always-on)

3.3V_A -> XBee XPIN1 (VCC)
3.3V_A -> XBee XPIN14 (VREF)
3.3V_A -> C6 0.1uF to GND (near XBee)
3.3V_A -> C2 10uF to GND (bulk)
```

### 3.2 Gated Sensor Rail (U2)

XC6220A331MR-G replaces XC9140.

```text
3xAAA(+) ----> U2 XC6220A VIN
GND      ----> U2 GND
XPIN13   ----> U2 CE/EN
U2 VOUT  ----> 3.3V_S (gated)

3.3V_S -> C3 10uF to GND (at U2)
3.3V_S -> Strong pull-up PMOS source
```

Control behavior:

- XPIN13 HIGH (XBee awake): U2 ON, 3.3V_S active.
- XPIN13 LOW (XBee asleep): U2 OFF, 3.3V_S off.

Recommended CE/EN network (for startup determinism):

- R4 = 1k series from XPIN13 to U2 CE/EN.
- R3 = 100k pull-down from U2 CE/EN to GND.

### 3.3 Grounding

All grounds must remain common:

- Battery-, U1 GND, U2 GND, XBee XPIN10, DS18B20 GND, tilt network GND, and all capacitor returns.

---

## 4. DS18B20 Parasitic Strong Pull-Up

Keep DS18B20 in parasite mode:

- DS18B20 pin 1 (GND) -> GND
- DS18B20 pin 2 (DQ)  -> DQ net -> XPIN11
- DS18B20 pin 3 (VDD) -> GND

Strong pull-up remains PMOS high-side on DQ, controlled by XPIN12 (active-LOW).

```text
3.3V_S -- R7 4.7k --+-- DQ -- XPIN11 -- DS18B20 pin2
                    |
                    +-- PMOS drain
3.3V_S ---------------- PMOS source
XPIN12 -- R9 100~180R -- PMOS gate
PMOS gate -- R8 100k -- 3.3V_S
```

Firmware polarity:

- XPIN12 LOW  -> PMOS ON  -> strong pull-up active.
- XPIN12 HIGH -> PMOS OFF -> weak pull-up only.

---

## 5. Tilt, LED, Commissioning, and ADC

These sections are electrically unchanged from the previous validated design:

- Tilt input on XPIN7 with external RC debounce/filter.
- Status LED on XPIN15 via series resistor.
- Commissioning button on XPIN20 to GND.
- Battery ADC on XPIN18 via divider from raw battery.

Battery divider scaling should now target 3xAAA NiMH operating range.

### 5.1 Fitted Values (From Latest SPICE Export)

These are the currently fitted values reflected by the latest schematic export.
For the tilt network test build, C4 is intentionally set to 100nF X7R ceramic.

| Ref | Value | Role |
| --- | --- | --- |
| R1 | 82k | Battery divider low side (XPIN18 to GND) |
| R2 | 220k | Battery divider high side (VBAT to XPIN18) |
| R3 | 100k | CE/EN pull-down |
| R4 | 1k | XPIN13 to CE/EN series |
| R5 | 1k | Tilt switch series path to XPIN7 |
| R6 | 1M | Tilt bias to GND |
| R7 | 4.7k | DQ weak pull-up |
| R8 | 100k | PMOS gate bias |
| R9 | 100 | PMOS gate series |
| R10 | 330 | LED series resistor |
| R11 | 10k | Commissioning input series |
| C1 | 10uF | VBAT bulk decoupling |
| C2 | 10uF | VCC bulk decoupling |
| C3 | 10uF | 3.3V_S bulk decoupling |
| C4 | 100nF (X7R) | Tilt RC capacitor (test build) |
| C5 | 100nF | Commissioning input debounce capacitor |
| C6 | 0.1uF | VCC high-frequency bypass |

---

## 6. Bring-Up Checklist (Updated)

1. Confirm U1 output is stable 3.3V_A before inserting XBee.
2. Confirm U2 output (3.3V_S) toggles with XPIN13 state.
3. Confirm no hard short between 3.3V_A and 3.3V_S.
4. Confirm DQ idle level near 3.3V.
5. Confirm DQ remains >= 3.0V during the 750ms Convert-T strong pull-up window.
6. Confirm door tilt events wake and report on both state transitions.
7. Confirm sleep current with U2 OFF meets battery-life target.

---

## 7. Key Requirement

XBee must remain continuously powered on 3.3V_A.
Do not gate U1 output and do not remove always-on power to XPIN1.

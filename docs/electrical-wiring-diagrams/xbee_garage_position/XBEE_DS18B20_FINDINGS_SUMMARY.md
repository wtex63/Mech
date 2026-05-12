# XBee + DS18B20 Findings Summary

Date: 2026-05-11

This file is the consolidated findings record for the XBee garage position build and now includes complete wiring guidance for the updated 3xAAA NiMH power architecture.

## 1) Comparison Result (Arduino vs Mech Copy)

1. The Mech copy previously omitted detailed wiring sections found in the Arduino findings file.
2. The missing sections included complete rail wiring, detailed sensor interconnects, and battery-monitor implementation detail.
3. This Mech file is now expanded to include those details, updated for the new power strategy:
    - 3xAAA NiMH battery input.
    - MCP1700 always-on XBee rail.
    - XC6220A331MR-G gated sensor rail via XPIN13 -> CE/EN.

## 2) Current Design Decision

1. Keep XBee continuously powered from MCP1700 3.3V rail (always-on).
2. Replace prior XC9140 gated rail with XC6220A331MR-G.
3. Gate XC6220A CE/EN from XPIN13 (ON/SLEEP) using:
    - R4 = 1k series (XPIN13 to CE/EN).
    - R3 = 100k pull-down (CE/EN to GND).
4. Keep DS18B20 in parasite mode with PMOS strong pull-up controlled by XPIN12 (active-LOW).

## 3) Complete Wiring (Updated)

### 3.1 Power Rails

```text
3xAAA(+) ----+-------------------------------> U1 MCP1700 VIN
                 |
                 +-------------------------------> U2 XC6220A VIN

Common GND --+-------------------------------> U1 GND
                 +-------------------------------> U2 GND
                 +-------------------------------> XBee XPIN10
                 +-------------------------------> DS18B20 GND

U1 VOUT (3.3V_A always-on) ------------------> XBee XPIN1 (VCC)
                                                            +-> XBee XPIN14 (VREF)
                                                            +-> DQ weak pull-up source (R7)

U2 VOUT (3.3V_S gated) ----------------------> PMOS source (strong pull-up supply)

XPIN13 (ON/SLEEP) -- R4 1k --> U2 CE/EN
U2 CE/EN ----------- R3 100k --> GND
```

State behavior:

1. XPIN13 HIGH -> U2 ON -> 3.3V_S active.
2. XPIN13 LOW -> U2 OFF -> 3.3V_S off.

### 3.2 DS18B20 Parasite + Strong Pull-Up

```text
DS18B20 pin1 (GND) ---------------------------> GND
DS18B20 pin2 (DQ)  ---------------------------> DQ net -> XPIN11
DS18B20 pin3 (VDD) ---------------------------> GND (parasite mode)

3.3V_S ---- R7 4.7k ----+---- DQ ---- XPIN11
                                |
                                +---- PMOS drain

3.3V_S ---------------------- PMOS source
XPIN12 --- R9 100..180R ---- PMOS gate
PMOS gate ---- R8 100k ------ 3.3V_S
```

Control polarity:

1. XPIN12 LOW -> PMOS ON -> strong pull-up active during Convert-T.
2. XPIN12 HIGH -> PMOS OFF -> weak pull-up only.

### 3.3 Tilt / Door Input

```text
3.3V_A ---- S1 ---- N$9 ---- R5 ----+---- XPIN7
                                     |
                                     +---- R6 ---- GND
                                     |
                                     +---- C4 ---- GND
```

### 3.4 Commissioning Button and LED

```text
XPIN20 ---- R11 10k ---- pushbutton ---- GND
               |
               +---- C5 100nF ---- GND

XPIN15 ---- R10 330R ---- LED ---- GND
```

Optional commissioning debounce:

1. R11 = 10k series at XPIN20.
2. C5 = 100nF from XPIN20 node to GND.

### 3.5 Battery Monitoring (Required)

Raw battery must be measured before regulators on XPIN18 ADC.

Updated divider for 3xAAA NiMH:

```text
BAT+ ---- R2 220k ----+---- XPIN18 (ADC)
                              |
                              +---- R1 82k ---- GND
```

Reason for value change:

1. Previous 100k/100k divider was suitable for 2xAA but is too high at 3xAAA fresh voltage.
2. 220k/82k keeps ADC node in a safer range at pack peak voltage while reducing divider drain.

Scaling:

1. Divider ratio = R1 / (R2 + R1) = 82 / 302 = 0.2715.
2. ADC node at 4.2V pack = 1.14V.
3. ADC node at 3.0V pack = 0.81V.
4. Battery reconstruction formula: Vbat = Vadc x ((R2 + R1) / R1) = Vadc x 3.6829.

## 4) Component Value Review (Change / No Change)

No change recommended:

1. R7 = 4.7k (1-Wire weak pull-up).
2. R4 = 1k and R3 = 100k for CE/EN gating.
3. R9 = 100R gate series.
4. R8 = 100k PMOS gate bias.
5. R10 = 330R LED series resistor.
6. C2 = 10uF bulk and C6 = 0.1uF bypass on VCC rail.
7. C3 = 10uF on 3.3V_S rail.

Change recommended:

1. Battery divider should remain R2=220k (high side) and R1=82k (low side).

Review required on your exact board routing:

1. R5=1k (series), R6=1M (to GND), and C4=100nF X7R (test build) define the tilt input behavior.
2. Commissioning RC network is R11=10k and C5=100nF at XPIN20.

### 4.1 Fitted Values Snapshot (Latest SPICE Export)

Test-build override: C4 uses 100nF X7R ceramic for tilt validation.

| Ref | Value |
| --- | --- |
| R1 | 82k |
| R2 | 220k |
| R3 | 100k |
| R4 | 1k |
| R5 | 1k |
| R6 | 1M |
| R7 | 4.7k |
| R8 | 100k |
| R9 | 100 |
| R10 | 330 |
| R11 | 10k |
| C1 | 10uF |
| C2 | 10uF |
| C3 | 10uF |
| C4 | 100nF (X7R) |
| C5 | 100nF |
| C6 | 0.1uF |

## 5) Sleep/Wake and Power Notes

1. XBee must remain continuously powered to preserve sleep/wake behavior.
2. Gating only the sensor rail minimizes sleep current without breaking wake capability.
3. XC6220A CE/EN gating removes the need for an additional regulator load-switch transistor.

## 6) Validation Checklist (Updated)

1. Confirm U1 output remains ~3.3V in sleep and TX bursts.
2. Confirm U2 toggles ON/OFF with XPIN13 transitions.
3. Confirm DS18B20 Convert-T remains CRC OK over repeated cycles.
4. Confirm DQ stays >=3.0V during the 750ms strong pull-up window.
5. Confirm tilt wake/report on both transitions with no false triggers.
6. Confirm XPIN18 battery readings match DMM within expected divider tolerance.
7. Run 24-hour endurance test and capture resets, CRC failures, and missed wake events.

## 7) Source of Truth Location

This updated findings file and the associated wiring docs are maintained in:

- Mech/docs/electrical-wiring-diagrams/xbee_garage_position/

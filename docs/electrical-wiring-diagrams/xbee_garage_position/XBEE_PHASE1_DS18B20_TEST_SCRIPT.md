# XBee Phase 1 DS18B20 Test Script

Date: 2026-04-28

Purpose: Validate that `ds18b20_1_wire` runs on XBee PRO S2B with only the DS18B20 section of the breadboard (power-supply section removed), powered from XBIB-U.

## 1. Scope

This script validates:

1. Hardware wiring integrity.
2. Device detection from XBee firmware.
3. DS18B20 power-mode detection.
4. Stable temperature reads.
5. Basic strong pull-up behavior for parasitic operation.

Not in scope for Phase 1:

1. Zigbee payload integration to Hubitat.
2. Commissioning button logic.
3. Tilt switch logic.
4. Sleep-mode event behavior.

## 2. Hardware Required

1. XBee PRO S2B (Programmable).
2. XBIB-U interface board.
3. PE Micro debugger/programmer.
4. Breadboard DS18B20 section:
   1. DS18B20 sensor.
   2. R2 = 4.7k (DQ pull-up to VCC).
   3. Q1 PMOS strong pull-up path.
   4. R3 = 100 ohm (XPIN7 to gate).
   5. R4 = 100k (gate pull-up to VCC).

## 3. Wiring (Phase 1)

1. XPIN1 (VCC) -> breadboard VCC rail.
2. XPIN10 (GND) -> breadboard GND rail.
3. XPIN4 -> DS18B20 DQ bus.
4. XPIN7 -> PMOS gate path through R3.
5. DS18B20 pin 1 -> GND.
6. DS18B20 pin 2 -> DQ bus.
7. DS18B20 pin 3:
   1. Parasite test: connect to GND.
   2. External-power test: connect to VCC.

Keep disconnected for this phase:

1. Regulator/boost section.
2. Tilt network.
3. Commission input network.
4. External LED network.

## 4. Pre-Power Checks (Multimeter)

Power OFF.

1. VCC to GND: not shorted.
2. DQ to VCC: about 4.7k.
3. XPIN7-to-gate path: about 100 ohm.
4. Gate to VCC: about 100k.
5. DQ to GND: no hard short.

Pass criterion: all 5 checks are within expected range.

## 5. Program and Console Setup

1. Program `CodeWarrior/ds18b20_1_wire` onto XBee.
2. Open serial terminal at 115200.
3. Reset/restart application if needed.

Expected startup behavior:

1. App banner appears.
2. Menu with options includes `S`, `T`, and `P`.

## 6. Functional Test Steps

### Step A: Search Device

1. Press `S`.

Expected:

1. DS18B20 found and ROM printed.

Go/No-Go:

1. GO if ROM is printed.
2. NO-GO if no device found.

### Step B: Check Supply Mode

1. Press `P`.

Expected:

1. If pin 3 tied to GND: reports parasite powered.
2. If pin 3 tied to VCC: reports externally powered.

Go/No-Go:

1. GO if reported mode matches wiring.
2. NO-GO if mismatch.

### Step C: Read Temperature Repeatedly

1. Press `T` once.
2. Press `T` 10 times, about 1 second apart.

Expected:

1. Valid temperature output each read.
2. No repeated communication errors.

Go/No-Go:

1. GO if all reads are valid.
2. NO-GO if frequent read errors occur.

### Step D: Parasitic Stress Quick Check

Prerequisite: DS18B20 pin 3 tied to GND.

1. Press `T` 20 times over about 1 minute.
2. Optionally warm sensor slightly by touch to confirm trend response.

Expected:

1. Reads continue to succeed.
2. Values change smoothly and plausibly.

Go/No-Go:

1. GO if stable read success.
2. NO-GO if intermittent dropouts or stuck values.

## 7. Optional Scope Checks

Probe points:

1. DQ bus.
2. PMOS gate.
3. VCC rail.

Expected:

1. DQ idle near VCC.
2. Gate transitions low during strong pull-up window.
3. VCC remains stable without collapse or large spikes.

## 8. Failure Triage

If `S` fails (no device found):

1. Recheck common ground.
2. Verify DQ is on XPIN4.
3. Verify DS18B20 orientation.
4. Verify R2 value and placement.

If `P` mode is wrong:

1. Recheck DS18B20 pin 3 wiring.

If `T` is intermittent:

1. Inspect R3/R4 and PMOS orientation.
2. Shorten jumper leads.
3. Add local 100 nF decoupling near sensor supply rail.

## 9. Exit Criteria for Phase 1

Phase 1 is complete when all are true:

1. `S` consistently finds DS18B20.
2. `P` matches wiring mode.
3. `T` succeeds repeatedly without errors.
4. No unexplained resets during test run.

After passing, proceed to project copy and Zigbee/Hubitat communication integration phase.

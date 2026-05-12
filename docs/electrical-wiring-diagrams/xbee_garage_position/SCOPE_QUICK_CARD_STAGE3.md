# Scope Quick Card - Stage 3 XBee DS18B20

Use this card at the bench for fast pass/fail checks.

## Probe Setup

- CH1: DQ bus (XPIN11 net)
- CH2: PMOS gate drive (XPIN12 path)
- GND: DUT common ground
- Probe mode: 10x default, 1x only for detailed pulse-shape debug

## Trigger Setup (Primary)

- Type: Edge
- Source: CH1 (DQ)
- Slope: Falling
- Threshold: about 1.2 V (3.3 V logic)
- Coupling: DC
- Holdoff: 900 ms

## Timebase Presets

- Reset/presence detail: 200 us/div
- Bit-slot detail: 10 us/div
- Convert-T behavior window: 100 ms/div
- Fine pulse overview during command slots: 2 ms/div

## What To Trigger In System

1. In Hubitat device page, click Refresh to force poll.
2. Or toggle tilt switch to force immediate report.
3. Watch serial marker lines:
   - FC00 cmd=0x01 (poll) -> queuing temp read
   - FC00 TX: TEMP_C=...,DOOR=...,VBAT_MV=...,BATT_PCT=...

## Pass/Fail Checks

1. DQ idle level: about 3.3 V.
2. PMOS gate goes LOW only during strong pull-up window.
3. DQ remains near rail during strong pull-up window.
4. No repeated FC00 TX failed lines in terminal.
5. Door toggles produce matching door/contact updates in Hubitat.

## Quick Fault Hints

- DQ low or sagging: check R7 4.7k pull-up, PMOS orientation, and 3.3V_S rail.
- Gate never changes: check XPIN12 routing and gate resistor path.
- Poll works but no payload: check FC00 path and endpoint/cluster handling.
- Random transitions: check tilt bias network and grounding noise.

## Capture Record (Fill In)

- Date:
- Firmware build:
- Hubitat driver file/version:
- Scope model:
- Probe attenuation:
- Result: PASS / FAIL
- Notes:

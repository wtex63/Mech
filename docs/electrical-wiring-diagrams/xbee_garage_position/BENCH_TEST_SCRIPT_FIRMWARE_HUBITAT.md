# Bench Test Script: Firmware + Hubitat Validation

## Scope

This script validates the integrated behavior of:

1. XBee firmware in CodeWarrior ds18b20_hubitat_temp
2. Hubitat driver XBee_Garage_Door_Sensor.groovy
3. Current wiring/pin map (XPIN7 tilt, XPIN11 DS18B20 DQ, XPIN12 strong pull-up gate)

Use this after Stage 3 wiring checks and before PCB commit.

## Preconditions

- Breadboard wiring matches HARDWARE_WIRING.md and current IPC/SPICE values.
- Firmware flashed from CodeWarrior/ds18b20_hubitat_temp.
- XBee is paired to Hubitat and the custom driver is selected.
- Hubitat device settings:
  - Enable debug logging = true
  - Enable description text logging = true
  - reportingInterval = 300 (or your chosen value)
- Terminal connected to XBee serial console at 115200.
- DMM available for battery measurement cross-check.

## Expected Payload Formats

Firmware sends FC00 payloads as comma-separated UTF-8 text:

1. Temperature report:
TEMP_C=nn.nn,DOOR=open|closed,VBAT_MV=mmmm,BATT_PCT=pp
2. Door-only report:
DOOR=open|closed,VBAT_MV=mmmm,BATT_PCT=pp

Hubitat should decode and create events for:

1. door
2. contact
3. temperature and temperatureC
4. batteryVoltage
5. battery

## Test Script

### Step 1: Driver Configure Handshake

Action:

1. In Hubitat device page, click Configure.

Expected Hubitat behavior:

1. Driver sends FC00 cmd 0x02 (set interval) and FC00 cmd 0x01 (poll).
2. Debug log includes setIntervalCommands with a 2-byte big-endian payload.

Expected firmware console:

1. FC00 cmd=0x02: interval set to N s
2. FC00 cmd=0x01 (poll) -> queuing temp read
3. FC00 TX: TEMP_C=...,DOOR=...,VBAT_MV=...,BATT_PCT=...

Pass criteria:

1. Interval set message appears once after Configure.
2. Poll response appears within a few seconds.

### Step 2: Baseline Telemetry Sanity

Action:

1. Let the node idle for one report cycle or click Refresh.
2. Note VBAT_MV from payload and batteryVoltage in Hubitat.
3. Measure battery/input rail with DMM at the divider source.

Expected:

1. Hubitat lastPayload contains TEMP_C, DOOR, VBAT_MV, BATT_PCT.
2. Hubitat batteryVoltage equals VBAT_MV/1000 to 3 decimals.
3. Firmware and Hubitat battery percent remain in 0-100 range.
4. DMM and VBAT_MV are reasonably close for a breadboard setup.

Pass criteria:

1. No impossible values (negative mV, >5000 mV, >100%).
2. Hubitat values track firmware payload values.

### Step 3: Door Transition Test (XPIN7)

Action:

1. Toggle the tilt switch to force OPEN.
2. Toggle back to force CLOSED.
3. Repeat 5 cycles with 2-3 seconds between transitions.

Expected firmware console on each transition:

1. [DOOR] open or [DOOR] closed
2. FC00 door TX: DOOR=open|closed,VBAT_MV=...,BATT_PCT=...

Expected Hubitat:

1. door attribute follows state.
2. contact attribute mirrors door (open/open, closed/closed).
3. No duplicate storms while input is stable.

Pass criteria:

1. 10 commanded transitions produce 10 matching contact updates.
2. No stuck state after final toggle.

### Step 4: Poll/ACK Path Verification

Action:

1. Click Refresh in Hubitat three times, spaced by 3-5 seconds.

Expected firmware console:

1. For each refresh: FC00 cmd=0x01 (poll) -> queuing temp read
2. Followed by FC00 TX: TEMP_C=...,DOOR=...,VBAT_MV=...,BATT_PCT=...
3. Optionally: FC00 cmd=0x00 (ack/nack) len=...

Expected Hubitat:

1. Decoded payload log line for each returned report.
2. lastPayload updates each cycle.

Pass criteria:

1. 3 poll requests produce 3 valid payload parses.
2. No FC00 TX failed messages.

### Step 5: Reporting Interval Clamp Test

Action:

1. In Hubitat, set reportingInterval to 30 and click Configure.
2. Then set reportingInterval to 7200 and click Configure.
3. Finally set reportingInterval to 300 and click Configure.

Expected firmware console:

1. First configure clamps to 60 s: FC00 cmd=0x02: interval set to 60 s
2. Second configure clamps to 3600 s: FC00 cmd=0x02: interval set to 3600 s
3. Third configure sets to 300 s

Expected Hubitat debug:

1. setIntervalCommands logs payloads corresponding to requested values.

Pass criteria:

1. Firmware clamp behavior is correct and deterministic.

### Step 6: Temperature Path Validation

Action:

1. Warm the DS18B20 sensor slightly (finger touch) for 30-60 s.
2. Remove heat and observe recovery.

Expected firmware/Hubitat:

1. TEMP_C changes in payload.
2. Hubitat temperatureC tracks with 2 decimal precision.
3. Hubitat temperature (location unit) updates accordingly.

Pass criteria:

1. Temperature trend direction is correct during warm-up and cool-down.
2. No parse failures for TEMP_C values.

### Step 7: Fault-Visibility Spot Check

Action:

1. Briefly disconnect DS18B20 DQ (XPIN11) and then restore.

Expected firmware diagnostics (if triggered during sample window):

1. Startup/diagnostic warnings referencing XPIN11 and pull-up checks.

Expected Hubitat:

1. Temporary stale temperature is acceptable during fault window.
2. Normal updates resume after reconnection.

Pass criteria:

1. Recovery occurs without reboot.

## Quick Failure Triage

If door updates fail but temperature works:

1. Check XPIN7 wiring and tilt switch bias network.
2. Confirm no unintended pull conflict on tilt line.

If temperature fails but door works:

1. Check XPIN11 DQ continuity.
2. Check 4.7k pull-up to 3.3V_S.
3. Check XPIN12 MOSFET gate path and DS18B20 power wiring.

If battery readings are implausible:

1. Verify divider values are 220k and 82k in hardware.
2. Compare DMM reading to VBAT_MV payload.

If polls fail:

1. Confirm FC00 cluster traffic is enabled in the driver.
2. Look for FC00 TX failed lines in firmware console.

## Sign-Off Checklist

Mark pass only when all are true:

1. Configure sends interval and poll, firmware acknowledges both.
2. Door state changes are correct and stable for repeated cycles.
3. TEMP_C reports parse cleanly in Hubitat.
4. VBAT_MV and batteryVoltage are plausible and correlated with DMM.
5. No recurring FC00 TX failed or unhandled-cmd noise in normal operation.

## Suggested Run Log Template

Date:

Firmware build ID:

Driver version/file:

1. Configure handshake: PASS/FAIL

Notes:

1. Baseline telemetry: PASS/FAIL

Notes:

1. Door transition cycles: PASS/FAIL

Notes:

1. Poll/ACK path: PASS/FAIL

Notes:

1. Interval clamp: PASS/FAIL

Notes:

1. Temperature trend: PASS/FAIL

Notes:

1. Fault recovery: PASS/FAIL

Notes:

Overall sign-off: PASS/FAIL

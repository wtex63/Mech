# Three-Stage Breadboard Test Procedure

This document defines the bench test plan for the Door Position Sensor design before PCB layout. It is written around the current Arduino Uno harness in [Test_D18B20.ino](c:/Users/wtex6/source/repos/wtex63/Arduino/Test_D18B20/Test_D18B20.ino) and the schematic image reviewed in this chat.

## Scope

Three stages will be tested:

1. Stage 1: sensor, strong pull-up, LED, and button functions with the Arduino Uno, but without the regulator/power section and without the XBee.
2. Stage 2: regulator/power section added, still no XBee, with the Uno controlling the logic test.
3. Stage 3: full breadboard design with the regulator and XBee present, with the Uno no longer driving XBee-controlled nets.

## Design Summary

Key schematic intent from the reviewed image:

1. DS18B20 is in parasite-power mode.
2. Q1 is a P-channel high-side MOSFET used as a strong pull-up for the 1-Wire bus.
3. R2 is the normal 1-Wire pull-up from DQ to VCC.
4. R3 is the gate series resistor.
5. R4 is the gate pull-up that keeps Q1 off by default.
6. R5 and C3 form the tilt input bias/filter network.
7. R1 and D1 are the indicator LED path.

## Recommended Resistor Values

### Final Low-Power PCB Values

Use these values for the final battery-powered design.

| Ref | Function | Value |
|---|---|---:|
| R1 | LED series resistor | 220 ohm |
| R2 | DS18B20 DQ pull-up | 4.7k ohm |
| R3 | MOSFET gate series resistor | 100 ohm |
| R4 | MOSFET gate pull-up to VCC | 100k ohm |
| R5 | Tilt input bias/filter resistor | 1M ohm |

Notes:

1. Do not keep R1 at 50 ohm.
2. R5 at 1M ohm is acceptable for the final low-power PCB and keeps current near 3.3 microamps at 3.3V.
3. C3 at 100nF with R5 at 1M ohm gives a time constant of about 100 ms.

### Recommended Temporary Breadboard-Test Values

Use these values while proving the design on a breadboard.

| Ref | Function | Value |
|---|---|---:|
| R1 | LED series resistor | 220 ohm |
| R2 | DS18B20 DQ pull-up | 4.7k ohm |
| R3 | MOSFET gate series resistor | 100 ohm |
| R4 | MOSFET gate pull-up to VCC | 100k ohm |
| R5 | Tilt input bias/filter resistor | 100k ohm |

Reason for the temporary change:

1. A breadboard is noisier and leakier than the final PCB.
2. R5 at 100k ohm is much more forgiving during bench validation.
3. Once the design is proven, R5 can be returned to 1M ohm to match the final battery design.

## General Bench Rules

1. The Uno is a 5V board. Its digital outputs must not directly drive XBee 3.3V pins in the final-stage test.
2. The Stage 1 and Stage 2 logic tests are acceptable only because the XBee is not connected.
3. Use a common ground between the Uno, the bench supply, and the DUT in every stage.
4. When the regulator section is active, prefer a bench supply with current limit.
5. If powering the DUT from the Uno 3.3V pin, keep the total current low.
6. Use a short oscilloscope ground spring if possible when probing the regulator and the 1-Wire bus.

## Stage 1

### Goal

Verify the DS18B20 parasite-power bus, strong pull-up MOSFET, tilt button function, commission button function, and LED behavior without the regulator/power section and without the XBee.

### Excluded Parts

Do not connect:

1. G1
2. C1
3. C2
4. L1
5. J1 / XC9140 power section
6. XBee module

### Stage 1 Wiring

Power the DUT logic rail from the Uno 3.3V pin or from an external 3.3V bench supply.

Recommended wiring:

| Uno / Supply | DUT Net / Part | Notes |
|---|---|---|
| Uno 3.3V or external 3.3V | VCC | Logic rail for Stage 1 |
| Uno GND | GND | Common ground |
| Uno D2 | DS18B20 DQ bus | Matches XPIN11 role in the XBee design |
| Uno D3 | Q1 gate drive through R3 | Matches XPIN12 strong pull-up gate role in the XBee design, active low |
| Push button to GND | Tilt input net | Simulates S1 tilt switch |
| Push button to GND | Commission input net | Simulates S2 commissioning button |
| Uno D6 through R1 to LED anode, LED cathode to GND | Indicator path | Use 220 ohm series resistor |

If you are using the current Uno sketch directly:

1. Uno D2 is the 1-Wire DQ controller.
2. Uno D3 drives the MOSFET gate.
3. Uno D4 is the tilt simulation button input.
4. Uno D5 is the commission button input.
5. Uno D6 drives the external association LED for the blink test.
6. Use `x` in the serial monitor to enable parasitic conversion mode in the sketch.

Important for parasitic-mode validation:

1. Do not hard-tie Uno D3 to VCC or GND during runtime testing.
2. Uno D3 must only drive the Q1 gate through R3 so the sketch can switch the strong pull-up window correctly.

### Stage 1 Pre-Power VMM Checklist

Power off. Measure these before connecting power.

| Test Point | Expected Result |
|---|---|
| VCC to GND | Not a short |
| DQ to VCC | About 4.7k ohm |
| Q1 gate to VCC | About 100k ohm |
| Gate drive node to gate | About 100 ohm |
| Tilt input to bias rail | About 100k ohm for breadboard test |
| LED series resistor | 220 ohm |
| DS18B20 VDD to GND | Continuity present |
| DQ to GND | No hard short |
| VCC to DQ through Q1 | No direct short |

### Stage 1 Power-Up VMM Checks

| Test Point | Expected Value |
|---|---|
| VCC | About 3.3V |
| DQ idle | About 3.3V |
| Q1 gate idle | About 3.3V |
| Q1 gate during strong pull-up | Near 0V while asserted |
| LED output when idle | Off unless explicitly commanded |

### Stage 1 Scope Procedure

Probe these points:

1. DQ bus
2. Q1 gate
3. VCC

Procedure:

1. Power the Stage 1 circuit at 3.3V.
2. Open the serial monitor at 115200.
3. Send `s` and verify device scan finds the DS18B20.
4. Probe DQ and send `c`.
5. Verify reset and presence pulses on DQ.
6. Send `x` once so parasitic conversion mode is enabled.
7. During Convert T, verify the gate goes low.
8. During that same window, verify DQ stays very near VCC.
9. After conversion, verify the gate returns high and DQ remains high through R2.
10. Press the commission button and verify the LED blinks 5 times.
11. Press the tilt button and verify the serial output toggles between OPEN and CLOSED.

### Stage 1 Pass Criteria

1. DS18B20 is detected.
2. Scratchpad reads return CRC OK.
3. DQ does not sag badly during the strong pull-up window.
4. Q1 gate is controlled by Uno D3 and is not hard-wired to a rail.
5. Commission button produces 5 LED blinks.
6. Tilt button toggles state reliably.

## Stage 2

### Goal

Verify the regulator/power section first, then repeat the Stage 1 functional checks while the DUT is powered through the regulator, still without the XBee.

### Stage 2 Wiring

Add the power section back in:

1. G1 input source
2. C1
3. L1
4. J1 / XC9140 regulator
5. C2

Keep the XBee disconnected.

Use the Uno only for logic/test control.

| Connection | Notes |
|---|---|
| Bench supply positive | G1 input node |
| Bench supply ground | GND |
| Regulator VOUT | VCC logic rail |
| Uno GND | Common ground with DUT |
| Uno D2 | DQ bus |
| Uno D3 | Q1 gate drive through R3 |
| Uno D4 | Tilt button input if using sketch-driven button simulation |
| Uno D5 | Commission button input if using sketch-driven button simulation |

Do not feed the DUT VCC from the Uno 3.3V pin in Stage 2. The regulator under test must power VCC.

### Stage 2 Pre-Power VMM Checklist

Power off.

| Test Point | Expected Result |
|---|---|
| Input rail to GND | Not a short |
| VCC to GND | Not a short |
| C1 across input rail | Installed correctly |
| C2 across VCC and GND | Installed correctly |
| L1 continuity | Present |
| DQ to VCC | About 4.7k ohm |
| Gate to VCC | About 100k ohm |

### Stage 2 Power-Up VMM Procedure

1. Set the bench supply current limit low first, for example 30 mA to 50 mA.
2. Apply the intended input voltage to G1.
3. Measure regulator output VCC.
4. If VCC is correct, increase the current limit as needed.
5. Repeat the Stage 1 VMM checks at DQ and the gate.

Expected values:

| Test Point | Expected Value |
|---|---|
| Regulator input | Applied source voltage |
| VCC | About 3.3V |
| DQ idle | About 3.3V |
| Q1 gate idle | About 3.3V |

### Stage 2 Scope Procedure

Probe these points:

1. Regulator output VCC
2. LX switch node on the XC9140 section
3. DQ bus
4. Q1 gate

Procedure:

1. Probe VCC during power-up and verify a clean ramp to about 3.3V.
2. Probe LX and verify switching activity exists.
3. Probe VCC ripple at no load.
4. Add a light load if needed, for example 330 ohm from VCC to GND, and recheck VCC ripple.
5. Once the regulator is stable, run the Stage 1 DQ and gate tests again.

Expected observations:

| Point | Expected Observation |
|---|---|
| VCC startup | Clean rise to about 3.3V |
| LX | Switching pulses present |
| VCC ripple | Modest ripple, not unstable burst collapse |
| DQ during Convert T | Near VCC |
| Gate during Convert T | Low while strong pull-up active |

### Stage 2 Pass Criteria

1. Regulator starts cleanly.
2. VCC regulates near 3.3V.
3. No excessive ripple or collapse under a light load.
4. DS18B20 still reads correctly with CRC OK.
5. Button and LED functions still work.

## Stage 3

### Goal

Test the complete breadboard design with regulator and XBee present.

### Critical Rule For Stage 3

Do not let the Uno drive any XBee-controlled net directly.

That means:

1. Do not connect Uno D2 to the DQ net when the XBee is connected and expected to own that net.
2. Do not connect Uno D3 to the MOSFET gate drive net when the XBee is connected and expected to own that net.
3. Do not connect any Uno 5V digital output directly to XBee pins.

In Stage 3, the Uno should be used only if it is electrically isolated from the XBee logic domain. The safer approach is:

1. Use physical push buttons on the breadboard for tilt and commission.
2. Let the XBee control DQ and the MOSFET gate.
3. Use the scope and VMM for observation.
4. If the Uno must stay present, connect only common ground unless you add proper level shifting or high-value monitoring resistors.

### Stage 3 Wiring

| Connection | Notes |
|---|---|
| Bench supply positive | G1 input node |
| Bench supply ground | GND |
| Regulator output VCC | XBee VCC, DQ pull-up, and all logic rails |
| XBee DIO4 / XPIN11 equivalent | DQ bus |
| XBee DIO3 / XPIN12 equivalent | Q1 gate through R3 |
| Tilt switch | Actual tilt input net |
| Commission switch | Actual commission input net |
| LED path | Actual indicator output net with 220 ohm |
| Uno GND only, optional | Common reference only unless level shifting is used |

### Stage 3 Pre-Power VMM Checklist

| Test Point | Expected Result |
|---|---|
| Input rail to GND | Not a short |
| VCC to GND | Not a short |
| XBee VCC to GND | Not a short |
| DQ to VCC | About 4.7k ohm |
| Q1 gate to VCC | About 100k ohm |
| LED series resistor | 220 ohm |
| Tilt bias resistor | 1M ohm for final design |

### Stage 3 Power-Up VMM Procedure

1. Apply input supply with current limit enabled.
2. Verify VCC is about 3.3V before inserting or enabling the XBee.
3. Verify the XBee sees a valid 3.3V rail.
4. Check idle DQ and gate voltages.
5. Exercise the tilt and commission buttons.

Expected values:

| Test Point | Expected Value |
|---|---|
| VCC | About 3.3V |
| XBee VCC | About 3.3V |
| DQ idle | About 3.3V |
| Gate idle | About 3.3V |

### Stage 3 Scope Procedure

Probe these points:

1. VCC
2. DQ
3. Q1 gate
4. Optional: XBee-controlled button nets

Procedure:

1. Verify regulator startup and ripple again with the XBee fitted.
2. Observe DQ and gate during an XBee-driven temperature conversion.
3. Verify the gate goes low only during the strong pull-up interval.
4. Verify DQ stays near VCC during that same interval.
5. Exercise the commission button and confirm the LED behavior expected by the XBee firmware.
6. Exercise the tilt switch and verify the XBee firmware sees the transition.

### Stage 3 Pass Criteria

1. Regulator remains stable with the XBee fitted.
2. XBee powers up correctly at 3.3V.
3. DQ and gate timing match the intended strong pull-up behavior.
4. LED function is correct with the actual XBee-controlled output.
5. Tilt and commission inputs behave correctly with the actual XBee firmware.

### Stage 3 Firmware And Hubitat Quick Run (Condensed)

Use this as the execution checklist during first integrated bring-up.
For full detail and run logging, use [Mech/docs/electrical-wiring-diagrams/xbee_garage_position/BENCH_TEST_SCRIPT_FIRMWARE_HUBITAT.md](Mech/docs/electrical-wiring-diagrams/xbee_garage_position/BENCH_TEST_SCRIPT_FIRMWARE_HUBITAT.md).

1. Click Configure on the Hubitat device.
2. Confirm firmware console shows interval set and poll queued on FC00.
3. Confirm a valid FC00 payload arrives with TEMP_C, DOOR, VBAT_MV, and BATT_PCT.
4. Toggle tilt switch open then closed for five cycles.
5. Confirm Hubitat contact and door events match every transition.
6. Click Refresh three times and confirm three valid poll responses.
7. Warm DS18B20 briefly and confirm temperature trend updates in Hubitat.

Quick pass conditions:

1. No repeated FC00 TX failure lines.
2. No stuck door state after toggle sequence.
3. Battery values are plausible and correlate with DMM reading.
4. Poll, parse, and event update path is stable across repeated refresh.

## Test Points Summary

Use these names consistently during all three stages.

| Test Point | Description | Expected Idle Value |
|---|---|---|
| TP_IN | Raw input supply at G1 | Applied source voltage |
| TP_VCC | Regulated logic rail | About 3.3V |
| TP_DQ | DS18B20 1-Wire bus | About 3.3V |
| TP_GATE | Q1 gate | About 3.3V when idle |
| TP_LX | XC9140 switch node | Pulsing waveform when regulator active |
| TP_TILT | Tilt input node | Defined high or low, not floating |
| TP_COMM | Commission input node | Defined high or low, not floating |
| TP_LED | LED drive node | Depends on output state |

## Suggested Bench Equipment Settings

1. Bench supply current limit for first power-up: 30 mA to 50 mA.
2. Scope vertical scale for VCC: start at 1 V/div.
3. Scope vertical scale for DQ and gate: start at 1 V/div.
4. Scope time base for regulator startup: start at 1 ms/div.
5. Scope time base for 1-Wire bus: start at 50 us/div, then widen for the Convert T window.

## Known Risks To Watch During Testing

1. R1 at 50 ohm will overdrive the LED current. Change it before testing.
2. The Uno is a 5V board. Do not use it to drive XBee pins in Stage 3.
3. Breadboard leakage can make the final 1M tilt bias look worse than it will on a PCB.
4. If DQ sits well below VCC during strong pull-up, suspect MOSFET pinout or orientation mismatch.
5. If VCC ripples heavily or collapses, debug the XC9140 section before continuing.

## Stage Completion Record

| Stage | Completed | Notes |
|---|---|---|
| Stage 1 | [ ] | |
| Stage 2 | [ ] | |
| Stage 3 | [ ] | |

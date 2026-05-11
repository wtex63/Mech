# XBee Garage Door Sensor — Complete Hardware Wiring

Date: 2026-05-07
Board: XBee ZB (S2B) Programmable
Power: 2xAA alkaline in series (~3.0V fresh, ~2.4V end-of-life)

---

## 1. XBee Pin Assignment Summary

```text
              _________________
             /     ________    \
            /     |   __   |    \
           /      | //  \\ |     \
  XPIN1  -|       | \\__// |      |- XPIN20  Commission button input
  XPIN2  -|       |________|      |- XPIN19  (unused)
  XPIN3  -|     J1: diag header    |- XPIN18  Battery voltage ADC input
  XPIN4  -|                       |- XPIN17  (unused)
  XPIN5  -|                       |- XPIN16  (unused)
  XPIN6  -|                       |- XPIN15  Status LED output
  XPIN7  -|                       |- XPIN14  VCC REF
  XPIN8  -|                       |- XPIN13  On/Sleep output  --> XC9140 CE gate
  XPIN9  -|                       |- XPIN12  (unused)
  XPIN10 -|_______________________|- XPIN11  Door tilt IRQ input

Pin functions:
  XPIN1  = VCC (3.3V always-on from MCP1700)
  XPIN2  = UART TX → J1 pin 1 (diagnostic header, 3.3V logic out)
  XPIN3  = UART RX ← J1 pin 2 (diagnostic header, 3.3V logic in)
  XPIN4  = DS18B20 DQ (1-Wire data bus)
  XPIN5  = Reset (leave unconnected)
  XPIN6  = RSSI PWM (internal, leave unconnected)
  XPIN7  = DS18B20 strong pull-up drive (MOSFET gate, firmware-controlled)
  XPIN8  = BKGD / debug (leave unconnected)
  XPIN9  = Sleep Request output (firmware-controlled, leave unconnected externally)
  XPIN10 = GND
  XPIN11 = Door tilt switch IRQ input (pull-up topology, both-edge wake)
  XPIN12 = (unused)
  XPIN13 = On/Sleep status output  --> drives XC9140 CE gate
  XPIN14 = VCC REF (tie to 3.3V)
  XPIN15 = Status LED output (active HIGH)
  XPIN16 = (unused)
  XPIN17 = (unused)
  XPIN18 = battery voltage sensing (ADC2 input, 1:1 divider from 2xAA)
  XPIN19 = (unused)
  XPIN20 = Commissioning button input (active LOW, internal pull-up)
```

---

## 2. Power Supply

Two independent regulated rails from a single 2xAA battery pack.

### 2.1 Always-On Rail (XBee power)

XBee must never lose power, including during sleep. The MCP1700 LDO draws only 1.6 µA quiescent.

```text
2xAA(+) -------+---> MCP1700-3302 (U1)
               |       PIN2: VIN <--- 2xAA(+)
               |       PIN1: GND <--- common GND
               |       PIN3: VOUT ---> 3.3V_A rail
               |
               +--> (C4 on shared battery rail — see Section 2.2)

               3.3V_A (always-on):
                    |
                    +---> [C2: 0.1µF ceramic] ---> GND   (place at XBee VCC pin)
                    +---> [C3: 10µF ceramic X7R] -> GND  (bulk on LDO output)
                    +---> XBee XPIN1 (VCC)
                    +---> XBee XPIN14 (VCC REF)

MCP1700-3302 pinout (TO-92, flat face toward you):
  PIN1 (left)   = GND
  PIN2 (center) = VIN
  PIN3 (right)  = VOUT
```

### 2.2 Gated Sensor Rail (DS18B20 strong pull-up supply)

The XC9140 boost is enabled only when XBee is awake (XPIN13 HIGH). During XBee sleep, the DS18B20 strong pull-up rail is off.

**IMPORTANT — Protoboard modification required:**
The CE pin on your XC9140 protoboard is factory-tied to VIN. Cut or lift this trace/wire before connecting.

```text
2xAA(+) -------+--------> XC9140 (U2) VIN
               |               GND <------------- Common GND
               |               CE  <---+--------- [R4: 1k] <--- XBee XPIN13
               |                       |
               |                      [R3: 100k]
               |                       |
               |                      GND
               |
               |           [C4: 4.7µF ceramic X7R] between VIN and GND (at U2)
               |
               +---> XC9140 VOUT ---> 3.3V_S rail

               3.3V_S (gated sensor rail):
                    |
                    +---> [C5: 10µF ceramic X7R] ---> GND  (at VOUT)
                    +---> PMOSFET source (strong pull-up supply)

CE gate behavior:
  XBee awake  -> XPIN13 = HIGH -> CE pulled HIGH via R4 -> XC9140 ON  -> 3.3V_S active
  XBee asleep -> XPIN13 = LOW  -> R3 pulls CE LOW       -> XC9140 OFF -> 3.3V_S = 0V
```

### 2.3 Common Ground

All grounds are the same node. Do not split grounds.

```text
2xAA(-) ----------> Common GND

Connected to GND:
  MCP1700 PIN1
  XC9140 GND
  XBee XPIN10
  DS18B20 GND
  R3 lower end (CE pull-down)
  R5 lower end (XPIN11 pull-down)
  C2 lower end
  C3 lower end
  C4 lower end
  C5 lower end
  C6 lower end
  LED cathode resistor lower end
```

---

## 3. Temperature Sensor (DS18B20) — Parasitic Power Mode

DS18B20 is wired in parasitic mode: VDD pin tied to GND. The sensor draws
its operating power from the DQ line. A P-channel MOSFET controlled by
XPIN7 provides the high-current strong pull-up during the 750ms conversion
window. This is mandatory in parasitic mode — the 4.7k resistor alone cannot
supply enough current for a reliable conversion.

```text
DS18B20 TO-92 pinout (flat face toward you):
  PIN1 (left)   = GND
  PIN2 (center) = DQ
  PIN3 (right)  = VDD  <-- tied to GND in parasitic mode

Parasitic wiring:
  DS18B20 PIN3 (VDD) ----> GND   (parasitic mode: VDD shorted to GND)
  DS18B20 PIN1 (GND) ----> GND
  DS18B20 PIN2 (DQ)  <---> DQ net

1-Wire idle pull-up (weak):
  3.3V_A ----[R1: 4.7k]----+----> DQ net ----> XBee XPIN4
                           |                   DS18B20 PIN2

Strong pull-up circuit (PMOSFET on XPIN7):

  XPIN7 ----[R7: 180Ω]----+----> PMOSFET Gate   (point A)
                           |
                          [R8: 100k]
                           |
                          GND

  3.3V_S ---------> PMOSFET Source
  PMOSFET Drain ---> DQ net
  PMOSFET Gate  <--- point A (via R7 from XPIN7, with R8 pull-down to GND)

  R7 (180Ω): Limits transient gate current and damps gate oscillation.
  R8 (100k): Holds gate at GND when XPIN7 is high-impedance (XBee boot/reset).
             Without R8 the PMOSFET can turn on unintentionally at power-up.

  Operation:
    XPIN7 LOW  (firmware asserts LOW) -> Gate pulled low through R7, R8 to GND
                                      -> Vgs = -3.3V -> PMOSFET ON
                                      -> 3.3V_S drives DQ directly
                                      -> DS18B20 draws conversion current (~1mA)
    XPIN7 HIGH (idle/default)         -> Gate = 3.3V via R7 -> Vgs = 0V -> PMOSFET OFF
                                      -> R8 path negligible (XPIN7 wins)
                                      -> only R1 4.7k pull-up active on DQ
    XPIN7 high-Z (boot/reset)         -> R8 pulls gate to GND -> Vgs = 0V -> PMOSFET OFF
                                      -> safe default, no unintended DQ drive

Note: R1 (4.7k) pull-up connects to 3.3V_A (always-on) so the DQ line is
always properly biased even when 3.3V_S is gated off during XBee sleep.
```

---

## 4. Battery Voltage Sensing (ADC)

The XBee is isolated from the raw battery by the MCP1700 regulator, so `%V` cannot measure
true battery depletion. This circuit uses an ADC pin to directly sense the raw 2xAA voltage.

```text
Raw Battery Voltage Divider (XPIN18 / ADC2):

2xAA(+) ----[R10: 100k]----+----[R11: 100k]----+----> GND
                            |
                        XBee XPIN18 (ADC2 input)

Operating range:
  Battery 3.0V fresh  → Divider output = 1.5V  (100% capacity)
  Battery 2.4V EOL    → Divider output = 1.2V  (0% capacity)
  
  XBee ADC resolution: 10-bit (0–1024) with ~3.2mV/step
  Sensed voltage range: 1.2V–1.5V → ADC 375–469 counts (good resolution)

Resistor rationale:
  R10 + R11 = 200k total = minimal drain from battery (~15µA at 3V)
  1:1 divider = simple, symmetric, stable with component tolerances
  Both 1% tolerance recommended for accurate battery tracking

Connection:
  R10 high end  ← 2xAA(+)  (raw battery, before regulator)
  R10/R11 node ← XBee XPIN18 (ADC2)
  R11 low end  ← GND (common ground)

Firmware:
  Read XPIN18 via AT command ADC2 (or DIO2/ADC2 in XBee API)
  Scaling: ADC count → voltage → percent
  Linear mapping: 1.2V (2400mV) = 0%, 1.5V (3000mV) = 100%
  Internal calculation already in battery_percent_from_mv()
```

---

## 5. Door Tilt Switch

Pull-up topology: switch connects 3.3V_A to XPIN11 when door changes state.
When switch is open, R5 holds XPIN11 LOW.
When switch is closed, pin is pulled HIGH through R2.

```text
3.3V_A ----> [S1: Tilt switch] ----> [R2: 1k] ---+---> XBee XPIN11
                                                  |
                                                  +---> [C6: 100µF EMVE160ARA101MF55G] --> GND
                                                  |
                                                 [R5: 1M]
                                                  |
                                                 GND

IRQ edge:   Both edges (LOW->HIGH and HIGH->LOW, re-armed dynamically)
Firmware:   `DOOR_TILT_ACTIVE_LOW` must match your physical switch orientation
            Internal XPIN11 pull-up is DISABLED (R5 external pull-down handles resting state)
            IRQ dynamically re-armed to opposite edge after each event

Debounce:   C6 (100µF EMVE160ARA101MF55G electrolytic) with R2 (1k) gives RC = 100ms.
            This restores the original debounce window. Single compact 5x5.5mm component.
Series R2:  Limits current into XPIN11 and forms RC with C6.
R5 (1M):    Holds XPIN11 LOW when switch is open. High value minimises static drain
            from the always-on 3.3V_A rail.
```

---

## 6. Status LED

LED indicates network state: commissioning blink, joined heartbeat, disassociated fast blink.

```text
XBee XPIN15 ----> [R6: 330Ω] ----> LED anode
                                   LED cathode ----> GND

LED behavior (firmware-controlled):
  Commissioning / searching : double-blink every 1.2 s
  Joined / normal operation : short pulse every 2 s
  Disassociated             : fast 50% blink for 10 s, then returns to commissioning
  TX activity overlay       : LED forced ON for 120 ms after each transmission

R6 value: 330Ω gives ~8 mA at 3.3V with a red LED (Vf ~0.6V).
          Adjust for other LED colors (green ~2.1V forward: use 100-150Ω).
Note: LED draws current only when on. During sleep XPIN15 is low,
      no current flows through LED circuit.
```

---

## 7. Commissioning Button

Built-in function on XPIN20. Single press sends Node ID broadcast.
Hold ~8 seconds to force leave/rejoin the Zigbee network.

```text
XBee XPIN20 ----> [Pushbutton S2] ----> GND

Internal pull-up enabled on XPIN20 (firmware default).

Optional hardware debounce (recommended if false-triggers observed):

  XPIN20 ----> [R9: 10k] ---+----> [Pushbutton S2] ----> GND
                            |
                          [C7: 100nF]
                            |
                           GND

  R9 + C7 give RC = 1ms, which is enough to suppress contact bounce
  on a standard tactile switch without slowing the intentional press.
  R9 also current-limits XPIN20 if the pin is ever driven accidentally.
  Without R9/C7 the firmware relies solely on software debounce timing.
```

---

## 8. Diagnostic UART Header (J1)

A 3-pin 0.1" male header populated on the breadboard/PCB allows a CP2102
USB-to-serial adapter to be temporarily connected for live diagnostic output
without disturbing any other wiring. Disconnect J1 before field deployment.

```text
XBee XPIN2 (TX) ----> J1 pin 1   (signal label: DIAG_TX)
XBee XPIN3 (RX) ----> J1 pin 2   (signal label: DIAG_RX)
Common GND      ----> J1 pin 3   (signal label: GND)

Logic level : 3.3V TTL — verify CP2102 board is set to 3.3V before connecting
Baud rate   : 115200  8N1  no flow control
Do NOT connect CP2102 VCC to any circuit rail.
```

J1 connector placement: next to XBee module, accessible from board edge.

---

## 9. Complete Net List

| Net | Connects |
| --- | --- |
| 2xAA(+) | B1(+), U1 VIN, U2 VIN, C4(+), R10 high end |
| 2xAA(-) / GND | B1(-), U1 GND, U2 GND, XPIN10, DS18B20 PIN1 (GND), DS18B20 PIN3 (VDD — parasitic tie), C2(-), C3(-), C4(-), C5(-), C6(-), R3 low, R5 low, R8 low, R11 low, LED cathode resistor low, J1 pin 3 (DIAG_GND) |
| 3.3V_A | U1 VOUT, C2(+), C3(+), XPIN1 (VCC), XPIN14 (VREF), R1 high end, S1 supply terminal |
| 3.3V_S | U2 VOUT, C5(+), PMOSFET source |
| DQ | DS18B20 PIN2, R1 low end, XPIN4, PMOSFET drain |
| XPIN7 | R7 high end (180Ω series gate resistor) |
| XPIN11 | R2 output, R5 high end, C6 high end |
| XPIN2 | J1 pin 1 (DIAG_TX) |
| XPIN3 | J1 pin 2 (DIAG_RX) |
| GND | J1 pin 3 (DIAG_GND) |
| XPIN13 | R4 high end |
| XPIN15 | R6 high end (LED series resistor) |
| XPIN20 | R9 high end (optional debounce), S2 commissioning button |
| XPIN18 | R10/R11 divider node (battery voltage sensing ADC input) |
| CE | R3 high end, R4 low end, U2 CE pin |
| S1_out | S1 output terminal, R2 high end |
| GATE_A | R7 low end, R8 high end, PMOSFET gate (point A) |
| BATT_DIV | R10 low end, R11 high end (divider node, to XPIN18) |

---

## 10. Component Values and Placement

### Resistors

| Resistor | Value | Purpose | Tolerance |
| --- | --- | --- | --- |
| R1 | 4.7k | DQ weak pull-up (1-Wire) | 5% |
| R2 | 1k | Tilt switch pull-up series / RC time constant | 5% |
| R3 | 100k | XC9140 CE pull-down to GND (disabled state) | 5% |
| R4 | 1k | XBee XPIN13 to XC9140 CE gate resistor | 5% |
| R5 | 1M | Tilt switch pull-down to GND (resting state) | 5% |
| R6 | 330Ω | LED series current limiting | 5% |
| R7 | 180Ω | PMOSFET gate series (damp transients) | 5% |
| R8 | 100k | PMOSFET gate pull-down (safe default at boot) | 5% |
| R9 | 10k | Commissioning button debounce (optional) | 5% |
| R10 | 100k | Battery divider high side (1:1 ratio) | **1%** |
| R11 | 100k | Battery divider low side (1:1 ratio) | **1%** |

**Battery divider (R10/R11):** Use 1% tolerance for consistent voltage measurement across units.
R10 + R11 = 200k total = ~15µA quiescent drain from always-on battery.

### Capacitors

| Capacitor | Value | Type | Part Number | Location | Notes |
| --- | --- | --- | --- | --- | --- |
| C2 | 0.1µF | Ceramic X7R | (any) | As close as possible to XBee XPIN1/XPIN10 | High-frequency bypass. |
| C3 | 10µF | Ceramic X7R | (any) | Within 10mm of U1 VOUT | Bulk on LDO output. |
| C4 | 4.7µF | Ceramic X7R | (any) | At U2 VIN pin | XC9140 datasheet-specified input cap; X7R required. |
| C5 | 10µF | Ceramic X7R | (any) | At U2 VOUT pin | XC9140 datasheet-specified output cap; X7R required. |
| C6 | 100µF | Electrolytic radial | EMVE160ARA101MF55G | From XPIN11 node to GND (tilt debounce) | 16V 100µF 5×5.5mm Panasonic. RC = 1kΩ × 100µF = 100ms. |
| C7 | 100nF | Ceramic X7R | (any) | XPIN20 to GND (commissioning button debounce, optional) | Optional; only needed if false button triggers observed. |

---

## 11. Build Notes

1. **Common ground is mandatory.** Run a single GND bus across the breadboard. All negative terminals, regulator GNDs, and sensor GNDs must tie to this bus.
2. **Cut CE trace on XC9140 protoboard** before wiring R3/R4. Verify with a multimeter (CE to VIN should read open before soldering).
3. **Capacitor selection:** C2, C3, C4, C5 are ceramic X7R (from stock). C6 is the EMVE160ARA101MF55G (100µF 16V radial electrolytic, 5×5.5mm) which restores the full 100ms RC debounce in a single compact component. C4 (4.7µF at the shared 2xAA battery rail) serves as the input filter for both the MCP1700 (min 1µF) and the XC9140 — a separate C1 is unnecessary on a protoboard with short traces, as confirmed by working prototype. C4 and C5 must be X7R (not Y5V) for stable XC9140 boost converter operation.
4. **Battery divider resistors (R10/R11):** Use 1% tolerance parts for accurate battery voltage tracking. Standard 5% resistors will cause ±5% error in reported battery level. Place resistors as close as possible to the battery connector to minimize lead-induced noise on the ADC input.
5. **Keep DQ wire short.** Long wires increase capacitance and can cause CRC errors. Under 30cm is best for a breadboard prototype.
6. **Keep XPIN11 wire short.** Noise on this line can cause false door-state events.
7. **Do not tie XPIN9 externally.** Sleep Request is driven by firmware. Tying it HIGH or LOW will prevent the sleep cycle from working.
8. **XPIN5 (Reset) and XPIN8 (BKGD)** must be left unconnected for normal operation. They are used only by CodeWarrior debugger.
9. **Verify 3.3V_A is present before powering sensors.** Use a multimeter to confirm MCP1700 output before connecting DS18B20.
10. **DS18B20 parasitic mode — VDD pin must be tied to GND**, not left floating. Floating VDD is a common fault that causes intermittent CRC errors.
11. **PMOSFET gate resistors are both required.** R7 (180Ω) damps gate ringing. R8 (100k) pulls gate to GND when XPIN7 is high-impedance during boot/reset, preventing unintended DQ drive. Do not omit R8.
12. **R1 pull-up connects to 3.3V_A, not 3.3V_S.** DQ must remain biased when XBee is awake but before 3.3V_S has started up.
13. **C6 tilt debounce.** EMVE160ARA101MF55G (100µF electrolytic) with R2 (1k) gives RC = 100ms — full original debounce window restored in a single 5×5.5mm component.
14. **J1 (diagnostic header) must be disconnected before field deployment.** An attached CP2102 draws current continuously and adds a conductive path to the outside world. Populate J1 with a 3-pin male header; leave it unpopulated on the production build or cap it with a jumper shunt.
15. **Tilt switch supply must be 3.3V_A (always-on).** Do not power S1 from 3.3V_S, or door transitions cannot wake the XBee while it is asleep.

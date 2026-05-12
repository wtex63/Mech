# CP2102 USB Diagnostic Connection Guide

**Sensor node:** XBee ZB (S2B) Garage Door Sensor  
**Adapter module:** DIYmalls CP2102 — Amazon ASIN [B086ZHGKZT](https://www.amazon.com/dp/B086ZHGKZT)  
**Purpose:** Monitor real-time `printf` debug output from the XBee firmware over USB

---

## 1. Board Overview

The DIYmalls B086ZHGKZT is a 6-in-1 USB serial adapter built around a Silicon Labs
CP2102 chip and a MAX3232 level-converter chip. It can be set to several different
modes using two DIP switches and one horizontal slide switch.

**Board connectors/headers (standard layout):**

| Header pin | Signal (TTL mode) |
| --- | --- |
| VCC | 3.3V or 5V (set by voltage jumper — see section 3) |
| GND | Common ground |
| TXD | CP2102 transmit out → feeds into target RX |
| RXD | CP2102 receive in  ← accepts target TX |
| RTS | (not used for this application) |
| CTS | (not used for this application) |

---

## 2. Mode Switch Configuration

The board has **two DIP switches** (DIP1, DIP2) and **one horizontal slide switch**.
Wrong switch positions are the most common reason communications fail.

For **USB ↔ TTL** operation (the mode needed for XBee diagnostics):

| Switch | Required position |
| --- | --- |
| DIP switch 1 | **UP** (ON) |
| DIP switch 2 | **DOWN** (OFF) |
| Horizontal slide | **LEFT** (toward USB connector) |

> **Tip from user reviews:** Set TX → RX and RX → TX on your terminal (cross-wired).
> If DIP1 is DOWN instead of UP, the module silently fails; no error is shown.

---

## 3. Voltage Level — Critical Safety Step

The XBee UART pins (XPIN2, XPIN3) operate at **3.3V TTL logic**.
The CP2102 board has a solder jumper or header jumper to select 3.3V or 5V for
the VCC/output rail.

**Before connecting to the XBee:**

1. Do **not** plug into the XBee yet.
2. Plug the CP2102 board into your PC USB port.
3. Set your multimeter to DC voltage, black probe to GND pin, red probe to TXD pin.
4. Open any terminal (PuTTY, CoolTerm, etc.) — the idle UART line should be HIGH.
5. **Confirm reading is 3.3V** (± 0.1V). If it reads 5V, move the voltage jumper to
   the 3.3V position before proceeding.
6. Also confirm VCC pin reads 3.3V if you measure it (but do not connect VCC to the circuit at all).

---

## 4. Physical Wiring

Use the included 6-pin F/F cable or individual Dupont jumper wires.
**Only three wires are needed.** Do not connect the VCC pin.

```text
XBee Sensor Board           CP2102 Board
─────────────────           ────────────
J1 pin 1 (DIAG_TX) ──────> RXD
J1 pin 2 (DIAG_RX) <────── TXD
J1 pin 3 (GND)     ──────> GND

                            VCC  ← DO NOT CONNECT
                            RTS  ← leave unconnected
                            CTS  ← leave unconnected
```

**Wire connections via J1 diagnostic header:**

| Wire colour (suggestion) | From | To |
| --- | --- | --- |
| Orange | J1 pin 1 (XPIN2 TX) | CP2102 RXD |
| Yellow | J1 pin 2 (XPIN3 RX) | CP2102 TXD |
| Black | J1 pin 3 (GND) | CP2102 GND |

---

## 5. PC Driver Installation

The CP2102 requires the Silicon Labs VCP driver before Windows will assign a
COM port.

1. Download from: <https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers>
2. Run the installer (supports Windows 7/8/10/11, 32-bit and 64-bit).
3. Plug in the USB adapter; Device Manager should show **Silicon Labs CP210x USB to UART Bridge (COMx)**.
4. Note the assigned COM port number.

---

## 6. Terminal Software Settings

Open any serial terminal and configure it as follows:

| Parameter | Value |
| --- | --- |
| Port | COMx (from Device Manager) |
| Baud rate | **115200** |
| Data bits | 8 |
| Parity | None |
| Stop bits | 1 |
| Flow control | **None** |
| Line ending | CR+LF |

**Recommended free terminals:** PuTTY · CoolTerm · Tera Term · VS Code Serial Monitor extension

---

## 7. Expected Output

When the sensor node powers on and joins the Zigbee network, the UART prints
startup and periodic diagnostic lines. Use these as markers to coordinate
oscilloscope captures.

Typical lines for the current firmware are similar to:

```text
--- Radio Settings ---
FC00 cmd=0x01 (poll) -> queuing temp read
FC00 TX: TEMP_C=24.62,DOOR=closed,VBAT_MV=3910,BATT_PCT=92
[DOOR] open
FC00 door TX: DOOR=open,VBAT_MV=3904,BATT_PCT=91
[DOOR] closed
FC00 door TX: DOOR=closed,VBAT_MV=3901,BATT_PCT=91
```

Scope capture markers:

1. Use `FC00 cmd=0x01 (poll)` as the start marker for a forced sensor read cycle.
2. Use `FC00 TX:` as the end marker for that cycle.
3. During this interval, probe DQ and PMOS gate to verify strong pull-up timing.

If you see nothing at all:

- Check DIP switch settings (Section 2).
- Verify GND is connected.
- Confirm baud rate is 115200.
- Swap TX/RX wires (J1 pin 1 ↔ pin 2) — wrong orientation is silent.

If you see garbage characters:

- Baud rate is wrong; try 9600 if a different firmware build was flashed.

---

## 8. Warnings and Limitations

| Issue | Detail |
| --- | --- |
| **No VCC connection** | Do not connect CP2102 VCC to the sensor 3.3V_A or 3.3V_S rail. The CP2102 board draws up to 100 mA from USB; this would instantly drain the 2xAA batteries. VCC on the CP2102 header is an OUTPUT, not an input for this use. |
| **3.3V logic only** | The XBee UART pins tolerate 3.3V maximum. A 5V TXD from the CP2102 board will exceed the XBee absolute maximum rating and may damage XPIN3. Always confirm voltage before connecting (Section 3). |
| **Disconnect before field deployment** | The CP2102 adapter keeps XPIN3 driven even when idle. In the field, J1 must be unconnected or the board removed from the sensor entirely. |
| **Sleep gaps** | During XBee pin-sleep the UART is inactive. The terminal will appear silent for up to 60 seconds between wake events — this is normal. |
| **Heat on MAX3232 chip** | Some units report the MAX3232 chip getting hot during RS232/RS485 modes. In USB-to-TTL mode (DIP1 UP, DIP2 DOWN) this chip is not in the signal path and should remain cool. If the board gets hot in TTL mode, re-check DIP switch positions. |

---

## 9. Oscilloscope-Assisted Workflow (Recommended)

Use CP2102 + terminal + scope together for deterministic captures.

1. Connect CP2102 as in Section 4 and open terminal at 115200.
2. Connect scope CH1 to DQ (XPIN11 net) and CH2 to PMOS gate (XPIN12 side through gate resistor).
3. In Hubitat, click Refresh to force poll, or toggle tilt to force immediate report.
4. Watch terminal for `FC00 cmd=0x01 (poll)` and `FC00 TX:` lines.
5. Capture around that interval and verify:
   - Gate goes LOW only during strong pull-up window.
   - DQ remains near 3.3V during conversion window.
6. Save matching screenshot + terminal snippet as a pair for each run.

---

## 10. Quick-Reference Checklist

- [ ] CP2102 driver installed and COM port visible in Device Manager
- [ ] DIP1 = UP, DIP2 = DOWN, horizontal switch = LEFT
- [ ] Voltage jumper set to **3.3V** — confirmed with multimeter
- [ ] Three wires connected: J1-pin1 → RXD, J1-pin2 → TXD, J1-pin3 → GND
- [ ] VCC pin on CP2102 board left unconnected
- [ ] Terminal set to 115200 8N1 no flow control
- [ ] Sensor powered from 2xAA batteries (not from CP2102)

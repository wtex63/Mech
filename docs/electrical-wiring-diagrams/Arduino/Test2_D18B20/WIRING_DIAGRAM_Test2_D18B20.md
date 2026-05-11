# Wiring Diagram - Test2_D18B20

This wiring matches `Test2_D18B20.ino`.

## Sketch Pin Map

- `ONE_WIRE_BUS_PIN = 2` -> Arduino Uno `D2`
- DS18B20 data bus requires a `4.7k` pull-up resistor from `DQ` to `VCC`

## DS18B20 TO-92 Pinout

Hold the flat face of the DS18B20 toward you, leads pointing down:

- Left = Pin 1 = `GND`
- Middle = Pin 2 = `DQ`
- Right = Pin 3 = `VDD`

## Normal-Power Wiring (recommended first test)

```text
Arduino Uno                     DS18B20
-----------                     -------
5V  --------------------------> VDD (pin 3)
GND --------------------------> GND (pin 1)
D2  --------------------------> DQ  (pin 2)

4.7k resistor:
One end -> DQ (pin 2) node
Other end -> 5V
```

## Parasite-Power Wiring (optional)

Use only after normal-power mode passes.

```text
Arduino Uno                     DS18B20
-----------                     -------
GND --------------------------> GND (pin 1)
GND --------------------------> VDD (pin 3)   <-- tied to GND for parasite mode
D2  --------------------------> DQ  (pin 2)

4.7k resistor:
One end -> DQ (pin 2) node
Other end -> 5V
```

## ASCII Wiring Diagram (Normal-Power)

```text
                 +5V (Uno)
                    |
                  [4.7k]
                    |
Uno D2 -------------+------------------- DS18B20 pin 2 (DQ)

Uno GND -------------------------------- DS18B20 pin 1 (GND)
Uno 5V  -------------------------------- DS18B20 pin 3 (VDD)
```

## Quick Bring-Up Checklist

1. Verify continuity from Uno `D2` to DS18B20 `DQ`.
2. Verify `4.7k` is really from `DQ` to `5V`.
3. Verify common ground.
4. Open Serial Monitor at `115200`.
5. Look for:

- `Bus idle state: HIGH`
- `1-Wire reset/presence: PRESENT`
- `CRC: OK`

## XBee Low-Power Prototype Wiring (for sleep firmware)

Use this when moving from Arduino bench test to the XBee programmable node firmware.

### Required Signals

- DS18B20 `DQ` -> XBee `XPIN4`
- DS18B20 `VDD` -> regulated supply rail used by XBee
- DS18B20 `GND` -> XBee `GND`
- `4.7k` pull-up from `DQ` to sensor/XBee supply rail

### Sleep/Power Management Pins (internal XBee use)

- `XPIN9` = Sleep Request (driven by firmware power-management API)
- `XPIN13` = On/Sleep indicator (status from radio)

These are internal to the programmable XBee module firmware flow and should not be tied to external logic during initial prototype bring-up.

### Battery Monitoring Strategy

The current firmware reads XBee AT `%V` and reports:

- `VBAT_MV=<millivolts>`
- `BATT_PCT=<0..100>`

That means no extra ADC divider is required for single-cell Li-ion/LiPo style prototypes where XBee supply voltage is the battery rail being monitored.

### Optional External Divider (only if battery voltage exceeds XBee-safe measurement range)

If your battery pack is higher than the XBee operating range, monitor through an external divider into an ADC-capable front-end on your carrier (not directly to non-ADC XBee pins).

Design targets:

- Divider current <= `10 uA` to minimize standby drain
- Example ratio for high-voltage pack: `Rtop=1M`, `Rbottom=330k` (adjust to ADC reference)
- Add small capacitor (`10-100 nF`) at ADC input for stable sampling

## Battery-Life Recheck Checklist

1. Verify firmware uses power-management sleep API (radio + CPU sleep cycle).
2. Verify DS18B20 cable length and pull-up quality to avoid retries (retries waste energy).
3. Keep serial logging disabled in production builds except short diagnostics.
4. Confirm reporting interval is as long as acceptable for your use case.
5. Validate Hubitat receives `VBAT_MV` and `BATT_PCT` fields.

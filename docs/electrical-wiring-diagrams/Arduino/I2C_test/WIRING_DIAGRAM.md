# I2C Test Breadboard Wiring

This test setup uses the Arduino UNO R3 USB connector for power.

## Goal

- Verify BME280 I2C traffic on the SDS1204X-E
- Use a simple known-good sketch with continuous bus activity
- Power the board from USB-C while probing SDA and SCL

## Parts

- Arduino UNO R3
- BME280 breakout board
- Breadboard
- Jumper wires
- USB cable for UNO (typically USB-B on official UNO R3)
- Siglent SDS1204X-E oscilloscope

## Wiring

```text
Arduino UNO R3                BME280 Breakout
---------------------------   ----------------------
USB to PC/charger
3.3V -----------------------> VCC / 3.3V
GND ------------------------> GND
A4 (SDA) -------------------> SDA
A5 (SCL) -------------------> SCL
GND ------------------------> SDO   (sets address 0x76)
3.3V -----------------------> CS/CSB (forces I2C mode on boards that expose CS)
```

## Breadboard Layout

```text
┌─────────────────────────────────────────────────────┐
│ Breadboard                                          │
│                                                     │
│   Arduino UNO R3                      BME280        │
│  ┌───────────────┐                  ┌───────────┐   │
│  │ USB power     │                  │ VCC   SDA │   │
│  │               │ 3V3 -----------→ │           │   │
│  │ A4 (SDA) ---- ├────────────────→ │ SDA       │   │
│  │ A5 (SCL) ---- ├────────────────→ │ SCL       │   │
│  │ GND --------- ├────────────┬───→ │ GND       │   │
│  │ 3V3 --------- ├────────────┘     │ VCC       │   │
│  └───────────────┘                  │ SDO to GND│   │
│                                     │ CS to 3V3 │   │
│                                     └───────────┘   │
└─────────────────────────────────────────────────────┘
```

## Scope Connections

- CH2 probe tip to SCL
- CH3 probe tip to SDA
- Probe ground clips to circuit GND
- Use short ground leads if possible

## Known-Good Scope Setup

- CH2: DC coupling, 1 V/div to 2 V/div
- CH3: DC coupling, 1 V/div to 2 V/div
- Timebase: 20 us/div first, then 5 us/div for detail
- Trigger: Edge on CH2, rising, 1.6 V, Auto for setup then Normal
- Decode: I2C, SCL = CH2, SDA = CH3, 7-bit, Hex, 100 kHz expected

## Notes

- Use a BME280 breakout that supports 3.3V operation.
- Most BME280 breakout boards already include I2C pull-ups.
- If your breakout does not include pull-ups, add 4.7k to 10k from SDA to 3.3V and from SCL to 3.3V.
- Idle SDA and SCL should both sit near 3.3V.
- If your BME280 board is not 5V-tolerant on SDA/SCL, use a bidirectional level shifter between UNO and sensor.
- The sketch reads register 0xD0 every 100 ms, so the bus remains active for the scope.
- A valid BME280 chip ID is 0x60.

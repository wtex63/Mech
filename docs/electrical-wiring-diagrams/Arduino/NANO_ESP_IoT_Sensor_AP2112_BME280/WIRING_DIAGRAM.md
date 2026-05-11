# ESP32-S3 Nano Sensor Node - Wiring Diagram (XC6220A LDO + BME280)

## Component List
- ESP32-S3 Nano
- BME280 Temperature/Humidity/Pressure Sensor (I2C)
- Z024 PIR Motion Sensor (Onyrhn - with built-in filtering)
- 18650 Li-ion Cell (3.7V nominal, 4.2V max, externally charged)
- XC6220A331MR-G LDO Voltage Regulator (3.3V fixed output, 1000mA, SOT-25)
- Resistors: 470kΩ, 100kΩ (battery monitor only)
- Capacitors: 1µF (input), 1µF (output), 1000µF (bulk), 100µF (x3), 0.1µF (x4)

## Pin Connections

### ESP32-S3 Nano Pins
```
┌─────────────────────────────┐
│      ESP32-S3 NANO          │
├─────────────────────────────┤
│ 3V3  ─────────────────── VCC│
│ GND  ─────────────────── GND│
│                             │
│ GPIO 0  ─────── DEBUG_PIN   │ (Debug Mode Switch)
│ GPIO 3  ─────── PIR_PIN     │ (PIR Motion Sensor)
│ GPIO 5  ─────── ADC_PIN     │ (Battery Voltage)
│ GPIO 6  ─────── WAKE_SWITCH │ (Wake Mode Switch)
│ GPIO 21 ─────── SDA         │ (I2C Data - BME280)
│ GPIO 22 ─────── SCL         │ (I2C Clock - BME280)
└─────────────────────────────┘
```

## Detailed Wiring

### Power Supply - XC6220A331MR-G LDO Regulator (3.3V, 1000mA)
```
18650 Li-ion Cell (3.7V nominal, 4.2V max)

   (+) ────┬──── XC6220A VIN (Pin 3)
           │
          [1µF]  ← Input capacitor (ceramic, X7R, 10V rated)
           │
   (-) ────┴──── XC6220A VSS (Pin 1)


XC6220A LDO Connections (SOT-25 package):
  Pin 1 (VSS)     ──── 18650 (-) / Common GND
  Pin 2 (CE)      ──── VIN (chip enable - active HIGH, always on)
  Pin 3 (VIN)     ──── 18650 (+) via 1µF input capacitor
  Pin 4 (NC)      ──── Not connected
  Pin 5 (VOUT)    ──── 3.3V Output (regulated)

Output:
  XC6220A VOUT (Pin 5) ────┬──── VCC Rail (3.3V regulated)
                           │
                          [1µF]  ← Output capacitor (ceramic, X7R, 6.3V rated)
                           │
                           └──── GND

Notes:
  - Output voltage: Fixed 3.3V (±2% accuracy)
  - Maximum current: 1000mA continuous (excellent for ESP32 WiFi peaks)
  - Quiescent current: 1µA typical (ultra-low! Better battery life than AP2112K)
  - Dropout voltage: 100mV @ 300mA, 250mV @ 1A (works down to 3.45V input)
  - Input voltage range: 1.7V - 6V (perfect for 18650: 3.5V-4.2V when charged)
  - CE pin is Active HIGH - connect to VIN for always-on operation
  - No inductor needed - simplest possible design!
  - Very low noise output - ideal for ADC and WiFi
```

### Power Distribution
```
XC6220A VOUT (3.3V) ──────┬──── VCC Rail (Breadboard)
                         │
                        [1000µF]  ← Additional bulk capacitor (optional)
                         │
18650 Cell (-) ──────────┴──── GND Rail (Breadboard)


VCC Rail ──────┬──── ESP32 3V3
               │
              [100µF]  ← ESP32 power filter
               │
              [0.1µF]  ← ESP32 high-frequency filter
               │
               └──── ESP32 GND
```

### PIR Sensor (Z024 with Built-in Filtering)
```
Z024 PIR Board:
  VCC ────┬──── VCC Rail
          │
         [100µF]  ← PIR power filter (optional)
          │
  GND ────┴──── GND Rail

  OUT ──── ESP32 GPIO 3 (PIR_PIN)
  
Note: Z024 has built-in filtering and pull resistors - no external components needed
Note: PIR hold time is ~2 seconds - code waits for this before enabling wake
```

### BME280 Sensor (I2C - Temperature, Humidity, Pressure)

**Current Design: BME280 Breakout Board** (recommended for prototyping)
```
BME280 Breakout Board:
  VCC (or 3.3V) ───┬──── VCC Rail
                   │
                  [100µF]  ← BME280 power filter
                   │
  GND ─────────────┴──── GND Rail

  SDA ──── ESP32 GPIO 21 (I2C Data)
  SCL ──── ESP32 GPIO 22 (I2C Clock)
  
  SDO ──── GND (sets I2C address to 0x76)
       OR
       ──── VCC (sets I2C address to 0x77)

Note: I2C has internal pull-ups on most BME280 breakout boards
Note: No external pull-up resistors needed
Note: Much faster readings than DHT22 (<10ms vs 2 seconds)
Note: Lower power consumption (3.6µA sleep vs 50µA for DHT22)
```

**Future Production: Bare BME280 Chip (LGA-8 package)**
```
For custom PCB designs using bare BME280 chip (2.5mm x 2.5mm):

VCC Rail ──────┬──── 10kΩ ──── SDA ──── ESP32 GPIO 21
               │
               ├──── 10kΩ ──── SCL ──── ESP32 GPIO 22
               │
               ├──── BME280 VDD
               │
              [0.1µF]  ← Decoupling capacitor (place close to chip)
               │
GND Rail ──────┴──── BME280 VSS

Additional Requirements:
  - Two 10kΩ resistors for I2C pull-ups (SDA and SCL to VCC)
  - 0.1µF (100nF) ceramic capacitor for VDD/VDDIO decoupling
  - Custom PCB with LGA-8 footprint (0.5mm pad pitch)
  - Reflow soldering or hot air station required
  - Recommended only for production runs >100 units
  
Breakout board includes all of this - much easier for prototyping!
```

### Battery Voltage Monitor
```
18650 Cell (+) ───┬──── 470kΩ ────┬──── ESP32 GPIO 5 (ADC_PIN)
                  │                │
                  │               [0.1µF] ← ADC filter (optional)
                  │                │
                  └──── 100kΩ ────┴──── GND Rail

Voltage Divider Ratio: (470k + 100k) / 100k = 5.7
Max measurable voltage: 3.3V × 5.7 = 18.81V
18650 Range: 2.5V-4.2V (well within range)

Important: This monitors the raw battery voltage BEFORE the buck converter
```

### Debug/Wake Switches
```
Debug Switch (GPIO 0) - Uses Internal Pull-down:
  ESP32 GPIO 0 (DEBUG_PIN) ──── Switch ──── VCC Rail
      [INPUT_PULLDOWN internal ~45kΩ]
  
  - Internal pull-down keeps pin LOW (0V) when switch is open
  - Pressing switch connects to VCC → HIGH (3.3V) → Debug Mode on boot/reset
  - Only checked on boot, does NOT wake from deep sleep
  - NO external resistor needed


Wake Switch (GPIO 6) - Uses Internal Pull-down:
  ESP32 GPIO 6 (WAKE_SWITCH) ──── Switch ──── VCC Rail
      [INPUT_PULLDOWN internal ~45kΩ]
  
  - Internal pull-down keeps pin LOW (0V) during deep sleep
  - Pressing switch connects to VCC → HIGH (3.3V) → triggers wake from deep sleep
  - Matches PIR wake logic (both wake on HIGH signal)
  - Can also trigger debug mode if held during boot
  - NO external resistor needed
```

## Breadboard Layout Recommendations

```
┌──────────────────────────────────────────────────────────────────┐
│  18650 Cell ──[XC6220A LDO]──── VCC Rail (3.3V) ════════════      │
│   (3.7V)    Ultra-Low Power!    ║                                │
│                                 ║                                │
│                   [1µF]   [1µF] [1000µF]  [100µF]    [100µF]     │
│                    │      │       │         │           │         │
│                ┌───┴──────┴───────┴───┬─────┴────┐  ┌───┴────┐  │
│                │   XC6220A LDO      │  ESP32   │  │ BME280 │  │
│                │   Regulator        │   NANO   │  │ Sensor │  │
│                └─────────────────┬───┴────┬─────┘  └───┬────┘  │
│                                  │    SDA/SCL       │         │
│  ┌───┴────┐                     │     [0.1µF]      [0.1µF]     │
│  │  PIR   │                     │       │            │         │
│  │ Z024   │                     │       │            │         │
│  └───┬────┘                     │       │            │         │
│      │                          │       │            │         │
│   [0.1µF]                       │       │            │         │
│      │                          │       │            │         │
│  GND Rail ═══════════════════════════════════════════════════   │
└──────────────────────────────────────────────────────────────────┘

LAYOUT TIPS:
- Place XC6220A LDO regulator near the 18650 cell
- Keep input/output capacitors (1µF) very close to XC6220A pins
- No inductor needed - simplest possible power supply!
- Keep ESP32, BME280, and PIR physically separated
- Place PIR sensor away from ESP32 and LDO
- I2C wires (SDA/SCL) can be longer than DHT22 data line (more robust)
- Use shortest possible wires for all connections
- Keep all GND connections short and direct to GND rail
- LDO produces no switching noise - very clean power for sensors
```

## Component Shopping List

### Power Supply Components
- **XC6220A331MR-G LDO Regulator** (1x) - SOT-25 package, 3.3V fixed output, 1000mA, 1µA quiescent
  - Alternative: AP2112K-3.3TRG1 (600mA, 55µA quiescent)
  - Alternative: NCP167BMX330TBG (700mA, 55µA quiescent)
- **18650 Li-ion Cell** (1x) - 3.7V nominal, 2000-3500mAh capacity
- **18650 Battery Holder** (1x) - With solder tabs or wire leads
- **1µF Ceramic Capacitor** (2x) - X7R or X5R, 10V or higher (input & output)

### Sensor Components
- **BME280 Breakout Board** (1x) - I2C interface, 3.3V (Adafruit, SparkFun, or generic)
  - Alternative: BME680 if air quality sensing desired
- **Z024 PIR Motion Sensor** (1x) - Onyrhn brand with built-in filtering

### Essential Components
- **1000µF Electrolytic Capacitor** (1x) - Main power filter, 6.3V or higher
- **100µF Electrolytic Capacitor** (2x) - Power filters (ESP32, BME280), 6.3V or higher  
- **0.1µF Ceramic Capacitor** (4x) - High-frequency noise filtering, 50V
- **470kΩ Resistor** (1x) - Voltage divider R1 (battery monitor)
- **100kΩ Resistor** (1x) - Voltage divider R2 (battery monitor)

### Optional Upgrades
- **10µF Tantalum Capacitors** - Better filtering than electrolytics
- **Ferrite Beads** - On power lines for EMI filtering
- **Shielded Wire** - For PIR signal line
- **18650 Charging Module** - TP4056 or similar for USB charging

## Common Issues & Solutions

### False PIR Triggers
✓ Z024 board has built-in filtering - no external components needed
✓ Remove any external pull-down resistors (causes 1.5V stuck state)
✓ Keep PIR away from ESP32 and power supply
✓ Use short, direct wires

### Power Instability
✓ Add 1000µF capacitor on main power
✓ Add 100µF + 0.1µF near ESP32
✓ Use thick ground connections
✓ Ensure all grounds connect to same rail

### Sensor Read Failures
✓ Check all VCC/GND connections
✓ Add capacitors near sensor power pins
✓ Verify DHT22 is genuine (not clone)
✓ Test sensors individually

## Testing Procedure

1. **LDO Regulator Test** - Before connecting ESP32:
   - Connect 18650 cell to XC6220A VIN (Pin 3)
   - Connect CE (Pin 2) to VIN for always-on (Active HIGH enable)
   - Ensure VSS (Pin 1) connected to battery GND
   - Measure VOUT (Pin 5) - should be 3.30V ±0.07V
   - Check for stable voltage (no oscillation)
   - LDO will be slightly warm under load (normal)

2. **Power Test** - Measure voltage at ESP32 VCC pin (should be stable 3.3V)
3. **Ground Test** - Verify continuity between all GND points
4. **Battery Monitor Test** - Check ADC reading:
   - 4.2V battery → ~0.73V at ADC → reading ~4.2V
   - 3.7V battery → ~0.65V at ADC → reading ~3.7V  
   - 3.5V battery → ~0.61V at ADC → reading ~3.5V
5. **PIR Test** - Verify motion detection works correctly
6. **BME280 Test** - Verify I2C communication and sensor readings:
   - Run I2C scanner to confirm address (0x76 or 0x77)
   - Check temperature reading (~room temp)
   - Check humidity reading (30-70% typical)
   - Check pressure reading (~1013 mbar at sea level)
7. **Load Test** - Monitor LDO voltage during WiFi transmission (may dip ~50mV, still safe)

## Notes

- **Z024 PIR Board**: Has built-in filtering and pull resistors - connect output directly to ESP32
- **XC6220A LDO**: Simple, ultra-low noise regulator perfect for battery-powered ESP32 projects
- **LDO Efficiency**: ~75% typical - acceptable for deep sleep applications with short active periods
- **Quiescent Current**: 1µA typical - even better than AP2112K, essentially zero impact on battery life!
- **Heat Dissipation**: LDO will be warm during WiFi transmission (~0.3W heat) - this is normal
- **Dropout Voltage**: 100mV @ 300mA, 250mV @ 1A - regulator works down to 3.45V input (safe for charged 18650)
- **Higher Current Rating**: 1A vs 600mA - plenty of headroom for ESP32 WiFi peaks
- **No Switching Noise**: LDO produces ultra-clean DC - perfect for ADC and WiFi
- **Simplicity**: Only 2 capacitors needed (1µF input, 1µF output) - no inductor!
- **BME280 Sensor**: Much better than DHT22 - faster, more accurate, adds pressure sensing
- **I2C Communication**: More robust than DHT22's single-wire protocol
- **Battery Life**: Expect 2-3 weeks between charges (externally charged 18650)
- **18650 Cell**: Provides ~2000-3500mAh capacity
- All capacitor negative terminals connect to GND
- Electrolytic capacitors are polarized - observe +/- markings
- Ceramic capacitors are non-polarized
- For permanent installation, consider soldering on a prototype board or custom PCB
- Extremely simple circuit - easiest to build and debug of all voltage regulator options


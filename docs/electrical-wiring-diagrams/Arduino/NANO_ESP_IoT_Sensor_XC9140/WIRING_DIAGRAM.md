# ESP32-S3 Nano Sensor Node - Wiring Diagram (XC9140 Buck Converter)

## Component List
- ESP32-S3 Nano
- DHT22 Temperature/Humidity Sensor
- Z024 PIR Motion Sensor (Onyrhn - with built-in filtering)
- 18650 Li-ion Cell (3.7V nominal, 4.2V max, 2.5V min)
- XC9140 Synchronous Buck Converter IC (3.3V fixed output, 700mA, SOT-25)
- Inductor: 4.7µH or 10µH (rated ≥700mA)
- Resistors: 470kΩ, 100kΩ, 4.7kΩ (DHT22)
- Capacitors: 10µF (input), 22µF (output), 1000µF (bulk), 100µF (x3), 0.1µF (x4)

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
│ GPIO 4  ─────── DHT_PIN     │ (DHT22 Data)
│ GPIO 5  ─────── ADC_PIN     │ (Battery Voltage)
│ GPIO 6  ─────── WAKE_SWITCH │ (Wake Mode Switch)
└─────────────────────────────┘
```

## Detailed Wiring

### Power Supply - XC9140 Synchronous Buck Converter (3.3V, 700mA)
```
18650 Li-ion Cell (3.7V nominal, 4.2V max)

   (+) ────┬──── XC9140 VBAT (Pin 3)
           │
          [10µF]  ← Input capacitor (ceramic, X7R, 10V rated)
           │
   (-) ────┴──── XC9140 GND (Pin 2)


XC9140 Buck Converter Connections (SOT-25 package):
  Pin 1 (CE)      ──── VBAT (chip enable - always on)
  Pin 2 (GND)     ──── 18650 (-) / Common GND
  Pin 3 (VBAT)    ──── 18650 (+) via 10µF input capacitor
  Pin 4 (VOUT)    ──── 3.3V Output (regulated)
  Pin 5 (LX)      ──── Switching node (to inductor)

Inductor & Output:
  XC9140 LX (Pin 5) ────[4.7µH or 10µH Inductor]──── VOUT

  VOUT (Pin 4) ────┬──── VCC Rail (3.3V regulated)
                   │
                  [22µF]  ← Output capacitor (ceramic, X7R, 6.3V rated)
                   │
                   └──── GND

Notes:
  - Output voltage: Fixed 3.3V version (e.g., XC9140C333MR)
  - Maximum current: 700mA continuous
  - Switching frequency: ~1.2MHz typical
  - High efficiency: 90-95% (better than LDO)
  - Inductor: 4.7µH or 10µH, rated ≥700mA saturation current
  - Input voltage range: 2.5V - 5.5V (perfect for 18650)
```

### Power Distribution
```
XC9140 VOUT (3.3V) ──────┬──── VCC Rail (Breadboard)
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

### DHT22 Sensor
```
DHT22:
  VCC ────┬──── VCC Rail
          │
         [100µF]  ← DHT22 power filter
          │
  GND ────┴──── GND Rail

  DATA ───┬──── ESP32 GPIO 4 (DHT_PIN)
          │
  VCC ───[4.7kΩ]  ← Pull-up resistor (REQUIRED for DHT22)
  
Note: The 0.1µF filter capacitor is optional and usually not needed
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
│  18650 Cell ──[XC9140 Buck]─── VCC Rail (3.3V) ════════════      │
│   (3.7V)      + Inductor        ║                                │
│                                 ║                                │
│                  [10µF]  [22µF] [1000µF]  [100µF]    [100µF]     │
│                    │      │       │         │           │         │
│                ┌───┴──────┴───────┴───┬─────┴────┐  ┌───┴────┐  │
│                │   XC9140 Buck       │  ESP32   │  │ DHT22  │  │
│                │   Converter         │   NANO   │  │ Sensor │  │
│                └─────────────────┬───┴────┬─────┘  └───┬────┘  │
│                                  │       │            │         │
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
- Place XC9140 buck converter near the 18650 cell
- Keep inductor and XC9140 close together (short LX trace)
- Use 10µF ceramic at input, 22µF ceramic at output
- Keep ESP32, DHT22, and PIR physically separated
- Place PIR sensor away from ESP32 and buck converter
- Run PIR signal wire away from power lines and LX switching node
- Use shortest possible wires for all connections
- Keep all GND connections short and direct to GND rail
- Route LX switching node away from sensitive signals
```

## Component Shopping List

### Power Supply Components
- **XC9140C333MR Buck Converter IC** (1x) - SOT-25 package, 3.3V fixed output, 700mA
- **Inductor 4.7µH or 10µH** (1x) - Rated ≥700mA saturation current, low DCR
- **18650 Li-ion Cell** (1x) - 3.7V nominal, 2000-3500mAh capacity
- **18650 Battery Holder** (1x) - With solder tabs or wire leads
- **10µF Ceramic Capacitor** (1x) - X7R or X5R, 10V or higher (input)
- **22µF Ceramic Capacitor** (1x) - X7R or X5R, 6.3V or higher (output)

### Essential Components
- **1000µF Electrolytic Capacitor** (1x) - Main power filter, 6.3V or higher
- **100µF Electrolytic Capacitor** (3x) - Power filters for each device, 6.3V or higher
- **0.1µF Ceramic Capacitor** (4x) - High-frequency noise filtering, 50V
- **4.7kΩ Resistor** (1x) - DHT22 data line pull-up (required for communication)
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

1. **Buck Converter Test** - Before connecting ESP32:
   - Connect 18650 cell to XC9140 VBAT (Pin 3)
   - Connect CE (Pin 1) to VBAT for always-on
   - Connect inductor between LX (Pin 5) and VOUT (Pin 4)
   - Ensure GND (Pin 2) connected to battery GND
   - Measure VOUT - should be 3.30V ±0.05V
   - Check for stable voltage (no oscillation)
   - Verify no excessive heat on XC9140 or inductor

2. **Power Test** - Measure voltage at ESP32 VCC pin (should be stable 3.3V)
3. **Ground Test** - Verify continuity between all GND points
4. **Battery Monitor Test** - Check ADC reading:
   - 4.2V battery → ~0.73V at ADC → reading ~4.2V
   - 3.7V battery → ~0.65V at ADC → reading ~3.7V  
   - 3.0V battery → ~0.53V at ADC → reading ~3.0V
5. **PIR Test** - Verify motion detection works correctly
6. **Sensor Test** - Verify DHT22 reads correctly
7. **Load Test** - Monitor buck converter voltage during WiFi transmission (should remain stable)

## Notes

- **Z024 PIR Board**: Has built-in filtering and pull resistors - connect output directly to ESP32
- **XC9140 Buck Converter**: Synchronous step-down converter with high efficiency
- **Efficiency**: 90-95% typical - much better than LDO for battery life
- **Switching Frequency**: ~1.2MHz - requires proper layout to minimize noise
- **Input Range**: 2.5V - 5.5V (perfect for 18650 cell: 2.5V-4.2V)
- **Inductor**: 4.7µH or 10µH rated ≥700mA, keep traces to LX pin short
- **Ceramic Caps**: Use X7R or X5R dielectric (10µF input, 22µF output)
- **18650 Cell**: Provides ~2000-3500mAh capacity
- **Battery Life**: Expect 2-4 weeks between charges (better than LDO)
- All capacitor negative terminals connect to GND
- Electrolytic capacitors are polarized - observe +/- markings
- Ceramic capacitors are non-polarized
- For permanent installation, consider soldering on a prototype board or custom PCB
- Keep LX switching node traces short and away from sensitive analog/digital signals
- SOT-25 package is smaller and simpler than TPS62046 MSOP-10


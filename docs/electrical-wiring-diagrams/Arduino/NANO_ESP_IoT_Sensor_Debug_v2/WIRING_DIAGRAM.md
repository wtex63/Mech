================================================================================
ESP32-S3 Nano Sensor Node - Detailed Wiring Diagram
XC6220A LDO + BME280 Version (v3.2)
================================================================================

POWER SUPPLY SECTION
────────────────────────────────────────────────────────────────────────────

Li-ion Battery
    (+) ──┬────────────────────► XC6220A LDO VIN
          │- Capacitors: 22µF (x2: input & output), 1000µF, 100µF (x3), 0.1µF (x4)
          │    Voltage Divider for Battery Monitoring
          ├─── 470kΩ ───┬─── 100kΩ ─── GND## Pin Connections
          │             │
          │             └──────────► D5/GPIO8 (ADC_PIN) ESP32-S3 Nano Pins
          │
    (-) ──┴────────────────────────► GND (Common)


XC6220A LDO Regulator (Ultra-Low Power: 1µA quiescent)
    VIN  ────────────────────────► Battery (+)
    GND  ────────────────────────► GND
    VOUT ──┬─────────────────────► ESP32-S3 3V3
           ├─────────────────────► BME280 VCCr)
           └─────────────────────► PIR VCC


================================================================================
SENSOR CONNECTIONS
================================================================================

BME280 ENVIRONMENTAL SENSOR (I2C Breakout Board)
────────────────────────────────────────────────────────────────────────────
    
    BME280 Breakout          ESP32-S3 Nano
    ───────────────          ─────────────
    VCC ─────────────────────► 3V3 (from XC6220A VOUT)2,3)
    GND ─────────────────────► GND
    SDA ─────────────────────► GPIO21 (I2C Data)
    SCL ─────────────────────► GPIO22 (I2C Clock)
    SDO ─────────────────────► (Float/GND/VCC for I2C address)Pins 4,9,10)
                               • GND = 0x76 (default)
                               • VCC = 0x77
-10 package):
    NOTES:connect to Pins 2,3)
    • BME280 breakout includes onboard decoupling capacitors
    • No external capacitors needed
    • I2C pullup resistors typically included on breakout boardommon GND (analog ground)
    • Adjust BME280_ADDRESS in code if using 0x77elow)
  Pin 6 (MODE)    ──── GND (power save mode) or VIN (fixed frequency)
 (SW)      ──── Switching node (to inductor)
PIR MOTION SENSOR (Breakout Board with Digital Output)
──────────────────────────────────────────────────────────────────────────── (-) / Common GND (power ground)
    
    PIR Breakout             ESP32-S3 Nano
    ────────────             ─────────────
    VCC ─────────────────────► 3V3 (from XC6220A VOUT)  TPS62046 SW (Pins 7,8) ────[10µH Bourns RL622]──── VOUT
    GND ─────────────────────► GND
    OUT ─────────────────────► D4/GPIO7 (PIR_PIN)
    
    GPIO7 (D4) Configuration:
    • Internal RTC pulldown enabled in software
    • Wake-on-HIGH via EXT1 interrupt
    • Breakout board includes filtering capacitors

    NOTES:
    • PIR breakout includes onboard componentsion 1 - Fixed 3.3V Output (Recommended - Simplest):
    • No external capacitors needed  VOUT ──── FB (Pin 5)  (Direct connection, no resistors)
    • Output is 3.3V logic compatible
utput voltage: 3.33V (fixed by internal reference)

================================================================================
USER INTERFACE
================================================================================ (Pin 5)

WAKE SWITCH (Manual Wake / Debug Mode Trigger)                   56kΩ
────────────────────────────────────────────────────────────────────────────                    │

    Wake Switch (SPST)       ESP32-S3 Nano
    ──────────────────       ─────────────3.40V
    Terminal 1 ──────────────► D3/GPIO6 (WAKE_SWITCH): use 108kΩ top / 56kΩ bottom
    Terminal 2 ──────────────► 3V3
    Pin 6 - MODE):
    ┌──────────────────────────────────────────────────┐ave mode (PFM at light load, better efficiency)
    │  CRITICAL: EXTERNAL PULLDOWN RESISTOR REQUIRED   │ Connect to VIN for fixed frequency PWM mode (less ripple, better for noise)
    └──────────────────────────────────────────────────┘  Recommendation: Connect to GND for battery operation (better efficiency)
    
    GPIO6 (D3) ──────[100kΩ]────────► GND
    ibution
    • 100kΩ resistor is MANDATORY for stable operation
    • Prevents floating GPIO during deep sleepUT (3.3V) ────┬──── VCC Rail (Breadboard)
    • Software RTC pulldown also enabled as backup
             [1000µF]  ← Additional bulk capacitor (optional)
 │
DEBUG MODE BUTTON18650 Cell (-) ──────────┴──── GND Rail (Breadboard)
────────────────────────────────────────────────────────────────────────────

    Built-in Button (GPIO0)  ESP32-S3 Nano
    ───────────────────────  ─────────────
    DEBUG_PIN ───────────────► GPIO0 (onboard button)           [100µF]  ← ESP32 power filter
                   │
    • Internal pulldown enabled
    • Hold during boot for debug mode               │
    • No external components needed


================================================================================n Filtering)
COMPLETE PIN SUMMARY
================================================================================
Rail
ESP32-S3 Pin    GPIO    Function            Connection
────────────    ────    ────────            ──────────         [100µF]  ← PIR power filter (optional)
D3              6       WAKE_SWITCH         Switch to 3V3 + 100kΩ to GND
D4              7       PIR_PIN             PIR Breakout OUT
D5              8       ADC_PIN             Voltage divider mid-point
GPIO21          21      BME280_SDA          BME280 SDA (I2C Data)
GPIO22          22      BME280_SCL          BME280 SCL (I2C Clock)
GPIO0           0       DEBUG_PIN           Onboard button resistors - no external components needed
Note: PIR hold time is ~2 seconds - code waits for this before enabling wake

================================================================================
COMPONENT VALUES
================================================================================
22:
VOLTAGE DIVIDER (Battery Monitoring)  VCC ────┬──── VCC Rail
────────────────────────────────────────────────────────────────────────────
    R1 (High side):  470kΩ ±1%      [100µF]  ← DHT22 power filter
    R2 (Low side):   100kΩ ±1%
    Ratio:           5.7 = (470k + 100k) / 100k  GND ────┴──── GND Rail
    Max Input:       ~19V (limited by ESP32 ADC max 3.3V × 5.7)
    Typical Range:   3.0V - 4.2V (Li-ion battery)ESP32 GPIO 4 (DHT_PIN)

WAKE SWITCH PULLDOWN  ← Pull-up resistor (REQUIRED for DHT22)
────────────────────────────────────────────────────────────────────────────
    R_pulldown:      100kΩ (MANDATORY)filter capacitor is optional and usually not needed
    Purpose:         Prevents floating GPIO6 during deep sleep
    Location:        GPIO6 (D3) to GND

```
================================================================================470kΩ ────┬──── ESP32 GPIO 5 (ADC_PIN)
POWER DISTRIBUTION
================================================================================onal)

    Battery (+) ──► XC6220A VIN
                       │
                    VOUT (3.3V)ltage Divider Ratio: (470k + 100k) / 100k = 5.7
                       ├──────────► ESP32-S3 Nano (3V3)
                       ├──────────► BME280 Breakout (VCC)50 Range: 2.5V-4.2V (well within range)
                       └──────────► PIR Breakout (VCC)
e raw battery voltage BEFORE the buck converter
    GND (Common) ───┬──────────► ESP32-S3 Nano (GND)
                    ├──────────► BME280 Breakout (GND)
                    ├──────────► PIR Breakout (GND)
                    ├──────────► XC6220A (GND)
                    ├──────────► 100kΩ Voltage Divider (GND)l Pull-down:
                    └──────────► 100kΩ Wake Switch Pulldown (GND)Rail
      [INPUT_PULLDOWN internal ~45kΩ]

================================================================================hen switch is open
HARDWARE CHANGES FROM PREVIOUS VERSIONS (3.3V) → Debug Mode on boot/reset
================================================================================  - Only checked on boot, does NOT wake from deep sleep

v3.2 (Current - BME280 + XC6220A)
    • PIR: D3/GPIO6 → D4/GPIO7
    • Wake Switch: D6/GPIO9 → D3/GPIO6Uses Internal Pull-down:
    • Sensor: DHT22 → BME280 (I2C)SP32 GPIO 6 (WAKE_SWITCH) ──── Switch ──── VCC Rail
    • Removed: 10µF PIR cap (on breakout)
    • Removed: 100nF BME280 cap (on breakout)
    • Added: Pressure sensing capability(0V) during deep sleep
    • Power: XC6220A LDO (1µA quiescent)- Pressing switch connects to VCC → HIGH (3.3V) → triggers wake from deep sleep

v2.0 (Previous - DHT22)
    • PIR: D3/GPIO6
    • Wake Switch: D6/GPIO9
    • Sensor: DHT22 (digital single-wire)
    • Required: 10µF cap on PIR power## Breadboard Layout Recommendations


================================================================================──────────────────────────────┐
NOTES AND WARNINGS 18650 Cell ──[TPS62046 Buck]── VCC Rail (3.3V) ════════════     │
================================================================================         │

⚠️  CRITICAL REQUIREMENTS:  [100µF]     │
    1. 100kΩ pulldown on GPIO6 (D3) to GND is MANDATORY       │         │
    2. BME280 I2C address must match code (default 0x76)─────┴───┬─────┴────┐  ┌───┴────┐  │
    3. All grounds must be common              │    TPS62046 Buck    │  ESP32   │  │ DHT22  │  │
    4. XC6220A output voltage must be 3.3V variant│                │    Converter        │   NANO   │  │ Sensor │  │
┬──┴────┬─────┘  └───┬────┘  │
✓  SIMPLIFIED DESIGN:│                                   │       │            │         │
    • No external capacitors on BME280 (breakout includes them)┌───┴────┐                      │     [0.1µF]      [0.1µF]     │
    • No external capacitors on PIR (breakout includes them)
    • I2C pullups included on BME280 breakout
    • PIR filtering included on breakout

💡 TESTING:
    • Measure voltage divider output: should be ~3.7V for 3.7V battery
    • Verify BME280 I2C address with scanner sketch
    • Check GPIO6 has stable LOW when switch open (100kΩ pulldown working) │
    • Confirm PIR output goes HIGH on motion──┘

================================================================================


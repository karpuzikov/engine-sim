# Engine Simulator
![Alt text](docs/public/screenshots/screenshot_v01.png?raw=true)
---
# Engine Simulator has moved!

To get the newest releases of the game, [click here](https://github.com/Engine-Simulator/engine-sim-community-edition).
---

## What is this?

This is a real-time internal combustion engine simulation **designed specifically to produce engine audio and simulate engine response characteristics.** It is NOT a scientific tool and cannot be expected to provide accurate figures for the purposes of engineering or engine tuning.

<!-- motortown:start -->
## Motor Town engines

Engine scripts for every engine of the game [Motor Town](https://store.steampowered.com/app/1369670/Motor_Town_Behind_The_Wheel/), built from the real engine of each vehicle the game's vehicles are based on.

- Scripts: `assets/engines/motortown/<engine id>.mr`. To run one, change the third line of `assets/main.mr` to `import "engines/motortown/<engine id>.mr"`.
- Data with a source link per value: `tools/motortown/motortown_engines.json`.
- Scripts and this section are generated: `python tools/motortown/generate_engines.py`.

Every value in a script carries a comment: **SOURCED** (cited source), **ESTIMATE** (unsourced estimate) or **PLACEHOLDER** (nothing found, generic default below). Placeholders exist so every engine runs; replace them as data is found.

Diesels use this fork's compression ignition (`diesel_injection_pump`, `diesel_fuel`); the Detroit 6V92TA and the Vespa use its two-stroke support (`firings_per_cycle`, `lobes_per_cycle`, `piston_port_lobe`, intake `supply_pressure`).

Status (headless test, 2026-11-13): 67 of 68 scripts start, idle and rev. The Honda CB250 twin does not start yet. Idle speeds: diesels 680-770 rpm (governor), petrol engines 900-1400 rpm and small engines up to 2000 rpm (placeholder idle air); the Vespa idles near 3700 rpm (placeholder crankcase pressure).

### Placeholders

Crank, piston and rod masses, inertia, intake and exhaust flow rates and volumes have no sources for any engine: they are scaled from upstream's Audi 2.2 i5 example by displacement (or bore for pistons and rods). Vehicle and gearbox are generic. Timing curve is upstream's i5 curve stretched to the redline. Fixed placeholders:

| Placeholder | Value |
|---|---|
| compression_ratio_petrol | 9.0 |
| compression_ratio_diesel | 17.0 |
| redline_petrol_rpm | 6000 |
| redline_diesel_rpm | 2400 |
| rod_length_to_stroke_ratio | 1.75 |
| rod_length_to_stroke_ratio_flat_engines | 2.0 |
| compression_height_to_bore_ratio | 0.4 |
| cam_duration_at_50_thou_deg_petrol | 210 |
| cam_duration_at_50_thou_deg_diesel | 200 |
| cam_lift_thou_petrol | 400 |
| cam_lift_thou_diesel | 350 |
| lobe_separation_deg | 112 |
| exhaust_primary_length_inch | 10.0 |
| idle_air_k_carb_per_litre | 0.7 |
| idle_air_k_carb_extra | 1.5 |
| starter_speed_rpm | 400 |
| simulation_frequency | 20000 |
| diesel_idle_speed_rpm | 650 |
| diesel_injection_timing_deg_btdc | 4 at idle to 12 at the redline |
| diesel_fuel_conversion_efficiency | 0.4 |
| two_stroke_crankcase_scavenging_pressure_atm | 1.3 |
| two_stroke_blower_pressure_atm | 1.5 |
| two_stroke_exhaust_port_open_deg_before_bdc | 85 |
| two_stroke_transfer_port_open_deg_before_bdc | 60 |
| uniflow_intake_port_open_deg_before_bdc | 48 |
| uniflow_exhaust_valve_center_deg_before_bdc | 15 |
| uniflow_exhaust_duration_at_50_thou_deg | 140 |
| vehicle_mass_kg_petrol | 1500 |
| vehicle_mass_kg_diesel | 12000 |

### Missing information

Every engine-sim value without a source. The generated scripts use an unsourced estimate or a generic placeholder for these.
Exhaust (header and pipe lengths, muffler volumes) is missing for every engine and is not listed per row.

| Engine | Used by | Missing (no source) |
|---|---|---|
| Ford flathead V8 221 (1932 V8-18) | 1932 Ford 5-Window Coupe | power rpm, torque, torque rpm, redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Willys L134 Go Devil I4 | 1945 Willys MB 'Jeep' | redline, cam duration, cam lift, intake valve, exhaust valve |
| Ford flathead V8 239 (V8-8RT, 1948 F-1) | 1948 Ford F-1 | power rpm, torque rpm, redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Volkswagen Type 1 1131 cc flat-four | 1950 Volkswagen Transporter | torque, redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Chevrolet 283 small-block V8 (2-bbl) | 1964 Chevrolet Impala, 1967 Chevrolet C-10 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| BMC A-series 1275 cc (Cooper S) | 1965 Austin Mini Cooper | cam duration, cam lift, intake valve, exhaust valve |
| Chevrolet 350 small-block V8 (L48, 1969) | 1969 Chevrolet Camaro SS | redline, cam duration, cam lift, intake valve, exhaust valve |
| Chevrolet 307 small-block V8 | 1969 Chevrolet Nova | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Nissan L24 I6 | 1969 Nissan Fairlady Z | power, redline, cam duration, cam lift |
| Continental LDT-465 multifuel I6 (M35A2) | 1970 GMC M35 | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Chevrolet 350 small-block V8 (truck, 1971) | 1971 Chevrolet P30 Step Van | cam duration, cam lift, intake valve, exhaust valve |
| Volkswagen Type 4 1679 cc flat-four | 1972 Volkswagen Transporter | power rpm, torque, torque rpm, redline, rod length, cam duration, cam lift |
| Volkswagen Type 1 1584 cc flat-four | 1974 Volkswagen Type 181 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Chrysler 318 LA V8 | 1975 Dodge Coronet, 1981 Dodge Diplomat, 1986 Dodge Ram Van | power, torque, torque rpm, redline, cam duration, cam lift, intake valve, exhaust valve |
| Chrysler 360 LA V8 | 1979 Dodge Ram Van | torque, redline, cam duration, cam lift, intake valve, exhaust valve |
| Chevrolet 305 small-block V8 | 1980 GMC Vandura | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Detroit Diesel 6V92TA two-stroke V6 | 1980 MCI MC-9 | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Citroën 602 cc flat-twin (2CV6) | 1981 Citroën 2CV | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Ford 302 (5.0) small-block V8 | 1982 Ford F-150 XL, 1983 Ford LTD Country Squire | bank angle, rod length, cam duration, cam lift, intake valve, exhaust valve |
| VAZ-2106 1.6 L I4 | 1982 Lada 2107 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Nissan MA10S 987 cc I4 | 1983 Nissan Micra K10 | firing order, rod length, cam duration, cam lift |
| Mercedes-Benz OM 422 V8 diesel | 1983 Steinwinter Supercargo 2040 | bank angle, torque rpm, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Porsche 3.2 L flat-six (930/20, 911 Carrera) | 1984 Porsche 911 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Cummins NTC-350 Big Cam I6 | 1985 Freightliner FLA | torque, torque rpm, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Subaru EK23 544 cc I2 (four-stroke) | 1985 Subaru Sambar | firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Lamborghini L503 5.2 V12 (LM002) | 1986 Lamborghini LM002 | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Buick 3.8 SFI turbo V6 (LC2, GNX) | 1987 Buick GNX | redline, rod length, intake valve, exhaust valve |
| Oldsmobile 307 V8 (LV2) | 1987 Cadillac Fleetwood | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Mack E6-350 I6 | 1987 Mack R-Series | compression ratio, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Scania DSC11 I6 | 1987 Scania 113H | power rpm, redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Navistar DT466 I6 | 1989 International 3800 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Mazda B6ZE(RS) 1.6 I4 | 1989 Mazda MX-5 | firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Nissan RB26DETT I6 | 1989 Nissan Skyline GT-R | cam lift, intake valve, exhaust valve |
| Toyota 22R-E 2.4 I4 | 1990 Toyota Pickup | cam duration, cam lift, intake valve, exhaust valve |
| BMW S14B23 2.3 I4 (E30 M3) | 1991 BMW M3 | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Lancia 2.0 16v turbo I4 (Delta HF Integrale Evo) | 1992 Lancia Delta HF Integrale Evo | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Toyota 2JZ-GTE 3.0 I6 | 1993 Toyota Supra | cam duration, cam lift, intake valve, exhaust valve |
| Ford 4.6 Modular 2V SOHC V8 | 2003 Ford Crown Victoria, 2003 Lincoln Town Car Stretched Limousine | cam duration, cam lift, intake valve, exhaust valve |
| Iveco Cursor 8 I6 | 2005 Irisbus Citelis | power rpm, torque, torque rpm, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| GM 5.3 Vortec V8 (LY5/LMG, 2007) | 2007 Chevrolet Tahoe | bank angle, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Ford 5.4 Triton 2V SOHC V8 | 2008 Ford E-Series | redline, cam duration, cam lift, intake valve, exhaust valve |
| Ford 2.5 Duratec RS turbo I5 (Volvo B5254) | 2009 Ford Focus RS | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Renault DXi 13 480 I6 | 2009 Renault Magnum 480 | compression ratio, power rpm, torque rpm, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| MAN D0836 LOH I6 | 2009 TEMSA Opalin | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Lamborghini L539 6.5 V12 | 2011 Lamborghini Aventador LP 700-4 | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Chrysler 5.7 HEMI V8 | 2012 Dodge Charger | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Mazda Skyactiv-G 2.5 I4 | 2012 Mazda CX-5 | firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Ford 1.6 Ti-VCT Sigma I4 | 2013 Ford Fiesta | firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Mercedes-Benz OM 934 5.1 I4 | 2014 Mercedes Unimog U5023 | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Volvo D13 I6 | 2014 Volvo VNL | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Yamaha YZF-R1 998 cc crossplane I4 (2015) | 2015 Yamaha YZF R1 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| BMW N55B30T0 3.0 turbo I6 (M2) | 2016 BMW M2 | firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Ford 5.4 Triton 3V SOHC V8 | Ford F350-F550 Dually | cam duration, cam lift, intake valve, exhaust valve |
| Ford Kent 1.6 crossflow I4 (Formula Ford) | Formula 1600 | power rpm, torque, torque rpm, rod length, cam duration, intake valve, exhaust valve |
| Cummins ISX15 I6 | Peterbilt 389 | compression ratio, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Piaggio Vespa PX150 two-stroke single | Piaggio Vespa | rod length, cam duration, cam lift, intake valve, exhaust valve |
| Honda GX160 single | Race Car Kart | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Scania DC9 9.3 L I5 | Scania P-Series | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Scania DC13 12.7 L I6 | Scania P-Series, Scania PRT 380 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Volvo D9B 9.4 L I6 | Volvo FM | firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Cummins NHRBS (Beck DH1040) | 1955 Beck 'Semi' Deck & Half Cruiser | compression ratio, power, torque, torque rpm, redline, firing order, cam duration, cam lift, intake valve, exhaust valve |
| Caterpillar D343T (769) | 1966 Caterpillar 769 | compression ratio, power, power rpm, torque, torque rpm, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Fiat/Iveco 8060.05 (Zeta) 5.9 L | 1977 Iveco Zeta | compression ratio, power rpm, torque, torque rpm, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Volvo Penta TAD881-VE (Konecranes SMV 25-1200 C) | 2019 Konecranes SMV 25-1200 C | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Daewoo/GM F8C 0.8 I3 (Labo) | 2014 Daewoo Labo | redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Honda CB250 K0-K5 parallel twin | Honda CB250 | redline, rod length, cam duration, cam lift, intake valve, exhaust valve |
| Ford Dorset 363 I6 diesel (F-600, tuned to game 190 hp) | 1967 Ford F-600 | compression ratio, power rpm, torque, torque rpm, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |
| FPT/Iveco F1C 3.0 I4 diesel (Gulliver stand-in, tuned to game 140 hp) | 2009 Tecnobus Gulliver | compression ratio, power rpm, torque, torque rpm, redline, firing order, rod length, cam duration, cam lift, intake valve, exhaust valve |

### Game vs reality

Where the game's engine (name, power, fuel) does not match the real vehicle's engine used here.

| Game vehicle | Real vehicle | Game engine | Real engine | Mismatch |
|---|---|---|---|---|
| Air City | 2005 Irisbus Citelis | Bus 230HP (Diesel) | Iveco Cursor 8 I6 | power 230 hp in game vs 290 hp real |
| Atlas 4x2 Semi | 1987 Scania 113H | Heavy-Duty 260HP (Diesel) | Scania DSC11 I6 | power 260 hp in game vs 360 hp real |
| Bongo | 1972 Volkswagen Transporter | I4 90HP (Gasoline) | Volkswagen Type 4 1679 cc flat-four | power 90 hp in game vs 66 hp real; layout I4 in game vs H4 real |
| Bora | 1985 Subaru Sambar | I4 90HP (Gasoline) | Subaru EK23 544 cc I2 (four-stroke) | power 90 hp in game vs 34 hp real; layout I4 in game vs I2 real |
| Boxy | 1971 Chevrolet P30 Step Van | V8 180HP (Gasoline) | Chevrolet 350 small-block V8 (truck, 1971) | power 180 hp in game vs 250 hp real |
| Brutus Ambulance | 2014 Mercedes Unimog U5023 | Medium-Duty 190HP (Diesel) | Mercedes-Benz OM 934 5.1 I4 | power 190 hp in game vs 228 hp real |
| Campy | 1979 Dodge Ram Van | Medium-Duty 190HP (Diesel) | Chrysler 360 LA V8 | fuel Diesel in game vs petrol real |
| Cheetah Mk1 | 1980 MCI MC-9 | Bus 400HP (Diesel) | Detroit Diesel 6V92TA two-stroke V6 | power 400 hp in game vs 277 hp real |
| Compacty | Scania P-Series | Medium-Duty 190HP (Diesel) | Scania DC9 9.3 L I5 | power 190 hp in game vs 280 hp real |
| Cora | 2016 BMW M2 | V8 240HP (Gasoline) | BMW N55B30T0 3.0 turbo I6 (M2) | power 240 hp in game vs 365 hp real; layout V8 in game vs I6 real |
| Dabo | 2014 Daewoo Labo | I4 50HP (Gasoline) | Daewoo/GM F8C 0.8 I3 (Labo) | power 50 hp in game vs 38 hp real; layout I4 in game vs I3 real |
| Dory | 1948 Ford F-1 | V8 140HP (Gasoline) | Ford flathead V8 239 (V8-8RT, 1948 F-1) | power 140 hp in game vs 100 hp real |
| Duke | 1987 Buick GNX | V8 180HP (Gasoline) | Buick 3.8 SFI turbo V6 (LC2, GNX) | power 180 hp in game vs 276 hp real; layout V8 in game vs V6 real |
| Elisa | 2003 Ford Crown Victoria | V8 180HP (Gasoline) | Ford 4.6 Modular 2V SOHC V8 | power 180 hp in game vs 224 hp real |
| Enfo GT | 2009 Ford Focus RS | V8 320HP (Gasoline) | Ford 2.5 Duratec RS turbo I5 (Volvo B5254) | layout V8 in game vs I5 real |
| Essam | 1969 Nissan Fairlady Z | I4 150HP (Gasoline) | Nissan L24 I6 | layout I4 in game vs I6 real |
| Formula SCM | Formula 1600 | I4 150HP (Gasoline) | Ford Kent 1.6 crossflow I4 (Formula Ford) | power 150 hp in game vs 104 hp real |
| Fortem | 1984 Porsche 911 | V8 240HP (Gasoline) | Porsche 3.2 L flat-six (930/20, 911 Carrera) | layout V8 in game vs H6 real |
| Fox | 1945 Willys MB 'Jeep' | I4 90HP (Gasoline) | Willys L134 Go Devil I4 | power 90 hp in game vs 60 hp real |
| Gunthoo Police | Honda CB250 | Bike 50HP (Gasoline) | Honda CB250 K0-K5 parallel twin | power 50 hp in game vs 30 hp real |
| Jemusi Dump | 1970 GMC M35 | Medium-Duty 190HP (Diesel) | Continental LDT-465 multifuel I6 (M35A2) | power 190 hp in game vs 130 hp real |
| Kira Box | 1977 Iveco Zeta | Medium-Duty 190HP (Diesel) | Fiat/Iveco 8060.05 (Zeta) 5.9 L | power 190 hp in game vs 138 hp real |
| Koma | 1965 Austin Mini Cooper | I4 90HP (Gasoline) | BMC A-series 1275 cc (Cooper S) | power 90 hp in game vs 76 hp real |
| Kuda Container 6x2 | 2009 Renault Magnum 480 | Heavy-Duty 350HP (Diesel) | Renault DXi 13 480 I6 | power 350 hp in game vs 480 hp real |
| Liliput | 2009 Tecnobus Gulliver | Bus 140HP (Diesel) | FPT/Iveco F1C 3.0 I4 diesel (Gulliver stand-in, tuned to game 140 hp) | FPT/Iveco F1C 3.0 I4 diesel (stand-in), tuned to game 140 hp |
| Lobo | 1983 Steinwinter Supercargo 2040 | Heavy-Duty 350HP (Diesel) | Mercedes-Benz OM 422 V8 diesel | power 350 hp in game vs 275 hp real |
| Longhorn Rollback | 2014 Volvo VNL | Heavy-Duty 350HP (Diesel) | Volvo D13 I6 | power 350 hp in game vs 460 hp real |
| Magis | 1993 Toyota Supra | V8 240HP (Gasoline) | Toyota 2JZ-GTE 3.0 I6 | layout V8 in game vs I6 real |
| Micky | 1983 Nissan Micra K10 | I4 90HP (Gasoline) | Nissan MA10S 987 cc I4 | power 90 hp in game vs 51 hp real |
| Mitage | 2012 Mazda CX-5 | V8 180HP (Gasoline) | Mazda Skyactiv-G 2.5 I4 | layout V8 in game vs I4 real |
| Monarch | 1987 Cadillac Fleetwood | V8 180HP (Gasoline) | Oldsmobile 307 V8 (LV2) | power 180 hp in game vs 140 hp real |
| Neo | 1992 Lancia Delta HF Integrale Evo | I4 150HP (Gasoline) | Lancia 2.0 16v turbo I4 (Delta HF Integrale Evo) | power 150 hp in game vs 210 hp real |
| Nuke | 1981 Dodge Diplomat | V8 180HP (Gasoline) | Chrysler 318 LA V8 | power 180 hp in game vs 150 hp real |
| Panther | 1989 Mazda MX-5 | I4 150HP (Gasoline) | Mazda B6ZE(RS) 1.6 I4 | power 150 hp in game vs 116 hp real |
| Police | 2012 Dodge Charger | V8 240HP (Gasoline) | Chrysler 5.7 HEMI V8 | power 240 hp in game vs 370 hp real |
| Police Interceptor 1 | 1975 Dodge Coronet | V8 180HP (Gasoline) | Chrysler 318 LA V8 | power 180 hp in game vs 150 hp real |
| Pulio | 1967 Ford F-600 | Medium-Duty 190HP (Diesel) | Ford Dorset 363 I6 diesel (F-600, tuned to game 190 hp) | Ford Dorset 363 I6 diesel, tuned to game 190 hp |
| Ranchy | 1967 Chevrolet C-10 | V8 140HP (Gasoline) | Chevrolet 283 small-block V8 (2-bbl) | power 140 hp in game vs 195 hp real |
| Raton | 2011 Lamborghini Aventador LP 700-4 | V12 400HP (Gasoline) | Lamborghini L539 6.5 V12 | power 400 hp in game vs 690 hp real |
| Raven | 1932 Ford 5-Window Coupe | V8 320HP (Gasoline) | Ford flathead V8 221 (1932 V8-18) | power 320 hp in game vs 65 hp real |
| Savannah | 1974 Volkswagen Type 181 | I4 90HP (Gasoline) | Volkswagen Type 1 1584 cc flat-four | power 90 hp in game vs 46 hp real; layout I4 in game vs H4 real |
| SCM Kart One | Race Car Kart | Kart 10HP (Gasoline) | Honda GX160 single | power 10 hp in game vs 5 hp real |
| SRT | Scania PRT 380 | Heavy-Duty 260HP (Diesel) | Scania DC13 12.7 L I6 | power 260 hp in game vs 370 hp real |
| Stagon | 1983 Ford LTD Country Squire | V8 180HP (Gasoline) | Ford 302 (5.0) small-block V8 | power 180 hp in game vs 135 hp real |
| Stella | 2013 Ford Fiesta | V8 140HP (Gasoline) | Ford 1.6 Ti-VCT Sigma I4 | power 140 hp in game vs 120 hp real; layout V8 in game vs I4 real |
| Stinger | 1969 Chevrolet Camaro SS | V8 140HP (Gasoline) | Chevrolet 350 small-block V8 (L48, 1969) | power 140 hp in game vs 300 hp real |
| Tavan Ambulance | 1980 GMC Vandura | V8 240HP (Gasoline) | Chevrolet 305 small-block V8 | power 240 hp in game vs 140 hp real |
| Townie | 1950 Volkswagen Transporter | V8 140HP (Gasoline) | Volkswagen Type 1 1131 cc flat-four | power 140 hp in game vs 24 hp real; layout V8 in game vs H4 real |
| Trophy Taxi | 1982 Lada 2107 | I4 90HP (Gasoline) | VAZ-2106 1.6 L I4 | power 90 hp in game vs 75 hp real |
| Tuscan | 1969 Chevrolet Nova | V8 140HP (Gasoline) | Chevrolet 307 small-block V8 | power 140 hp in game vs 200 hp real |
| Vista | 1989 Nissan Skyline GT-R | V8 240HP (Gasoline) | Nissan RB26DETT I6 | layout V8 in game vs I6 real |
| Voltex | 1990 Toyota Pickup | V8 140HP (Gasoline) | Toyota 22R-E 2.4 I4 | power 140 hp in game vs 114 hp real; layout V8 in game vs I4 real |
| Zero | 2015 Yamaha YZF R1 | Bike i4 100HP (Gasoline) | Yamaha YZF-R1 998 cc crossplane I4 (2015) | power 100 hp in game vs 197 hp real |
| Zino | 1991 BMW M3 | V8 140HP (Gasoline) | BMW S14B23 2.3 I4 (E30 M3) | power 140 hp in game vs 195 hp real; layout V8 in game vs I4 real |
<!-- motortown:end -->

## How do I install it?

This is a code repository and might not look like other software that you're used to downloading and installing (if you're not familiar with programming). To download a ready-to-use version of the application, navigate to the [releases page](https://github.com/ange-yaghi/engine-sim/releases), find the most recent release (ex. `v0.1.5a`), click "Assets" and download the .zip file with a name that starts with `engine-sim-build`. Unzip this file, then run `bin/engine-sim-app.exe`. The simulator should then start normally.

Check out [our Frequently Asked Questions](https://github.com/ange-yaghi/engine-sim/wiki/Frequently-Asked-Questions) if you need more details.

## How do I use it?

The UI is extremely minimalistic and there are only a few controls used to interact with the engine:

| Key/Input | Action |
| :---: | :---: |
| A | Toggle ignition |
| S | Hold for starter |
| D | Enable dyno |
| H | Enable RPM hold (see below for instructions) |
| G + Scroll | Change hold speed |
| F | Enter fullscreen mode |
| I | Display dyno stats in the information panel |
| Shift | Clutch (hold spacebar at the same time to slowly engage/disengage) |
| Up Arrow | Up Gear | 
| Down Arrow | Down Gear | 
| Z + Scroll | Volume |
| X + Scroll | Convolution Level |
| C + Scroll | High frequency gain |
| V + Scroll | Low frequency noise |
| B + Scroll | High frequency noise |
| N + Scroll | Simulation frequency |
| M | Increase view layer |
| , | Decrease view layer |
| Enter | Reload engine script |
| Escape | Exit the program |
| Q, W, E, R | Change throttle position |
| Space + Scroll | Fine throttle adjustment |
| 1, 2, 3, 4, 5 | Simulation time warp |
| Tab | Change screen |

### Using the RPM hold
The RPM hold feature will hold the engine at a specific RPM and also measure the engine's horsepower and torque at that RPM. You can enable RPM hold by pressing the `H` key. **You must then enable the dynomometer** (press the `D` key) in order for the RPM hold to take effect. To change the hold speed, hold the `G` key and scroll with the mouse wheel. The RPM hold will be shown on the `DYNO. SPEED` gauge in the lower left of the screen.

## Why is the code so sloppy?

I wrote this to demo in a [YouTube video](https://youtu.be/RKT-sKtR970), not as a real product. If you would like it to become a usable product please reach out to me or join my Discord (link can be found in the description of the aforementioned YouTube video). I use this codebase for my own purposes and so it might change frequently and without warning.

## How do I build it? (Ignore this section if you're not a developer!)
**Note: this project currently only builds on Windows!**

### Step 1 - Clone the repository
```git clone --recurse-submodules https://github.com/ange-yaghi/engine-sim```

### Step 2 - Install CMake
Install the latest version of CMake [here](https://cmake.org/) if it's not already installed.

### Step 3 - Install Dependencies
You will need to install the following dependencies and CMake will need to be able to locate them (ie. they need to be listed on your PATH):

    1. SDL2
    2. SDL2_image
    3. Boost (make sure to build the optional dependencies)
    4. Flex and Bison

### Step 4 - Build and Run
From the root directory of the project, run the following commands:

```
mkdir build
cd build
cmake ..
cmake --build .
```

If these steps are successful, a Visual Studio solution will be generated in ```build```. You can open this project with Visual Studio and then run the ```engine-sim-app``` project. If you encounter an error telling you that you're missing DLLs, you will have to copy those DLLs to your EXE's directory.

## Patreon Supporters

This project was made possible by the generous donations of the following individuals!

### Grease Monkeys

|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|
|-|-|-|-|-|
|Devin@Hondatuningsuite|nut|Devin C Martinez|WelcomeCat|Saints Sasha|
|Ida 8858|Emily|Steelorse |Kruddy|Sgt. Fluff|
|darcuter|FatFluffyFox|Benton1234|Jim C K Flaten|The Zuck|
|Blade Skydancer|Ye' old apple|Hayden Henderson|AlphaX|Lucas Martins Bündchen|
|Jay Dog|damo|IBS-IS-CRAP|Snowy|Noah Greenberg|
|Eisberg|Brendan M.|Alex Layton|Lukas Bartee|Thibaut Dubuisson|
|The Cheeze Ity|JoeJimTom|MichaelB450|Björn|Bartdavy|
|sasha bandelier|Caleb Black|COOKIES|Andrew Cooper|asimo3089|
|Vim Wizard|Kevin Arsenault|Carl Linden|Kele Tappi|Kroklethon|
|labourateur|viperfan7|SlimmyJimmy|Jason Becker|Sascha Kamp|
|ves|Supernalboot |BeamNG|Paul Harrison|Tyler Russell (Nytelife26)|
|nicholas jacobs|DrDotMadness|AVeryPlainTyler|Zach Perez|Paul Schaefer|
|Clay Bauer|CR33DYM0N14|julien nadeau|Patt313|Philip Edwards|
|RegularRuby670|Mateusz Ładosz|FémLol Stúdió|Crazy Yany|Elden|
|Tristan Walker|Matthew McDonald|Jan-Sander Huiting|Mitchell Almstedt|Dylan Lebiedz|
|Name Here|LoganBoi FNAF|Epic Randomness|MrPiThon|mike |
|dung|Alvaro ArroyoZamora|Skinna Godwin|BeppoBarone|レナVA|
|Sabata |Brady Fulham|Powerpuncher |NK10K|Gavin Osowski|
|Orbitstrider|Steven Doyle|Jaksu2696|Toni |Devin Abolins|
### Tuners

|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|
|-|-|-|-|-|
|Boosted Media|Matthew McLennan|Venican|Lyan le Golmuth|Alberto R.|
|BetaToaster|Akira Takemoto|J Anderson|Apolly007|LexLuther|
|xilophor|Robert K|viktor lind|Adrian Kucinski|sarowie .|
|Chris Fischer|Marlod|Chase Hansen|Aidan Szalanski|Andrew Taylor|
|Jason Hwang|Juuso Natunen|Ian Moss|PickleRick |Beljim46|
|RSOFT92|UCD|Sped|OldManJenkins|James Hart|
|Kalle Nilsson|XxBrasta455xX |Colin Sandage|Dakota Mackinnon|Carter Kopp|
|Jakub Kozak|CJ Plessas|Loizeau|Charles Mills|YellowLight|
|Didrik Esbjug|Alessandro Dal Pino|Carter Williams|Robert D|Cadence Plume|
|BLANK|Provenance EMU|Dylan Engler|Nathan Rojas|Cornelius|
|Acid|larsloveslegos|Maxime Desages|GM|BreadForMen|
|Devin Freeman|Lieven RYCKEBOER|Amelia Taylor|Jelle Plukker|sodmo |
|Jimmy Briscoe|Cirithor|Martin .K|DMartland|Lucas Diem|
|Richard Budíček|Jack Sheppeard|Meemen|Anderson Huynh|NPException|
|Mattia Villa|C|AIDAN POWELL|Brenn_the_Otter|Lane Mosier|
|Ceze |oranjest1|Jw|ISON |Mathew Graham|
|MACHINA|John Crowell|Asher Blythe|Cronos Skies|Matt Amott|
|CpTKugelHagel|Simon Krayer|Caleb Bek|Monster Man25|GeneralMoineau|
|EsuKurimu|Caleb Sartin|Jared L.|Hunter Wood|Ben Poole|
|Steven Victoria|Jordan Zondlak|Agelessgod|Christopher Fahs|Jonathan Vincent|
|Dalton Guillot|Simon Stojanovic|Andrew Urbanczyk|deniaL|Tyler Hughes|
|vPam |Justin Kruithof|Curtis C Coomber|Sawyer Clark|Mike Hart|
|Ciro Rancourt|Miles Guo|Rewind |E=mc^2|Keaton Call|
|J.Es|Jeremy B|Chance Hall|Jack Tompkins|Race Sim Studio|
|Quentin ZAOUI|Floyd Henderson|James Haylow|Milkshiekh |Wyatt Todd|
|User 2820|Leon Schutte|CYBERBUG_JR|sebiii|Keegan|
|Victor Cosiuga|Rolly !|Elias Pettersson|Tyson Makovec|Bill McDermott|
|Phontonic|Simon Armstrong|avec |KidozyGAME (Dead)|Stephan Cote|
|Justin Biggerstaff|Jabba Jubba|notD34THNIGHT|Inventor|Wesley Bear|
|Supersonic2510|Pixel|Simon Bernhardt|Bas Vangermeersch|ToyotaCipra|
|kyle crawford|ApatheticWood|Ben Vaughn|Erich Westhoven|Zack Myers|
|Tbjoern|Vetle Høgås|Derek Thom|Aaron Beck||
### Junior Mechanics

|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|
|-|-|-|-|-|
|Karol Szép|Leon Jordan|Nathan Higginson|Patrick F|Samuel Picard|
|Alexander Fritsch|Lucas Scarpi|Jack Humbert|G2Eneko|SweCreations|
|Marius Becker|Cedric Wille|infernap12 |Julian Dinges|Wamuthas|
|Alex Mason|Hawar Karem|Melonenstrauch|Jacek Dębski|Alex Eastman|
|Darren Taing|Po Wang|Giorgio Iannucci|Levis|Eden|
|Alin Chiparatu|Arjun Mandakath|A.M. |Dylan Ryan|Noah Entrekin|
|GT130|Josh D|generic|Henrik Cohrs|Nic Yetter|
|Dan Fredriksen|153AN1MJ|Rasmus|EpicEcho|Kaur Hendrikson|
|Maddox Partridge|L33TIFY_|Zack Fletcher|teiiio|Mike Zaite|
|Evan Sonin|Christopher Zimmerman|PrefacedVase |funtomr|Triton Alabaster|
|appelpie|Julien Ferluc|AnomalousFerret_|Miles Orozco|Spencer Teeter|
|ThatCanadian|Harry Prabowo|Dylan Rogerson|Jaedyn Allen|Zephyr Sefira|
|Alexander Stone|Mason Little|Wojciech Czop|ryzen5 |Kosta Diamantis|
|Karol Stodolak|Tim van der Linde|Loïc Ruttner|jonthefuzz|AsgarK|
|James Morgan|Elijah |1ntl|Tobias Johansson|Mome |
|P|SOPA_|Shingekuro|Sean King|Russell Marsh|
|Alyx Ranas|Naters305 |ChrisakaMrXD |Nic |sean|
|Zach Hagedorn|Jhon lenon|Everett Butts|Kyan|ranger Nation|
|Hiago Oliveira|Texi|MrRhody|Inglorious Bastard|Marty Mitchell|
|Justin Chao|ManuelS|Cornelius Rössing|Pedro Freire|Anthony Stuart|
|Hubba Nubba|Skychii|Joe Underwood|Xander_|Notbigdank|
|Sander D.|Lars Joosten|Danksa|Metrostation |Myles Wommack|
|Derrick Sampson|Corey Hannen|Matteo La Corte|Octothorp Obelus|David Baril|
|Soyuz Kafire|Ivan Coha|BigElbowski|Apolepth|Julian Krad|
|David Soulieres|Eric Huang|Léo Vias|Riccardo Mariani|Vic Viper|
|Shinkaaaa|Mumaransa |Michael Banovsky|Hendrik Voss|Inverted Blackhat|
|skipyC |Tobias Moor|jaky3 .|Clément LEGRAND|Ian C. Simpson|
|Challier|Jan Przemysław Drabik|Dsand23|Smooth DLX|The German Dude|
|CrazyEagle |Jordon Goodman|HenryWithaG .|Oscar Krula|Brayden Moore|
|Steven|Nall Wolfert|papajonk|Andrew|Ben Kingston|
|Julian Vogl|Maxime Lubrano|MrMekouil|Doudimme|Jacob Hultberg|
|Nolan Orloff|Mike|tobi9899 |Danila Frolkin|Xecotcovach|
|Aj|Carcar404|John Martin|Dominik Greinert|Lukas Stadler|
|Oliver Yang|sonax51|Marcel Kliment|Chris|David Rush|
|LethalVenom13|Dave Osterhoff|Anto1709|Ben|Morgan Munroe|
|Ivor Forrest|Sam Hopkins|Atte |Dax |William Bergström|
|homelessmeme|Thanleft|Zaxerg |Robeloox|Maximilian-Lukas Marz|
|Morgn|Seth Monteleone|playfulmean videos|Lanimations LA|Bram G|
|Benoit Fournier|Bernar Lepiller|Nicolas Baur|the |Snekers|
|Darkmount|Tobiasz Michalik|Aidas Ri|Daniel Postler|Skim_Beeblez|
|Impetus|Thunderbird324|Fred Joss|Krzysztof Radowski|Azerrty|
|Harrison Speck|Matt Baker|BigLynch|Markus Pelto|IMBIBE|
|James L Plummer|Rose Giles|Jonas Brekka|HASTRX|Lepoucehumain|
|Naomi Humin|qkrrudgks|Johann Gross|Janis Knappich|WhatTheDuck|
|테루|Glimple Bort|Jacob Tudisco|Tanner|Julian kaspi|
|nathan gould|Randal Rainis Kruus|Beppierre|Craig Martin|Thomas Bukovsky|
|Colaxe|Robert Oram|Matsuy15 L|Kacpe|Alex Sedlic|
|Mark Benson|Mhenn!|Anders Nelson|Dingus|Rustle|
|Marco Schulz|stratum |brochier gabriel|Thomas|brody of hillcountry|
|Thomas Afford|Brody Blaskie|Martien Gaming|Adrien MC|William A Grubbs|
|Trevo Ph.D.|Donovan Gibson|Polish R3t4rd|Keith Price|LAWL CAKE|
|Rhien Schultz|FireThrow13|Seraphim|Titus Standing|Matt Miklos|
|B Dub|Jonathan Ekman|Al Pomeroy|Vestii|Wil|
|adrian|Airatise|TJ Sinkoski|Shotts SilverStone|Reagan Carbaugh|
|WarAestheticsRebooted|Aidan Case|Casey Bryant Goodwin|Konrad|Adam Larcher|
|Kazar Xin Xiao|Riccardo Marcaccio|William S.|Francis Filion|Loïc |
|Kenny Deane|Blackspots|mike |MXT|Joshua Gibson|
|milky boi|Hagen|gunmaster929 |jgvan |Benny 282|
|Sean Wehner|Christian Poole|Ethan|Tsukiyama Shuu|Ooof_uhhh_haah|
|sano ken ch|Diego Martinez|Chuck|GalaxyFrogs|TheGeForce |
|Chriphost|Carthage|Greg L|Chipskate|Muhammed Mehmood|
|Hamilton Sjoberg|Amina Moh|vSiiFT|Jeremy Wren|Esteban Acosta|
|John A Ullenberg|Michael Morozov|Andrew Webberley|Nathaniel Lim|Aaron Ksicinski|
|Apocalypt|Josh batuzich|Ed|Hunter |Gene Brockoff|
|Redheadspellslinger.|Pablo Magariños|Nilz|Jose Manuel Silva Calvo|AJ|
|Ethan Wille |Aurora|Derek Shunia|Jan|Nope Mircea|
|Giancarlo Cestari|Tanner Edge|brad.|Connor Merrick|Martin Scholer|
|Deppy|Dan Smith|Tyson |Jac Comeau|Itemfinder |
|Tischer Games|Pedro Henrique|BeenWashedUp|martin wolff|Kurt Houben|
|Thomas Onslow|Brendan Puglisi|Kai Anquetil|Rudolph Ignatenko|CloudHackIX|
|Zach Carreau|Jonathan Vanderlyn|Krobivnov|ienergy|Leifster|
|Mikael Kaaronen|Glen|H.Helsing|ange|The Nobles|
|Johnathan Johnson|Juha Merentie|Jim Fares|Tom Marshall|Superferrariman|
|Zakary Zisa|JustTy|晟道 杜|Dnialibr Williams|Takumi Fujiwara|
|Koen van Hal|Jonathan Hill|Marco Siciliano|Kevindosenfutter|Angry Prawn|
|Natharic 67|Rafael Monteiro|Jacob Ashline|ChironTheFloof|Caleb Dauphinee|
|Tony |Zac L|AlainMoto FPV|eirik johan johnsen|Elderet|
|Miles Longmore|lemon head|Viccy|Casey|Kajetan Cupa|
|Conejero00|Bill Gricko|A cow wearing a turban|Danni Nowicki|Udo Schmidt|
|Tyler Swords|Constellation Gaming|Manimo|valentine|Jules Schattenberg|
|Brandon Crotts|Philipp Popetschnigg|Tiziano Della Fazia|goodgamer1109|Joshua Thomas|
|Jeff Testa|Avery Snyder|Josh Kern|Triptagram|Bayon Antoine|
|Iván Juárez Núñez|Amery Martinat|ElArGee|Cory Green|lucas Di lorenzo|
|Caleb Sandersier|||||

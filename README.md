# Ventilation Project

This repository contains designs and resources for a combined supply and exhaust ventilation system in a 152 sq.m. non-residential room with a ceiling height of 2.91 m. The project includes automatic calculation of the optimal number of diffusers and pressure losses along both supply and exhaust routes.

## Project Specifications

### Room Parameters
- **Room Area:** 152 m²
- **Room Dimensions:** 12.0 m × 12.67 m
- **Ceiling Height:** 2.91 m
- **Air Exchange Rate:** 6 air changes per hour (typical for office/commercial spaces)

### Supply Ventilation System (Red)
- **Supply Fan:** Ø315 mm channel fan
- **Processing Equipment:**
  - Silencer (Ø250mm for noise reduction)
  - Air filter
  - Heater (caloripher)
- **Main Supply Duct:** Ø250 mm initially, then transitions to Ø160 mm
- **Branch Ducts:** Ø125 mm
- **Supply Diffusers:** ДПУ-М 125 (automatically calculated quantity)

### Exhaust Ventilation System (Blue)
- **Exhaust Fan:** Ø250 mm channel fan
- **Main Exhaust Duct:** Ø160 mm
- **Branch Ducts:** Ø125 mm
- **Exhaust Grilles:** Ø125 mm (automatically calculated quantity)

## Features

### Automatic Calculations

The system automatically calculates:

1. **Optimal Number of Diffusers/Grilles**
   - Based on room volume and air exchange requirements
   - Considers recommended airflow per diffuser (150-250 m³/h for ДПУ-М 125)
   - Ensures comfortable air distribution
   - Result: 14 supply diffusers and 14 exhaust grilles

2. **Supply System Pressure Loss Calculations**
   - Friction losses in main ducts (both Ø250mm and Ø160mm sections)
   - Friction losses in branch ducts (Darcy-Weisbach equation)
   - Local losses in equipment:
     - Supply fan outlet
     - Silencer (Ø250mm)
     - Air filter
     - Heater (caloripher)
     - Duct transition (Ø250mm → Ø160mm)
     - Branch tees
     - Diffusers
   - Total pressure loss with 15% safety factor
   - Required supply fan pressure specification

3. **Exhaust System Pressure Loss Calculations**
   - Friction losses in main duct (Ø160mm)
   - Friction losses in branch ducts
   - Local losses:
     - Exhaust fan inlet
     - Branch tees
     - Exhaust grilles
   - Total pressure loss with 15% safety factor
   - Required exhaust fan pressure specification

4. **Air Velocities**
   - Supply main duct (Ø250mm section): ~6.2 m/s
   - Supply main duct (Ø160mm section): ~15.1 m/s
   - Supply branch ducts: ~4.3 m/s
   - Exhaust main duct: ~15.1 m/s
   - Exhaust branch ducts: ~4.3 m/s

## Usage

### Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Generate Ventilation Scheme

Run the generator script to create the ventilation scheme PNG:

```bash
python3 generate_ventilation_scheme.py
```

This will create `ventilation_scheme.png` with a complete schematic diagram of both supply and exhaust ventilation systems.

## Output

The generated scheme includes:

### Visual Components
- Room outline with precise dimensions (12.0m × 12.67m)
- **Supply system (RED color)**:
  - Supply fan (Ø315 mm) positioned outside the room (left side)
  - Processing equipment (silencer Ø250mm, filter, heater) in sequence
  - Supply duct starting at Ø250mm, transitioning to Ø160mm
  - 14 supply diffusers (ДПУ-М 125) at the top with branch ducts
- **Exhaust system (BLUE color)**:
  - Exhaust fan (Ø250 mm) positioned outside the room (right side)
  - Main exhaust duct (Ø160mm)
  - 14 exhaust grilles at the bottom with branch ducts
- Color-coded components with comprehensive legend
- Airflow direction indicators

### Technical Specifications Panel
- Room parameters (area, dimensions, height, volume)
- Air exchange rate and total airflow (~2654 m³/h)
- Complete equipment list for both systems
- Number of diffusers/grilles and airflow per unit
- Air velocities in all duct sections

### Pressure Loss Analysis Panel
- **Supply System** detailed breakdown:
  - Main duct friction losses (Ø250mm + Ø160mm sections)
  - Branch duct friction losses
  - Equipment losses (fan outlet, silencer, filter, heater)
  - Transition loss (Ø250mm → Ø160mm)
  - Local losses (tees, diffusers)
  - Total: ~2851 Pa
  - Required fan pressure: ≥2851 Pa (with safety factor)
- **Exhaust System** detailed breakdown:
  - Main duct friction losses
  - Branch duct friction losses
  - Fan inlet losses
  - Local losses (tees, grilles)
  - Total: ~1404 Pa
  - Required fan pressure: ≥1404 Pa (with safety factor)

## Example Output

The script calculates and displays:
- **Room area:** 152 m² (12.0m × 12.67m)
- **Calculated supply diffusers:** 14 units
- **Calculated exhaust grilles:** 14 units
- **Total airflow:** ~2654 m³/h
- **Airflow per diffuser:** ~190 m³/h
- **Supply pressure loss:** ~2851 Pa
- **Exhaust pressure loss:** ~1404 Pa

## Engineering Notes

The pressure loss calculations follow standard HVAC engineering practices:
- Reynolds number calculations for flow regime determination
- Colebrook-White equation for friction factor (turbulent flow)
- Standard loss coefficients for fittings and equipment
- Air properties at 20°C (density: 1.2 kg/m³)
- Separate calculations for supply and exhaust systems
- Duct transition losses accounted for

## Note on DWG Format

The script generates high-quality PNG output (300 DPI). For DWG (AutoCAD) format output, specialized CAD software would be required as DWG is a proprietary binary format. The PNG output can be imported into CAD software for further editing if needed.
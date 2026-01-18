# Ventilation Project

This repository contains designs and resources for a supply ventilation system in a 119 sq.m. non-residential room with a ceiling height of 2.91 m. The project includes automatic calculation of the optimal number of diffusers and pressure losses along the route.

## Project Specifications

- **Room Area:** 119 m²
- **Ceiling Height:** 2.91 m
- **Air Exchange Rate:** 6 air changes per hour (typical for office/commercial spaces)
- **Supply Fan:** Ø315 mm channel fan
- **Processing Equipment:**
  - Silencer (noise reduction)
  - Air filter
  - Heater (caloripher)
- **Main Supply Duct:** Ø160 mm
- **Branch Ducts:** Ø125 mm
- **Diffusers:** ДПУ-М 125 (automatically calculated quantity)

## Features

### Automatic Calculations

The system automatically calculates:

1. **Optimal Number of Diffusers**
   - Based on room volume and air exchange requirements
   - Considers recommended airflow per diffuser (150-250 m³/h for ДПУ-М 125)
   - Ensures comfortable air distribution

2. **Pressure Loss Calculations**
   - Friction losses in main and branch ducts (Darcy-Weisbach equation)
   - Local losses in fittings and equipment:
     - Supply fan outlet
     - Silencer
     - Air filter
     - Heater (caloripher)
     - Branch tees
     - Diffusers
   - Total pressure loss with 15% safety factor
   - Required fan pressure specification

3. **Air Velocities**
   - Main duct velocity
   - Branch duct velocity
   - Fan outlet velocity

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

This will create `ventilation_scheme.png` with a complete schematic diagram of the supply ventilation system.

## Output

The generated scheme includes:

### Visual Components
- Room outline with precise dimensions (11.9m × 10.0m)
- Supply fan (Ø315 mm) positioned outside the room
- Processing equipment (silencer, filter, heater) in sequence
- Supply duct (Ø160 mm) entering the room
- Symmetrically placed main duct running through the center
- Evenly distributed diffusers connected via branch ducts (Ø125 mm)
- Color-coded components with comprehensive legend

### Technical Specifications Panel
- Room parameters (area, height, volume)
- Air exchange rate and total airflow
- Complete equipment list
- Number of diffusers and airflow per diffuser
- Air velocities in all duct sections

### Pressure Loss Analysis Panel
- Detailed breakdown of pressure losses:
  - Main duct friction losses
  - Branch duct friction losses
  - Equipment losses (fan outlet, silencer, filter, heater)
  - Local losses (tees, diffusers)
- Total pressure loss
- Required fan pressure (with safety factor)

## Example Output

The script calculates and displays:
- **Calculated diffusers:** 11 units
- **Total airflow:** ~2078 m³/h
- **Airflow per diffuser:** ~189 m³/h
- **Total pressure loss:** ~3698 Pa
- **Required fan pressure:** ≥4253 Pa (with 15% safety factor)

## Engineering Notes

The pressure loss calculations follow standard HVAC engineering practices:
- Reynolds number calculations for flow regime determination
- Colebrook-White equation for friction factor (turbulent flow)
- Standard loss coefficients for fittings and equipment
- Air properties at 20°C (density: 1.2 kg/m³)
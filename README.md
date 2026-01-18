# Ventilation Project

This repository contains designs and resources for a ventilation system in a 119 sq.m. room with a ceiling height of 2.9 m. The project involves symmetry, air diffusers, and planning for airduct diameters.

## Project Specifications

- **Room Area:** 119 m²
- **Ceiling Height:** 2.9 m
- **Air Exchange:** 2070.6 m³/h
- **Number of Diffusers:** 11 (ДПУ-М 125)
- **Main Duct Diameter:** 250 mm
- **Branch Duct Diameter:** 125 mm

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

This will create `ventilation_scheme.png` with a complete schematic diagram of the ventilation system, including:
- Room layout with dimensions
- Main duct placement (Ø250 mm)
- Branch ducts (Ø125 mm)
- 11 symmetrically distributed diffusers
- Technical specifications
- Legend and labels

## Output

The generated scheme includes:
- Room outline with precise dimensions
- Symmetrically placed main duct running through the center
- Evenly distributed diffusers connected via branch ducts
- Complete technical specifications panel
- Color-coded components with legend
- All dimensions and component labels
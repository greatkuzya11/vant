#!/usr/bin/env python3
"""
Ventilation System Scheme Generator with Pressure Loss Calculations

Creates a schematic visualization of supply and exhaust ventilation systems with:
- Room: 152 m² (12m × 12.67m), height 2.91 m
- Supply system (RED):
  * Supply fan: Ø315mm
  * Processing equipment: silencer (Ø250mm), filter, heater
  * Main supply duct: Ø250mm → Ø160mm (with transition)
  * Branch ducts: Ø125mm
- Exhaust system (BLUE):
  * Exhaust fan: Ø250mm
  * Main exhaust duct: Ø160mm
  * Branch ducts: Ø125mm
- Calculates optimal number of diffusers/grilles and pressure losses for both systems
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch, Polygon
import math

def calculate_diffusers_and_pressure_loss():
    """Calculate optimal number of diffusers and pressure losses for supply system."""
    
    # Room parameters
    room_area = 152  # m²
    ceiling_height = 2.91  # m
    room_volume = room_area * ceiling_height  # m³
    
    # Air exchange requirements for non-residential space
    # Using typical 6 air changes per hour for office/commercial space
    air_changes_per_hour = 6
    total_airflow = room_volume * air_changes_per_hour  # m³/h
    total_airflow_m3s = total_airflow / 3600  # m³/s
    
    # Diffuser specifications (ДПУ-М 125)
    diffuser_diameter = 125  # mm
    diffuser_diameter_m = diffuser_diameter / 1000  # m
    
    # Recommended airflow per diffuser: 150-250 m³/h for ДПУ-М 125
    # Using 200 m³/h as optimal for comfort
    airflow_per_diffuser = 200  # m³/h
    
    # Calculate number of diffusers
    num_diffusers = math.ceil(total_airflow / airflow_per_diffuser)
    actual_airflow_per_diffuser = total_airflow / num_diffusers
    
    # Air properties (at 20°C)
    air_density = 1.2  # kg/m³
    air_viscosity = 1.81e-5  # Pa·s
    
    # Duct dimensions
    main_duct_diameter_1 = 250  # mm (initial section)
    main_duct_diameter_2 = 160  # mm (after branching)
    branch_duct_diameter = 125  # mm
    supply_fan_diameter = 315  # mm
    silencer_diameter = 250  # mm
    
    # Convert to meters
    D_main_1 = main_duct_diameter_1 / 1000
    D_main_2 = main_duct_diameter_2 / 1000
    D_branch = branch_duct_diameter / 1000
    D_fan = supply_fan_diameter / 1000
    
    # Estimated duct lengths
    main_duct_length_1 = 3  # m (250mm section before branching)
    main_duct_length_2 = 10  # m (160mm section)
    branch_duct_length = 2  # m (average branch length)
    inlet_duct_length = 2  # m (from fan to room)
    
    # Calculate velocities
    v_main_1 = total_airflow_m3s / (math.pi * (D_main_1/2)**2)  # m/s in 250mm section
    v_main_2 = total_airflow_m3s / (math.pi * (D_main_2/2)**2)  # m/s in 160mm section
    v_branch = (actual_airflow_per_diffuser/3600) / (math.pi * (D_branch/2)**2)  # m/s
    v_fan = total_airflow_m3s / (math.pi * (D_fan/2)**2)  # m/s
    
    # Pressure loss calculations
    # 1. Friction losses in ducts (Darcy-Weisbach)
    roughness = 0.0001  # m (for smooth metal ducts)
    
    # Reynolds number and friction factor for main duct section 1 (250mm)
    Re_main_1 = (air_density * v_main_1 * D_main_1) / air_viscosity
    if Re_main_1 < 2300:
        f_main_1 = 64 / Re_main_1
    else:
        # Using Colebrook-White approximation (Swamee-Jain)
        f_main_1 = 0.25 / (math.log10(roughness/(3.7*D_main_1) + 5.74/Re_main_1**0.9))**2
    
    # Friction loss in main duct section 1
    delta_P_main_1 = f_main_1 * (main_duct_length_1 / D_main_1) * (air_density * v_main_1**2 / 2)
    
    # Reynolds number and friction factor for main duct section 2 (160mm)
    Re_main_2 = (air_density * v_main_2 * D_main_2) / air_viscosity
    if Re_main_2 < 2300:
        f_main_2 = 64 / Re_main_2
    else:
        f_main_2 = 0.25 / (math.log10(roughness/(3.7*D_main_2) + 5.74/Re_main_2**0.9))**2
    
    # Friction loss in main duct section 2
    delta_P_main_2 = f_main_2 * (main_duct_length_2 / D_main_2) * (air_density * v_main_2**2 / 2)
    
    # Total friction loss in main duct
    delta_P_main = delta_P_main_1 + delta_P_main_2
    
    # Reynolds number and friction factor for branch ducts
    Re_branch = (air_density * v_branch * D_branch) / air_viscosity
    if Re_branch < 2300:
        f_branch = 64 / Re_branch
    else:
        f_branch = 0.25 / (math.log10(roughness/(3.7*D_branch) + 5.74/Re_branch**0.9))**2
    
    # Friction loss in branch ducts (total for all branches)
    delta_P_branch = f_branch * (branch_duct_length / D_branch) * (air_density * v_branch**2 / 2)
    
    # 2. Local losses (fittings, transitions, etc.)
    # Supply fan outlet: ζ = 1.0
    delta_P_fan_outlet = 1.0 * (air_density * v_fan**2 / 2)
    
    # Silencer (250mm): typical loss coefficient ζ = 1.5-3.0
    delta_P_silencer = 2.5 * (air_density * v_main_1**2 / 2)
    
    # Filter: typical loss 50-150 Pa for clean filter
    delta_P_filter = 100  # Pa
    
    # Heater (caloripher): typical loss coefficient ζ = 2.0-4.0
    delta_P_heater = 3.0 * (air_density * v_main_1**2 / 2)
    
    # Transition from 250mm to 160mm: ζ = 0.2
    delta_P_transition = 0.2 * (air_density * v_main_2**2 / 2)
    
    # Branch tees: ζ = 1.5 per branch
    delta_P_branches = 1.5 * (air_density * v_branch**2 / 2) * num_diffusers
    
    # Diffusers: typical loss 10-20 Pa per diffuser
    delta_P_diffusers = 15 * num_diffusers  # Pa total for all diffusers
    
    # Total pressure loss
    total_pressure_loss = (delta_P_main + delta_P_branch + delta_P_fan_outlet + 
                          delta_P_silencer + delta_P_filter + delta_P_heater + 
                          delta_P_transition + delta_P_branches + delta_P_diffusers)
    
    # Add safety factor of 10-15%
    total_pressure_loss_with_safety = total_pressure_loss * 1.15
    
    return {
        'num_diffusers': num_diffusers,
        'total_airflow': total_airflow,
        'airflow_per_diffuser': actual_airflow_per_diffuser,
        'air_changes': air_changes_per_hour,
        'v_main_1': v_main_1,
        'v_main_2': v_main_2,
        'v_branch': v_branch,
        'v_fan': v_fan,
        'pressure_losses': {
            'main_duct': delta_P_main,
            'branch_ducts': delta_P_branch,
            'fan_outlet': delta_P_fan_outlet,
            'silencer': delta_P_silencer,
            'filter': delta_P_filter,
            'heater': delta_P_heater,
            'transition': delta_P_transition,
            'branches': delta_P_branches,
            'diffusers': delta_P_diffusers,
            'total': total_pressure_loss,
            'total_with_safety': total_pressure_loss_with_safety
        },
        'room_volume': room_volume
    }

def calculate_exhaust_pressure_loss(num_grilles, total_airflow):
    """Calculate pressure losses for exhaust system."""
    
    total_airflow_m3s = total_airflow / 3600  # m³/s
    
    # Air properties (at 20°C)
    air_density = 1.2  # kg/m³
    air_viscosity = 1.81e-5  # Pa·s
    
    # Duct dimensions
    main_duct_diameter = 160  # mm
    branch_duct_diameter = 125  # mm
    exhaust_fan_diameter = 250  # mm
    
    # Convert to meters
    D_main = main_duct_diameter / 1000
    D_branch = branch_duct_diameter / 1000
    D_fan = exhaust_fan_diameter / 1000
    
    # Estimated duct lengths
    main_duct_length = 8  # m
    branch_duct_length = 2  # m
    
    # Calculate velocities
    airflow_per_grille = total_airflow / num_grilles
    v_main = total_airflow_m3s / (math.pi * (D_main/2)**2)
    v_branch = (airflow_per_grille/3600) / (math.pi * (D_branch/2)**2)
    v_fan = total_airflow_m3s / (math.pi * (D_fan/2)**2)
    
    # Friction losses
    roughness = 0.0001  # m
    
    # Main duct
    Re_main = (air_density * v_main * D_main) / air_viscosity
    if Re_main < 2300:
        f_main = 64 / Re_main
    else:
        f_main = 0.25 / (math.log10(roughness/(3.7*D_main) + 5.74/Re_main**0.9))**2
    delta_P_main = f_main * (main_duct_length / D_main) * (air_density * v_main**2 / 2)
    
    # Branch ducts
    Re_branch = (air_density * v_branch * D_branch) / air_viscosity
    if Re_branch < 2300:
        f_branch = 64 / Re_branch
    else:
        f_branch = 0.25 / (math.log10(roughness/(3.7*D_branch) + 5.74/Re_branch**0.9))**2
    delta_P_branch = f_branch * (branch_duct_length / D_branch) * (air_density * v_branch**2 / 2)
    
    # Local losses
    delta_P_fan_inlet = 1.0 * (air_density * v_fan**2 / 2)
    delta_P_branches = 1.2 * (air_density * v_branch**2 / 2) * num_grilles
    delta_P_grilles = 10 * num_grilles  # Pa
    
    total_pressure_loss = (delta_P_main + delta_P_branch + delta_P_fan_inlet + 
                          delta_P_branches + delta_P_grilles)
    total_pressure_loss_with_safety = total_pressure_loss * 1.15
    
    return {
        'v_main': v_main,
        'v_branch': v_branch,
        'v_fan': v_fan,
        'total': total_pressure_loss,
        'total_with_safety': total_pressure_loss_with_safety
    }

def create_ventilation_scheme():
    """Generate the ventilation system schematic diagram with supply and exhaust."""
    
    # Calculate system parameters
    calc = calculate_diffusers_and_pressure_loss()
    exhaust_calc = calculate_exhaust_pressure_loss(calc['num_diffusers'], calc['total_airflow'])
    
    # Room parameters
    room_area = 152  # m²
    ceiling_height = 2.91  # m
    
    # Room dimensions (rectangular) - adjusted for 152 m²
    # Using approximately 12m x 12.67m
    room_width = 12.0  # m
    room_length = 12.67  # m
    
    # Ventilation components
    num_diffusers = calc['num_diffusers']
    main_duct_diameter_1 = 250  # mm (initial section)
    main_duct_diameter_2 = 160  # mm (after branching)
    branch_duct_diameter = 125  # mm
    supply_fan_diameter = 315  # mm
    silencer_diameter = 250  # mm
    exhaust_fan_diameter = 250  # mm (typical for exhaust)
    
    # Create figure with appropriate size
    fig, ax = plt.subplots(figsize=(20, 14))
    
    # Draw room outline
    room_rect = Rectangle((2, 0), room_length, room_width, 
                          fill=False, edgecolor='black', linewidth=2.5)
    ax.add_patch(room_rect)
    
    # Add room dimensions
    ax.annotate('', xy=(2 + room_length, -0.5), xytext=(2, -0.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(2 + room_length/2, -0.8, f'{room_length} м', ha='center', fontsize=12, weight='bold')
    
    ax.annotate('', xy=(1.5, room_width), xytext=(1.5, 0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(1.0, room_width/2, f'{room_width} м', ha='center', fontsize=12, 
            rotation=90, va='center', weight='bold')
    
    # Draw supply system components (outside room on left side)
    component_x = -2.5
    component_y = room_width / 2
    
    # Supply fan (315mm)
    fan = Circle((component_x, component_y), 0.4, 
                 fill=True, facecolor='lightcoral', edgecolor='darkred', linewidth=2)
    ax.add_patch(fan)
    ax.text(component_x, component_y, 'В', ha='center', va='center', 
            fontsize=14, weight='bold', color='darkred')
    ax.text(component_x, component_y - 0.7, 'Вентилятор\nØ315 мм', 
            ha='center', fontsize=9, weight='bold')
    
    # Components along the inlet duct
    comp_spacing = 1.2
    
    # Silencer
    silencer_x = component_x + comp_spacing
    silencer = Rectangle((silencer_x - 0.15, component_y - 0.3), 0.3, 0.6,
                         fill=True, facecolor='lightgray', edgecolor='black', linewidth=1.5)
    ax.add_patch(silencer)
    ax.text(silencer_x, component_y + 0.6, 'Глушитель', ha='center', fontsize=8, weight='bold')
    
    # Filter
    filter_x = silencer_x + comp_spacing * 0.8
    filter_rect = Rectangle((filter_x - 0.15, component_y - 0.3), 0.3, 0.6,
                            fill=True, facecolor='lightyellow', edgecolor='orange', linewidth=1.5)
    ax.add_patch(filter_rect)
    # Add filter pattern
    for i in range(5):
        ax.plot([filter_x - 0.1, filter_x + 0.1], 
                [component_y - 0.2 + i*0.1, component_y - 0.2 + i*0.1], 
                'orange', linewidth=1)
    ax.text(filter_x, component_y + 0.6, 'Фильтр', ha='center', fontsize=8, weight='bold')
    
    # Heater (Caloripher)
    heater_x = filter_x + comp_spacing * 0.8
    heater = Rectangle((heater_x - 0.15, component_y - 0.3), 0.3, 0.6,
                       fill=True, facecolor='lightpink', edgecolor='red', linewidth=1.5)
    ax.add_patch(heater)
    ax.text(heater_x, component_y + 0.6, 'Калорифер', ha='center', fontsize=8, weight='bold')
    
    # Draw connecting ducts to room entrance (RED for supply)
    # From fan to silencer
    ax.plot([component_x + 0.4, silencer_x - 0.15], [component_y, component_y], 
            'red', linewidth=4)
    # From silencer to filter
    ax.plot([silencer_x + 0.15, filter_x - 0.15], [component_y, component_y], 
            'red', linewidth=4)
    # From filter to heater
    ax.plot([filter_x + 0.15, heater_x - 0.15], [component_y, component_y], 
            'red', linewidth=4)
    # From heater to room entrance
    ax.plot([heater_x + 0.15, 2], [component_y, component_y], 
            'red', linewidth=4)
    
    # Add arrow showing airflow direction
    arrow = FancyArrowPatch((component_x - 0.6, component_y), (component_x - 0.45, component_y),
                           arrowstyle='->', mutation_scale=20, linewidth=2, color='red')
    ax.add_patch(arrow)
    ax.text(component_x - 0.8, component_y + 0.3, 'Приток', fontsize=9, weight='bold', color='red')
    
    # SUPPLY SYSTEM - Main duct position (upper part of room)
    supply_duct_y = room_width * 0.65  # Upper section for supply
    supply_duct_start_x = 2.5
    supply_duct_end_x = 2 + room_length - 0.5
    
    # Draw initial 250mm section (from entrance to first branch)
    initial_section_length = 2.0
    main_duct_width_250 = 0.25  # representing 250mm in scale
    main_duct_250 = Rectangle((supply_duct_start_x, supply_duct_y - main_duct_width_250/2),
                              initial_section_length, main_duct_width_250,
                              fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2)
    ax.add_patch(main_duct_250)
    
    # Draw main duct 160mm section (after transition)
    main_duct_width_160 = 0.16  # representing 160mm in scale
    transition_x = supply_duct_start_x + initial_section_length
    main_duct_160 = Rectangle((transition_x, supply_duct_y - main_duct_width_160/2),
                              supply_duct_end_x - transition_x, main_duct_width_160,
                              fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2)
    ax.add_patch(main_duct_160)
    
    # Draw transition from 250mm to 160mm
    transition_points = [
        [transition_x, supply_duct_y - main_duct_width_250/2],
        [transition_x + 0.3, supply_duct_y - main_duct_width_160/2],
        [transition_x + 0.3, supply_duct_y + main_duct_width_160/2],
        [transition_x, supply_duct_y + main_duct_width_250/2]
    ]
    transition = Polygon(transition_points, fill=True, facecolor='coral', edgecolor='red', linewidth=2)
    ax.add_patch(transition)
    
    # Connection from room entrance to supply duct
    ax.plot([2, supply_duct_start_x], [component_y, supply_duct_y], 
            'red', linewidth=4, linestyle='--')
    
    # Add supply duct labels
    ax.text(supply_duct_start_x + 1.0, supply_duct_y + 0.35, 'Ø250 мм',
            ha='center', fontsize=10, weight='bold', color='red')
    ax.text(2 + room_length/2, supply_duct_y + 0.35, 'Приточный воздуховод Ø160 мм',
            ha='center', fontsize=11, weight='bold', color='red')
    
    # Calculate diffuser positions (evenly distributed) - start after transition
    diffuser_start_x = transition_x + 0.5
    diffuser_span = supply_duct_end_x - diffuser_start_x
    spacing = diffuser_span / (num_diffusers - 1) if num_diffusers > 1 else 0
    diffuser_positions = []
    
    for i in range(num_diffusers):
        x_pos = diffuser_start_x + i * spacing if num_diffusers > 1 else 2 + room_length/2
        diffuser_positions.append((x_pos, supply_duct_y))
    
    # Draw SUPPLY branch ducts and diffusers
    branch_width = 0.125  # representing 125mm in scale
    branch_length = 1.5  # length of branch duct
    
    for idx, (x, y) in enumerate(diffuser_positions):
        # All branches go upward for supply
        direction = 1
        
        # Draw branch duct (red for supply)
        branch = Rectangle((x - branch_width/2, y + main_duct_width_160/2),
                          branch_width, branch_length,
                          fill=True, facecolor='mistyrose', edgecolor='red', linewidth=1.5)
        ax.add_patch(branch)
        
        # Draw diffuser (ДПУ-М 125)
        diffuser_y = y + main_duct_width_160/2 + branch_length
        diffuser = Circle((x, diffuser_y), 0.15, 
                         fill=True, facecolor='yellow', edgecolor='orange', linewidth=2)
        ax.add_patch(diffuser)
        
        # Add diffuser label
        label_offset = 0.3
        ax.text(x, diffuser_y + label_offset, f'ДПУ-М 125\n№{idx+1}',
                ha='center', va='center',
                fontsize=8, weight='bold')
        
        # Add branch duct diameter label (only for first few to avoid clutter)
        if idx < 3 or idx == num_diffusers - 1:
            branch_label_y = y + main_duct_width_160/2 + branch_length/2
            ax.text(x + 0.35, branch_label_y, 'Ø125', fontsize=7, color='red', rotation=90, va='center')
    
    # EXHAUST SYSTEM - Lower part of room
    exhaust_duct_y = room_width * 0.35  # Lower section for exhaust
    exhaust_duct_start_x = 2.5
    exhaust_duct_end_x = 2 + room_length - 0.5
    
    # Draw exhaust main duct (160mm)
    exhaust_duct_width = 0.16
    exhaust_main = Rectangle((exhaust_duct_start_x, exhaust_duct_y - exhaust_duct_width/2),
                             exhaust_duct_end_x - exhaust_duct_start_x, exhaust_duct_width,
                             fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(exhaust_main)
    
    # Add exhaust duct label
    ax.text(2 + room_length/2, exhaust_duct_y - 0.35, 'Вытяжной воздуховод Ø160 мм',
            ha='center', fontsize=11, weight='bold', color='blue')
    
    # Calculate exhaust grille positions (same number as supply diffusers)
    num_grilles = num_diffusers
    exhaust_span = exhaust_duct_end_x - exhaust_duct_start_x
    exhaust_spacing = exhaust_span / (num_grilles - 1) if num_grilles > 1 else 0
    grille_positions = []
    for i in range(num_grilles):
        x_pos = exhaust_duct_start_x + i * exhaust_spacing if num_grilles > 1 else 2 + room_length/2
        grille_positions.append((x_pos, exhaust_duct_y))
    
    # Draw EXHAUST branch ducts and grilles
    for idx, (x, y) in enumerate(grille_positions):
        # All branches go downward for exhaust
        direction = -1
        
        # Draw branch duct (blue for exhaust)
        branch = Rectangle((x - branch_width/2, y - exhaust_duct_width/2 - branch_length),
                          branch_width, branch_length,
                          fill=True, facecolor='lightcyan', edgecolor='blue', linewidth=1.5)
        ax.add_patch(branch)
        
        # Draw exhaust grille
        grille_y = y - exhaust_duct_width/2 - branch_length
        grille = Circle((x, grille_y), 0.15, 
                       fill=True, facecolor='lightyellow', edgecolor='darkorange', linewidth=2)
        ax.add_patch(grille)
        
        # Add grille label
        label_offset = -0.3
        ax.text(x, grille_y + label_offset, f'Решетка\n№{idx+1}',
                ha='center', va='center',
                fontsize=8, weight='bold')
        
        # Add branch duct diameter label (only for first few to avoid clutter)
        if idx < 3 or idx == num_grilles - 1:
            branch_label_y = y - exhaust_duct_width/2 - branch_length/2
            ax.text(x - 0.35, branch_label_y, 'Ø125', fontsize=7, color='blue', rotation=90, va='center')
    
    # Draw exhaust fan on right side outside room
    exhaust_fan_x = 2 + room_length + 1.5
    exhaust_fan_y = exhaust_duct_y
    
    # Connect exhaust duct to fan
    ax.plot([exhaust_duct_end_x, exhaust_fan_x - 0.35], [exhaust_duct_y, exhaust_fan_y], 
            'blue', linewidth=4, linestyle='--')
    
    # Exhaust fan (250mm)
    exhaust_fan = Circle((exhaust_fan_x, exhaust_fan_y), 0.35, 
                        fill=True, facecolor='lightblue', edgecolor='darkblue', linewidth=2)
    ax.add_patch(exhaust_fan)
    ax.text(exhaust_fan_x, exhaust_fan_y, 'В', ha='center', va='center', 
            fontsize=14, weight='bold', color='darkblue')
    ax.text(exhaust_fan_x, exhaust_fan_y - 0.6, 'Вытяжной\nвентилятор\nØ250 мм', 
            ha='center', fontsize=9, weight='bold')
    
    # Add arrow showing exhaust airflow direction
    exhaust_arrow = FancyArrowPatch((exhaust_fan_x + 0.35, exhaust_fan_y), 
                                   (exhaust_fan_x + 0.55, exhaust_fan_y),
                                   arrowstyle='->', mutation_scale=20, linewidth=2, color='blue')
    ax.add_patch(exhaust_arrow)
    ax.text(exhaust_fan_x + 0.75, exhaust_fan_y + 0.3, 'Вытяжка', fontsize=9, weight='bold', color='blue')
    
    # Add technical specifications box
    specs_text = (
        f"ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ:\n"
        f"──────────────────────────────────\n"
        f"Площадь помещения: {room_area} м²\n"
        f"Высота потолка: {ceiling_height} м\n"
        f"Объем помещения: {calc['room_volume']:.1f} м³\n"
        f"Воздухообмен: {calc['total_airflow']:.1f} м³/ч\n"
        f"Кратность: {calc['air_changes']:.1f} раз/ч\n\n"
        f"ПРИТОЧНАЯ СИСТЕМА:\n"
        f"──────────────────────────────────\n"
        f"Канальный вентилятор: Ø{supply_fan_diameter} мм\n"
        f"Глушитель шума: Ø{silencer_diameter} мм\n"
        f"Фильтр воздуха\n"
        f"Калорифер\n"
        f"Приточный воздуховод: Ø{main_duct_diameter_1}→Ø{main_duct_diameter_2} мм\n"
        f"Ответвления: Ø{branch_duct_diameter} мм\n"
        f"Диффузоры: {num_diffusers} шт. (ДПУ-М 125)\n"
        f"Расход на диффузор: {calc['airflow_per_diffuser']:.1f} м³/ч\n\n"
        f"ВЫТЯЖНАЯ СИСТЕМА:\n"
        f"──────────────────────────────────\n"
        f"Канальный вентилятор: Ø{exhaust_fan_diameter} мм\n"
        f"Вытяжной воздуховод: Ø160 мм\n"
        f"Ответвления: Ø{branch_duct_diameter} мм\n"
        f"Решетки: {num_grilles} шт.\n\n"
        f"СКОРОСТИ ВОЗДУХА (ПРИТОК):\n"
        f"──────────────────────────────────\n"
        f"В магистрали Ø250: {calc['v_main_1']:.2f} м/с\n"
        f"В магистрали Ø160: {calc['v_main_2']:.2f} м/с\n"
        f"В ответвлениях: {calc['v_branch']:.2f} м/с\n"
        f"На выходе вентилятора: {calc['v_fan']:.2f} м/с"
    )
    
    # Pressure loss box
    pl = calc['pressure_losses']
    pl_exhaust = exhaust_calc
    pressure_text = (
        f"ПОТЕРИ ДАВЛЕНИЯ (ПРИТОК):\n"
        f"──────────────────────────────────\n"
        f"Магистраль (Ø250+Ø160): {pl['main_duct']:.1f} Па\n"
        f"Ответвления: {pl['branch_ducts']:.1f} Па\n"
        f"Выход вентилятора: {pl['fan_outlet']:.1f} Па\n"
        f"Глушитель: {pl['silencer']:.1f} Па\n"
        f"Фильтр: {pl['filter']:.1f} Па\n"
        f"Калорифер: {pl['heater']:.1f} Па\n"
        f"Переход Ø250→Ø160: {pl['transition']:.1f} Па\n"
        f"Тройники: {pl['branches']:.1f} Па\n"
        f"Диффузоры: {pl['diffusers']:.1f} Па\n"
        f"──────────────────────────────────\n"
        f"ИТОГО: {pl['total']:.1f} Па\n"
        f"С запасом (15%): {pl['total_with_safety']:.1f} Па\n\n"
        f"ПОТЕРИ ДАВЛЕНИЯ (ВЫТЯЖКА):\n"
        f"──────────────────────────────────\n"
        f"ИТОГО: {pl_exhaust['total']:.1f} Па\n"
        f"С запасом (15%): {pl_exhaust['total_with_safety']:.1f} Па"
    )
    
    # Add specs box with background
    specs_box = FancyBboxPatch((2 + room_length + 0.8, room_width - 7.2), 5.2, 7.0,
                               boxstyle="round,pad=0.1", 
                               facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(specs_box)
    ax.text(2 + room_length + 1.0, room_width - 0.4, specs_text,
            fontsize=8, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='none', edgecolor='none'))
    
    # Add pressure loss box
    pressure_box = FancyBboxPatch((2 + room_length + 0.8, -1.2), 5.2, 5.8,
                                 boxstyle="round,pad=0.1", 
                                 facecolor='lightcyan', edgecolor='black', linewidth=2)
    ax.add_patch(pressure_box)
    ax.text(2 + room_length + 1.0, 4.4, pressure_text,
            fontsize=8, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='none', edgecolor='none'))
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='lightcoral', edgecolor='darkred', label='Приточный вентилятор Ø315мм'),
        mpatches.Patch(facecolor='lightblue', edgecolor='darkblue', label='Вытяжной вентилятор Ø250мм'),
        mpatches.Patch(facecolor='lightgray', edgecolor='black', label='Глушитель Ø250мм'),
        mpatches.Patch(facecolor='lightyellow', edgecolor='orange', label='Фильтр'),
        mpatches.Patch(facecolor='lightpink', edgecolor='red', label='Калорифер'),
        mpatches.Patch(facecolor='lightcoral', edgecolor='red', label='Приточный воздуховод (красный)'),
        mpatches.Patch(facecolor='lightblue', edgecolor='blue', label='Вытяжной воздуховод (синий)'),
        mpatches.Patch(facecolor='yellow', edgecolor='orange', label='Диффузор/Решетка')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, -0.05),
             ncol=4, fontsize=9, frameon=True)
    
    # Set title
    plt.title('СХЕМА ПРИТОЧНО-ВЫТЯЖНОЙ ВЕНТИЛЯЦИИ НЕЖИЛОГО ПОМЕЩЕНИЯ\n(с расчетом количества диффузоров и потерь давления)',
             fontsize=15, weight='bold', pad=20)
    
    # Set axis properties
    ax.set_xlim(-3.5, 2 + room_length + 6.5)
    ax.set_ylim(-2, room_width + 1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Длина, м', fontsize=12, weight='bold')
    ax.set_ylabel('Ширина, м', fontsize=12, weight='bold')
    
    # Save the figure
    output_file = 'ventilation_scheme.png'
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Схема вентиляции сохранена в файл: {output_file}")
    print(f"\nРасчетные параметры:")
    print(f"  Площадь помещения: {room_area} м²")
    print(f"  Размеры помещения: {room_width} м × {room_length} м")
    print(f"  Приточных диффузоров: {num_diffusers} шт.")
    print(f"  Вытяжных решеток: {num_grilles} шт.")
    print(f"  Общий воздухообмен: {calc['total_airflow']:.1f} м³/ч")
    print(f"  Расход на диффузор: {calc['airflow_per_diffuser']:.1f} м³/ч")
    print(f"  Потери давления (приток): {pl['total_with_safety']:.1f} Па")
    print(f"  Потери давления (вытяжка): {pl_exhaust['total_with_safety']:.1f} Па")
    
    return output_file

if __name__ == "__main__":
    create_ventilation_scheme()
    print("\nВизуализация успешно создана!")

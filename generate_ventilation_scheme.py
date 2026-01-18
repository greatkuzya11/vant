#!/usr/bin/env python3
"""
Ventilation System Scheme Generator

Creates a schematic visualization of a ventilation system with:
- Room: 119 m², height 2.9 m
- Air exchange: 2070.6 m³/h
- 11 diffusers (ДПУ-М 125)
- Main duct: 250mm diameter
- Branch ducts: 125mm diameter
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import numpy as np

def create_ventilation_scheme():
    """Generate the ventilation system schematic diagram."""
    
    # Room parameters
    room_area = 119  # m²
    ceiling_height = 2.9  # m
    air_exchange = 2070.6  # m³/h
    
    # Assuming a rectangular room with reasonable proportions
    # For 119 m², let's use approximately 10m x 11.9m
    room_width = 10.0  # m
    room_length = 11.9  # m
    
    # Ventilation components
    num_diffusers = 11
    main_duct_diameter = 250  # mm
    branch_duct_diameter = 125  # mm
    
    # Create figure with appropriate size
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Draw room outline
    room_rect = Rectangle((0, 0), room_length, room_width, 
                          fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(room_rect)
    
    # Add room dimensions
    ax.annotate('', xy=(room_length, -0.5), xytext=(0, -0.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(room_length/2, -0.8, f'{room_length} м', ha='center', fontsize=12, weight='bold')
    
    ax.annotate('', xy=(-0.5, room_width), xytext=(-0.5, 0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(-1.2, room_width/2, f'{room_width} м', ha='center', fontsize=12, 
            rotation=90, va='center', weight='bold')
    
    # Main duct position (centered horizontally, running along the length)
    main_duct_y = room_width / 2
    main_duct_start_x = 0.5
    main_duct_end_x = room_length - 0.5
    
    # Draw main duct (250mm)
    main_duct_width = 0.25  # representing 250mm in scale
    main_duct = Rectangle((main_duct_start_x, main_duct_y - main_duct_width/2),
                          main_duct_end_x - main_duct_start_x, main_duct_width,
                          fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(main_duct)
    
    # Add main duct label
    ax.text(room_length/2, main_duct_y + 0.4, 'Магистральный воздуховод Ø250 мм',
            ha='center', fontsize=11, weight='bold', color='blue')
    
    # Calculate diffuser positions (evenly distributed)
    # Place diffusers symmetrically along the main duct
    spacing = (main_duct_end_x - main_duct_start_x) / (num_diffusers - 1)
    diffuser_positions = []
    
    for i in range(num_diffusers):
        x_pos = main_duct_start_x + i * spacing
        diffuser_positions.append((x_pos, main_duct_y))
    
    # Draw branch ducts and diffusers
    branch_width = 0.125  # representing 125mm in scale
    branch_length = 1.5  # length of branch duct
    
    for idx, (x, y) in enumerate(diffuser_positions):
        # Alternate branches above and below for clarity
        direction = 1 if idx % 2 == 0 else -1
        
        # Draw branch duct
        if direction == 1:
            branch = Rectangle((x - branch_width/2, y + main_duct_width/2),
                              branch_width, branch_length,
                              fill=True, facecolor='lightgreen', edgecolor='green', linewidth=1.5)
        else:
            branch = Rectangle((x - branch_width/2, y - main_duct_width/2 - branch_length),
                              branch_width, branch_length,
                              fill=True, facecolor='lightgreen', edgecolor='green', linewidth=1.5)
        ax.add_patch(branch)
        
        # Draw diffuser (ДПУ-М 125)
        diffuser_y = y + main_duct_width/2 + branch_length if direction == 1 else y - main_duct_width/2 - branch_length
        diffuser = Circle((x, diffuser_y), 0.15, 
                         fill=True, facecolor='yellow', edgecolor='orange', linewidth=2)
        ax.add_patch(diffuser)
        
        # Add diffuser label
        label_offset = 0.3 if direction == 1 else -0.3
        ax.text(x, diffuser_y + label_offset, f'ДПУ-М 125\n№{idx+1}',
                ha='center', va='center' if direction == 1 else 'center',
                fontsize=8, weight='bold')
        
        # Add branch duct diameter label (only for first few to avoid clutter)
        if idx < 3 or idx == num_diffusers - 1:
            branch_label_y = y + main_duct_width/2 + branch_length/2 if direction == 1 else y - main_duct_width/2 - branch_length/2
            ax.text(x + 0.35, branch_label_y, 'Ø125', fontsize=7, color='green', rotation=90, va='center')
    
    # Add technical specifications box
    specs_text = (
        f"ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ:\n"
        f"─────────────────────────────\n"
        f"Площадь помещения: {room_area} м²\n"
        f"Высота потолка: {ceiling_height} м\n"
        f"Объем помещения: {room_area * ceiling_height:.1f} м³\n"
        f"Воздухообмен: {air_exchange} м³/ч\n"
        f"Кратность воздухообмена: {air_exchange / (room_area * ceiling_height):.1f} раз/ч\n\n"
        f"ОБОРУДОВАНИЕ:\n"
        f"─────────────────────────────\n"
        f"Количество диффузоров: {num_diffusers} шт.\n"
        f"Тип диффузора: ДПУ-М 125\n"
        f"Диаметр магистрали: {main_duct_diameter} мм\n"
        f"Диаметр ответвлений: {branch_duct_diameter} мм\n"
        f"Расход на диффузор: {air_exchange/num_diffusers:.1f} м³/ч"
    )
    
    # Add specs box with background
    specs_box = FancyBboxPatch((room_length + 0.8, room_width - 5.5), 4.5, 5.3,
                               boxstyle="round,pad=0.1", 
                               facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(specs_box)
    ax.text(room_length + 1.0, room_width - 0.4, specs_text,
            fontsize=9, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='none', edgecolor='none'))
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='lightblue', edgecolor='blue', label='Магистральный воздуховод Ø250мм'),
        mpatches.Patch(facecolor='lightgreen', edgecolor='green', label='Ответвление Ø125мм'),
        mpatches.Patch(facecolor='yellow', edgecolor='orange', label='Диффузор ДПУ-М 125')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, -0.05),
             ncol=3, fontsize=10, frameon=True)
    
    # Set title
    plt.title('СХЕМА ВЕНТИЛЯЦИИ НЕЖИЛОГО ПОМЕЩЕНИЯ\n(План расположения воздуховодов и диффузоров)',
             fontsize=16, weight='bold', pad=20)
    
    # Set axis properties
    ax.set_xlim(-2, room_length + 5.5)
    ax.set_ylim(-1.5, room_width + 1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Длина, м', fontsize=12, weight='bold')
    ax.set_ylabel('Ширина, м', fontsize=12, weight='bold')
    
    # Save the figure
    output_file = 'ventilation_scheme.png'
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Схема вентиляции сохранена в файл: {output_file}")
    
    return output_file

if __name__ == "__main__":
    create_ventilation_scheme()
    print("Визуализация успешно создана!")

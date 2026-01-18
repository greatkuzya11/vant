#!/usr/bin/env python3
"""
Генератор схемы системы вентиляции с расчетом потерь давления

Создает схематическую визуализацию приточной и вытяжной систем вентиляции:
- Помещение: 152 м² (12м × 12.67м), высота 2.91 м
- Приточная система (КРАСНЫЙ):
  * Приточный вентилятор: Ø315мм
  * Оборудование обработки: глушитель (Ø250мм), фильтр, нагреватель
  * Главный приточный воздуховод: Ø250мм → Ø160мм (с переходом)
  * Ответвления: Ø125мм
- Вытяжная система (СИНИЙ):
  * Вытяжной вентилятор: Ø250мм
  * Главный вытяжной воздуховод: Ø160мм
  * Ответвления: Ø125мм
- Рассчитывает оптимальное количество диффузоров/решеток и потери давления для обеих систем
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch, Polygon
import math

def calculate_diffusers_and_pressure_loss():
    """Рассчитать оптимальное количество диффузоров и потери давления для приточной системы."""
    
    # Параметры помещения
    room_area = 152  # m²
    ceiling_height = 2.91  # m
    room_volume = room_area * ceiling_height  # m³
    
    # Требования к воздухообмену для нежилых помещений
    # Используется типовое значение 6 кратностей в час для офиса/коммерческого помещения
    air_changes_per_hour = 6
    total_airflow = room_volume * air_changes_per_hour  # m³/h
    total_airflow_m3s = total_airflow / 3600  # m³/s
    
    # Технические характеристики диффузора (ДПУ-М 125)
    diffuser_diameter = 125  # mm
    diffuser_diameter_m = diffuser_diameter / 1000  # m
    
    # Рекомендуемый расход воздуха на диффузор: 150-250 м³/ч для ДПУ-М 125
    # Используется 200 м³/ч как оптимальное значение для комфорта
    airflow_per_diffuser = 200  # m³/h
    
    # Расчет количества диффузоров
    num_diffusers = math.ceil(total_airflow / airflow_per_diffuser)
    actual_airflow_per_diffuser = total_airflow / num_diffusers
    
    # Свойства воздуха (при 20°C)
    air_density = 1.2  # kg/m³
    air_viscosity = 1.81e-5  # Pa·s
    
    # Размеры воздуховодов
    main_duct_diameter_1 = 250  # mm (начальный участок)
    main_duct_diameter_2 = 160  # mm (после разветвления)
    branch_duct_diameter = 125  # mm
    supply_fan_diameter = 315  # mm
    silencer_diameter = 250  # mm
    
    # Преобразование в метры
    D_main_1 = main_duct_diameter_1 / 1000
    D_main_2 = main_duct_diameter_2 / 1000
    D_branch = branch_duct_diameter / 1000
    D_fan = supply_fan_diameter / 1000
    
    # Расчетная длина воздуховодов
    main_duct_length_1 = 3  # m (участок 250мм до разветвления)
    main_duct_length_2 = 10  # m (участок 160мм)
    branch_duct_length = 2  # m (средняя длина ответвления)
    inlet_duct_length = 2  # m (от вентилятора до помещения)
    
    # Расчет скоростей
    v_main_1 = total_airflow_m3s / (math.pi * (D_main_1/2)**2)  # м/с в участке 250мм
    v_main_2 = total_airflow_m3s / (math.pi * (D_main_2/2)**2)  # м/с в участке 160мм
    v_branch = (actual_airflow_per_diffuser/3600) / (math.pi * (D_branch/2)**2)  # м/с
    v_fan = total_airflow_m3s / (math.pi * (D_fan/2)**2)  # м/с
    
    # Расчет потерь давления
    # 1. Потери на трение в воздуховодах (формула Дарси-Вейсбаха)
    roughness = 0.0001  # m (для гладких металлических воздуховодов)
    
    # Число Рейнольдса и коэффициент трения для участка магистрали 1 (250мм)
    Re_main_1 = (air_density * v_main_1 * D_main_1) / air_viscosity
    if Re_main_1 < 2300:
        f_main_1 = 64 / Re_main_1
    else:
        # Используется аппроксимация Колбрука-Уайта (Суоми-Джейн)
        f_main_1 = 0.25 / (math.log10(roughness/(3.7*D_main_1) + 5.74/Re_main_1**0.9))**2
    
    # Потери на трение в участке магистрали 1
    delta_P_main_1 = f_main_1 * (main_duct_length_1 / D_main_1) * (air_density * v_main_1**2 / 2)
    
    # Число Рейнольдса и коэффициент трения для участка магистрали 2 (160мм)
    Re_main_2 = (air_density * v_main_2 * D_main_2) / air_viscosity
    if Re_main_2 < 2300:
        f_main_2 = 64 / Re_main_2
    else:
        f_main_2 = 0.25 / (math.log10(roughness/(3.7*D_main_2) + 5.74/Re_main_2**0.9))**2
    
    # Потери на трение в участке магистрали 2
    delta_P_main_2 = f_main_2 * (main_duct_length_2 / D_main_2) * (air_density * v_main_2**2 / 2)
    
    # Полные потери на трение в магистрали
    delta_P_main = delta_P_main_1 + delta_P_main_2
    
    # Число Рейнольдса и коэффициент трения для ответвлений
    Re_branch = (air_density * v_branch * D_branch) / air_viscosity
    if Re_branch < 2300:
        f_branch = 64 / Re_branch
    else:
        f_branch = 0.25 / (math.log10(roughness/(3.7*D_branch) + 5.74/Re_branch**0.9))**2
    
    # Потери на трение в ответвлениях (суммарно для всех ответвлений)
    delta_P_branch = f_branch * (branch_duct_length / D_branch) * (air_density * v_branch**2 / 2)
    
    # 2. Местные потери (фитинги, переходы и т.д.)
    # Выход приточного вентилятора: ζ = 1.0
    delta_P_fan_outlet = 1.0 * (air_density * v_fan**2 / 2)
    
    # Глушитель (250мм): типовой коэффициент потерь ζ = 1.5-3.0
    delta_P_silencer = 2.5 * (air_density * v_main_1**2 / 2)
    
    # Фильтр: типовые потери 50-150 Па для чистого фильтра
    delta_P_filter = 100  # Pa
    
    # Калорифер: типовой коэффициент потерь ζ = 2.0-4.0
    delta_P_heater = 3.0 * (air_density * v_main_1**2 / 2)
    
    # Переход с 250мм на 160мм: ζ = 0.2
    delta_P_transition = 0.2 * (air_density * v_main_2**2 / 2)
    
    # Тройники для ответвлений: ζ = 1.5 на каждое ответвление
    delta_P_branches = 1.5 * (air_density * v_branch**2 / 2) * num_diffusers
    
    # Диффузоры: типовые потери 10-20 Па на диффузор
    delta_P_diffusers = 15 * num_diffusers  # Па суммарно для всех диффузоров
    
    # Полные потери давления
    total_pressure_loss = (delta_P_main + delta_P_branch + delta_P_fan_outlet + 
                          delta_P_silencer + delta_P_filter + delta_P_heater + 
                          delta_P_transition + delta_P_branches + delta_P_diffusers)
    
    # Добавление коэффициента запаса 10-15%
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
    """Рассчитать потери давления для вытяжной системы."""
    
    total_airflow_m3s = total_airflow / 3600  # m³/s
    
    # Свойства воздуха (при 20°C)
    air_density = 1.2  # kg/m³
    air_viscosity = 1.81e-5  # Pa·s
    
    # Размеры воздуховодов
    main_duct_diameter = 160  # mm
    branch_duct_diameter = 125  # mm
    exhaust_fan_diameter = 250  # mm
    
    # Преобразование в метры
    D_main = main_duct_diameter / 1000
    D_branch = branch_duct_diameter / 1000
    D_fan = exhaust_fan_diameter / 1000
    
    # Расчетная длина воздуховодов
    main_duct_length = 8  # m
    branch_duct_length = 2  # m
    
    # Расчет скоростей
    airflow_per_grille = total_airflow / num_grilles
    v_main = total_airflow_m3s / (math.pi * (D_main/2)**2)
    v_branch = (airflow_per_grille/3600) / (math.pi * (D_branch/2)**2)
    v_fan = total_airflow_m3s / (math.pi * (D_fan/2)**2)
    
    # Потери на трение
    roughness = 0.0001  # m
    
    # Магистральный воздуховод
    Re_main = (air_density * v_main * D_main) / air_viscosity
    if Re_main < 2300:
        f_main = 64 / Re_main
    else:
        f_main = 0.25 / (math.log10(roughness/(3.7*D_main) + 5.74/Re_main**0.9))**2
    delta_P_main = f_main * (main_duct_length / D_main) * (air_density * v_main**2 / 2)
    
    # Ответвления
    Re_branch = (air_density * v_branch * D_branch) / air_viscosity
    if Re_branch < 2300:
        f_branch = 64 / Re_branch
    else:
        f_branch = 0.25 / (math.log10(roughness/(3.7*D_branch) + 5.74/Re_branch**0.9))**2
    delta_P_branch = f_branch * (branch_duct_length / D_branch) * (air_density * v_branch**2 / 2)
    
    # Местные потери
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
    """Создать схему системы вентиляции с приточной и вытяжной системами."""
    
    # Расчет параметров системы
    calc = calculate_diffusers_and_pressure_loss()
    exhaust_calc = calculate_exhaust_pressure_loss(calc['num_diffusers'], calc['total_airflow'])
    
    # Параметры помещения
    room_area = 152  # m²
    ceiling_height = 2.91  # m
    
    # Размеры помещения (прямоугольник) - скорректировано для 152 м²
    # Используется приблизительно 12м × 12.67м
    room_width = 12.0  # m
    room_length = 12.67  # m
    
    # Компоненты вентиляции
    num_diffusers = calc['num_diffusers']
    main_duct_diameter_1 = 250  # mm (начальный участок)
    main_duct_diameter_2 = 160  # mm (после разветвления)
    branch_duct_diameter = 125  # mm
    supply_fan_diameter = 315  # mm
    silencer_diameter = 250  # mm
    exhaust_fan_diameter = 250  # mm (типовой для вытяжки)
    
    # Создание графика с соответствующим размером
    fig, ax = plt.subplots(figsize=(20, 14))
    
    # Отрисовка контура помещения
    room_rect = Rectangle((2, 0), room_length, room_width, 
                          fill=False, edgecolor='black', linewidth=2.5)
    ax.add_patch(room_rect)
    
    # Добавление размеров помещения
    ax.annotate('', xy=(2 + room_length, -0.5), xytext=(2, -0.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(2 + room_length/2, -0.8, f'{room_length} м', ha='center', fontsize=12, weight='bold')
    
    ax.annotate('', xy=(1.5, room_width), xytext=(1.5, 0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(1.0, room_width/2, f'{room_width} м', ha='center', fontsize=12, 
            rotation=90, va='center', weight='bold')
    
    # Отрисовка компонентов приточной системы (снаружи помещения слева)
    component_x = -2.5
    component_y = room_width / 2
    
    # Приточный вентилятор (315мм)
    fan = Circle((component_x, component_y), 0.4, 
                 fill=True, facecolor='lightcoral', edgecolor='darkred', linewidth=2)
    ax.add_patch(fan)
    ax.text(component_x, component_y, 'В', ha='center', va='center', 
            fontsize=14, weight='bold', color='darkred')
    ax.text(component_x, component_y - 0.7, 'Вентилятор\nØ315 мм', 
            ha='center', fontsize=9, weight='bold')
    
    # Компоненты вдоль приточного воздуховода
    comp_spacing = 1.2
    
    # Глушитель
    silencer_x = component_x + comp_spacing
    silencer = Rectangle((silencer_x - 0.15, component_y - 0.3), 0.3, 0.6,
                         fill=True, facecolor='lightgray', edgecolor='black', linewidth=1.5)
    ax.add_patch(silencer)
    ax.text(silencer_x, component_y + 0.6, 'Глушитель', ha='center', fontsize=8, weight='bold')
    
    # Фильтр
    filter_x = silencer_x + comp_spacing * 0.8
    filter_rect = Rectangle((filter_x - 0.15, component_y - 0.3), 0.3, 0.6,
                            fill=True, facecolor='lightyellow', edgecolor='orange', linewidth=1.5)
    ax.add_patch(filter_rect)
    # Добавление рисунка фильтра
    for i in range(5):
        ax.plot([filter_x - 0.1, filter_x + 0.1], 
                [component_y - 0.2 + i*0.1, component_y - 0.2 + i*0.1], 
                'orange', linewidth=1)
    ax.text(filter_x, component_y + 0.6, 'Фильтр', ha='center', fontsize=8, weight='bold')
    
    # Калорифер
    heater_x = filter_x + comp_spacing * 0.8
    heater = Rectangle((heater_x - 0.15, component_y - 0.3), 0.3, 0.6,
                       fill=True, facecolor='lightpink', edgecolor='red', linewidth=1.5)
    ax.add_patch(heater)
    ax.text(heater_x, component_y + 0.6, 'Калорифер', ha='center', fontsize=8, weight='bold')
    
    # Отрисовка соединительных воздуховодов до входа в помещение (КРАСНЫЙ для притока)
    # От вентилятора до глушителя
    ax.plot([component_x + 0.4, silencer_x - 0.15], [component_y, component_y], 
            'red', linewidth=4)
    # От глушителя до фильтра
    ax.plot([silencer_x + 0.15, filter_x - 0.15], [component_y, component_y], 
            'red', linewidth=4)
    # От фильтра до калорифера
    ax.plot([filter_x + 0.15, heater_x - 0.15], [component_y, component_y], 
            'red', linewidth=4)
    # От калорифера до входа в помещение
    ax.plot([heater_x + 0.15, 2], [component_y, component_y], 
            'red', linewidth=4)
    
    # Добавление стрелки, показывающей направление потока воздуха
    arrow = FancyArrowPatch((component_x - 0.6, component_y), (component_x - 0.45, component_y),
                           arrowstyle='->', mutation_scale=20, linewidth=2, color='red')
    ax.add_patch(arrow)
    ax.text(component_x - 0.8, component_y + 0.3, 'Приток', fontsize=9, weight='bold', color='red')
    
    # ПРИТОЧНАЯ СИСТЕМА - Положение магистрального воздуховода (верхняя часть помещения)
    supply_duct_y = room_width * 0.65  # Верхний участок для притока
    supply_duct_start_x = 2.5
    supply_duct_end_x = 2 + room_length - 0.5
    
    # Отрисовка начального участка 250мм (от входа до первого ответвления)
    initial_section_length = 2.0
    main_duct_width_250 = 0.25  # представление 250мм в масштабе
    main_duct_250 = Rectangle((supply_duct_start_x, supply_duct_y - main_duct_width_250/2),
                              initial_section_length, main_duct_width_250,
                              fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2)
    ax.add_patch(main_duct_250)
    
    # Отрисовка участка магистрали 160мм (после перехода)
    main_duct_width_160 = 0.16  # представление 160мм в масштабе
    transition_x = supply_duct_start_x + initial_section_length
    main_duct_160 = Rectangle((transition_x, supply_duct_y - main_duct_width_160/2),
                              supply_duct_end_x - transition_x, main_duct_width_160,
                              fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2)
    ax.add_patch(main_duct_160)
    
    # Отрисовка перехода с 250мм на 160мм
    transition_points = [
        [transition_x, supply_duct_y - main_duct_width_250/2],
        [transition_x + 0.3, supply_duct_y - main_duct_width_160/2],
        [transition_x + 0.3, supply_duct_y + main_duct_width_160/2],
        [transition_x, supply_duct_y + main_duct_width_250/2]
    ]
    transition = Polygon(transition_points, fill=True, facecolor='coral', edgecolor='red', linewidth=2)
    ax.add_patch(transition)
    
    # Соединение от входа в помещение до приточного воздуховода
    ax.plot([2, supply_duct_start_x], [component_y, supply_duct_y], 
            'red', linewidth=4, linestyle='--')
    
    # Добавление надписей приточного воздуховода
    ax.text(supply_duct_start_x + 1.0, supply_duct_y + 0.35, 'Ø250 мм',
            ha='center', fontsize=10, weight='bold', color='red')
    ax.text(2 + room_length/2, supply_duct_y + 0.35, 'Приточный воздуховод Ø160 мм',
            ha='center', fontsize=11, weight='bold', color='red')
    
    # Расчет положения диффузоров (равномерно распределены) - начало после перехода
    diffuser_start_x = transition_x + 0.5
    diffuser_span = supply_duct_end_x - diffuser_start_x
    spacing = diffuser_span / (num_diffusers - 1) if num_diffusers > 1 else 0
    diffuser_positions = []
    
    for i in range(num_diffusers):
        x_pos = diffuser_start_x + i * spacing if num_diffusers > 1 else 2 + room_length/2
        diffuser_positions.append((x_pos, supply_duct_y))
    
    # Отрисовка ПРИТОЧНЫХ ответвлений и диффузоров
    branch_width = 0.125  # представление 125мм в масштабе
    branch_length = 1.5  # длина ответвления
    
    for idx, (x, y) in enumerate(diffuser_positions):
        # Все ответвления направлены вверх для притока
        direction = 1
        
        # Отрисовка ответвления (красный для притока)
        branch = Rectangle((x - branch_width/2, y + main_duct_width_160/2),
                          branch_width, branch_length,
                          fill=True, facecolor='mistyrose', edgecolor='red', linewidth=1.5)
        ax.add_patch(branch)
        
        # Отрисовка диффузора (ДПУ-М 125)
        diffuser_y = y + main_duct_width_160/2 + branch_length
        diffuser = Circle((x, diffuser_y), 0.15, 
                         fill=True, facecolor='yellow', edgecolor='orange', linewidth=2)
        ax.add_patch(diffuser)
        
        # Добавление надписи диффузора
        label_offset = 0.3
        ax.text(x, diffuser_y + label_offset, f'ДПУ-М 125\n№{idx+1}',
                ha='center', va='center',
                fontsize=8, weight='bold')
        
        # Добавление надписи диаметра ответвления (только для первых нескольких, чтобы избежать загромождения)
        if idx < 3 or idx == num_diffusers - 1:
            branch_label_y = y + main_duct_width_160/2 + branch_length/2
            ax.text(x + 0.35, branch_label_y, 'Ø125', fontsize=7, color='red', rotation=90, va='center')
    
    # ВЫТЯЖНАЯ СИСТЕМА - Нижняя часть помещения
    exhaust_duct_y = room_width * 0.35  # Нижний участок для вытяжки
    exhaust_duct_start_x = 2.5
    exhaust_duct_end_x = 2 + room_length - 0.5
    
    # Отрисовка вытяжного магистрального воздуховода (160мм)
    exhaust_duct_width = 0.16
    exhaust_main = Rectangle((exhaust_duct_start_x, exhaust_duct_y - exhaust_duct_width/2),
                             exhaust_duct_end_x - exhaust_duct_start_x, exhaust_duct_width,
                             fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(exhaust_main)
    
    # Добавление надписи вытяжного воздуховода
    ax.text(2 + room_length/2, exhaust_duct_y - 0.35, 'Вытяжной воздуховод Ø160 мм',
            ha='center', fontsize=11, weight='bold', color='blue')
    
    # Расчет положения вытяжных решеток (такое же количество, как приточных диффузоров)
    num_grilles = num_diffusers
    exhaust_span = exhaust_duct_end_x - exhaust_duct_start_x
    exhaust_spacing = exhaust_span / (num_grilles - 1) if num_grilles > 1 else 0
    grille_positions = []
    for i in range(num_grilles):
        x_pos = exhaust_duct_start_x + i * exhaust_spacing if num_grilles > 1 else 2 + room_length/2
        grille_positions.append((x_pos, exhaust_duct_y))
    
    # Отрисовка ВЫТЯЖНЫХ ответвлений и решеток
    for idx, (x, y) in enumerate(grille_positions):
        # Все ответвления направлены вниз для вытяжки
        direction = -1
        
        # Отрисовка ответвления (синий для вытяжки)
        branch = Rectangle((x - branch_width/2, y - exhaust_duct_width/2 - branch_length),
                          branch_width, branch_length,
                          fill=True, facecolor='lightcyan', edgecolor='blue', linewidth=1.5)
        ax.add_patch(branch)
        
        # Отрисовка вытяжной решетки
        grille_y = y - exhaust_duct_width/2 - branch_length
        grille = Circle((x, grille_y), 0.15, 
                       fill=True, facecolor='lightyellow', edgecolor='darkorange', linewidth=2)
        ax.add_patch(grille)
        
        # Добавление надписи решетки
        label_offset = -0.3
        ax.text(x, grille_y + label_offset, f'Решетка\n№{idx+1}',
                ha='center', va='center',
                fontsize=8, weight='bold')
        
        # Добавление надписи диаметра ответвления (только для первых нескольких, чтобы избежать загромождения)
        if idx < 3 or idx == num_grilles - 1:
            branch_label_y = y - exhaust_duct_width/2 - branch_length/2
            ax.text(x - 0.35, branch_label_y, 'Ø125', fontsize=7, color='blue', rotation=90, va='center')
    
    # Отрисовка вытяжного вентилятора с правой стороны снаружи помещения
    exhaust_fan_x = 2 + room_length + 1.5
    exhaust_fan_y = exhaust_duct_y
    
    # Соединение вытяжного воздуховода с вентилятором
    ax.plot([exhaust_duct_end_x, exhaust_fan_x - 0.35], [exhaust_duct_y, exhaust_fan_y], 
            'blue', linewidth=4, linestyle='--')
    
    # Вытяжной вентилятор (250мм)
    exhaust_fan = Circle((exhaust_fan_x, exhaust_fan_y), 0.35, 
                        fill=True, facecolor='lightblue', edgecolor='darkblue', linewidth=2)
    ax.add_patch(exhaust_fan)
    ax.text(exhaust_fan_x, exhaust_fan_y, 'В', ha='center', va='center', 
            fontsize=14, weight='bold', color='darkblue')
    ax.text(exhaust_fan_x, exhaust_fan_y - 0.6, 'Вытяжной\nвентилятор\nØ250 мм', 
            ha='center', fontsize=9, weight='bold')
    
    # Добавление стрелки, показывающей направление вытяжного потока воздуха
    exhaust_arrow = FancyArrowPatch((exhaust_fan_x + 0.35, exhaust_fan_y), 
                                   (exhaust_fan_x + 0.55, exhaust_fan_y),
                                   arrowstyle='->', mutation_scale=20, linewidth=2, color='blue')
    ax.add_patch(exhaust_arrow)
    ax.text(exhaust_fan_x + 0.75, exhaust_fan_y + 0.3, 'Вытяжка', fontsize=9, weight='bold', color='blue')
    
    # Добавление блока технических характеристик
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
    
    # Блок потерь давления
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
    
    # Добавление блока характеристик с фоном
    specs_box = FancyBboxPatch((2 + room_length + 0.8, room_width - 7.2), 5.2, 7.0,
                               boxstyle="round,pad=0.1", 
                               facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(specs_box)
    ax.text(2 + room_length + 1.0, room_width - 0.4, specs_text,
            fontsize=8, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='none', edgecolor='none'))
    
    # Добавление блока потерь давления
    pressure_box = FancyBboxPatch((2 + room_length + 0.8, -1.2), 5.2, 5.8,
                                 boxstyle="round,pad=0.1", 
                                 facecolor='lightcyan', edgecolor='black', linewidth=2)
    ax.add_patch(pressure_box)
    ax.text(2 + room_length + 1.0, 4.4, pressure_text,
            fontsize=8, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='none', edgecolor='none'))
    
    # Добавление легенды
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
    
    # Установка заголовка
    plt.title('СХЕМА ПРИТОЧНО-ВЫТЯЖНОЙ ВЕНТИЛЯЦИИ НЕЖИЛОГО ПОМЕЩЕНИЯ\n(с расчетом количества диффузоров и потерь давления)',
             fontsize=15, weight='bold', pad=20)
    
    # Установка свойств осей
    ax.set_xlim(-3.5, 2 + room_length + 6.5)
    ax.set_ylim(-2, room_width + 1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Длина, м', fontsize=12, weight='bold')
    ax.set_ylabel('Ширина, м', fontsize=12, weight='bold')
    
    # Сохранение графика
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

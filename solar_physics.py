import math

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""

class Star():
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"
    """Признак объекта звезды"""

    m = 0
    """Масса звезды"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус звезды"""

    color = "red"
    """Цвет звезды"""

    image = None
    """Изображение звезды"""


class Planet():
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    type = "planet"
    """Признак объекта планеты"""

    m = 0
    """Масса планеты"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус планеты"""

    color = "green"
    """Цвет планеты"""

    image = None
    """Изображение планеты"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue

        dx = obj.x - body.x
        dy = obj.y - body.y
        r = math.sqrt(dx**2 + dy**2) #расстояние между телами
        
        if r == 0:
            continue
        F = gravitational_constant * body.m * obj.m / (r**2)
        #компоненты силы
        body.Fx += F * dx / r
        body.Fy += F * dy / r


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.
    Параметры:
    **body** — тело, которое нужно переместить.
    """
    #ускорение
    ax = body.Fx / body.m
    ay = body.Fy / body.m
    #скорость
    body.Vx += ax * dt
    body.Vy += ay * dt
    #координаты
    body.x += body.Vx * dt
    body.y += body.Vy * dt


def calculate_angular_velocity(body, central_body):
    """Вычисляет угловую скорость тела относительно центрального тела."""
    dx = body.x - central_body.x
    dy = body.y - central_body.y
    
    r = math.sqrt(dx**2 + dy**2)
    if r == 0:
        return 0
    Vx_rel = body.Vx - central_body.Vx
    Vy_rel = body.Vy - central_body.Vy
    
    angular_velocity = (dx * Vy_rel - dy * Vx_rel) / (r**2)
    return angular_velocity


def calculate_sector_velocity(body, central_body, dt):
    """Вычисляет секторную скорость (площадь, заметаемая радиус-вектором в единицу времени)."""
    x1 = body.x - central_body.x
    y1 = body.y - central_body.y
    
    x2 = x1 + body.Vx * dt
    y2 = y1 + body.Vy * dt
    area = 0.5 * abs(x1 * y2 - y1 * x2)
    sector_velocity = area / dt if dt > 0 else 0    # секторная скорость
    return sector_velocity


def check_keplers_second_law(space_objects, dt):
    """Проверяет второй закон Кеплера для всех планет."""
    results = {}
    stars = [obj for obj in space_objects if obj.type == "star"]
    if not stars:
        return results
    central_star = stars[0]
    for body in space_objects:
        if body.type == "planet":
            sector_velocity = calculate_sector_velocity(body, central_star, dt)
            angular_velocity = calculate_angular_velocity(body, central_star)
            distance = math.sqrt((body.x - central_star.x)**2 + (body.y - central_star.y)**2)
            results[body] = {
                'sector_velocity': sector_velocity,
                'angular_velocity': angular_velocity,
                'distance': distance
            }
    return results


def recalculate_space_objects_positions(space_objects, dt):
    #пересчитываем координаты объектов
    for body in space_objects:
        body.Fx = 0
        body.Fy = 0
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)
    kepler_results = check_keplers_second_law(space_objects, dt)  # проверка второго закона Кеплера
    
"""
    if kepler_results:
        first_planet = list(kepler_results.keys())[0]
        results = kepler_results[first_planet]
        print(f"Закон Кеплера: расстояние={results['distance']:.2e}, "
              f"секторная скорость={results['sector_velocity']:.2e}")
"""

if __name__ == "__main__":
    print("This module is not for direct call!")
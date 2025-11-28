from Data_Types import Planet, chart_details,Horror_scope,position
def make_navamsa_horoscope(d1: Horror_scope) -> Horror_scope:
    """returns a new Horror_scope (D9 Navamsha) with correct 0–3°20′ proportional degree mapping"""

    NAV_PART = 30 / 9  # 3°20' in decimal = 3.333333333°

    def navamsa_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)                    # 0–11
        inside = lon % 30                         # degrees inside rashi (0–30)
        part = int(inside // NAV_PART)            # navamsha index 0–8

        # proportion inside the part
        inside_part = inside - part * NAV_PART
        percent = inside_part / NAV_PART          # 0.0 – 1.0
        nav_deg = percent * 30                    # 0°–30° D9

        # Navamsha sign shift rule
        # Aries (0) Nav1 starts from Aries, Taurus from Capricorn, etc.
        # Equivalent rule:
        new_sign = (rashi * 9 + part) % 12        # final rashi index (0–11)

        return new_sign * 30 + nav_deg

    def convert(planet: Planet):
        nl = navamsa_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 9)

    asc_long = navamsa_long(d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position") else d1.ascendant.planet_position.longitude)
    asc = Planet.make("Ascendant", asc_long, 0)

    return Horror_scope(
        ascendant=asc,
        natal_chart=d1.natal_chart,
        Sun=convert(d1.Sun),
        Moon=convert(d1.Moon),
        Mercury=convert(d1.Mercury),
        Venus=convert(d1.Venus),
        Mars=convert(d1.Mars),
        Jupiter=convert(d1.Jupiter),
        Saturn=convert(d1.Saturn),
        Rahu=convert(d1.Rahu),
        Ketu=convert(d1.Ketu),
        weekday=d1.weekday,
        date=d1.date,
        month=d1.month,
        year=d1.year,
        hour=d1.hour,
        minute=d1.minute,
        second=d1.second,
        longitude=d1.longitude,
        latitude=d1.latitude,
    )

def make_drekkana_horoscope(d1: Horror_scope) -> Horror_scope:
    """returns a new Horror_scope (D3 Drekkana) derived from D1"""

    D3_PART = 30 / 3  # 10°

    def drekkana_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)          # original sign 0–11
        inside = lon % 30               # degree inside rashi (0–30)

        part = int(inside // D3_PART)   # 0,1,2 → 3 parts
        # Drekkanas jump by 4 signs each time
        new_rashi = (rashi + part * 4) % 12

        # % progress inside D3 part
        inside_part = inside - part * D3_PART     # 0–10°
        percent = inside_part / D3_PART           # 0.0–1.0
        new_deg = percent * 30                    # 0°–30°

        return new_rashi * 30 + new_deg

    def convert(planet: Planet):
        nl = drekkana_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 3)

    # Ascendant
    asc_lon = drekkana_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position") else d1.ascendant.planet_position.longitude
    )
    new_asc = Planet.make("Ascendant", asc_lon, 0)

    return Horror_scope(
        ascendant=new_asc,
        natal_chart=d1.natal_chart,
        Sun=convert(d1.Sun),
        Moon=convert(d1.Moon),
        Mercury=convert(d1.Mercury),
        Venus=convert(d1.Venus),
        Mars=convert(d1.Mars),
        Jupiter=convert(d1.Jupiter),
        Saturn=convert(d1.Saturn),
        Rahu=convert(d1.Rahu),
        Ketu=convert(d1.Ketu),
        weekday=d1.weekday,
        date=d1.date,
        month=d1.month,
        year=d1.year,
        hour=d1.hour,
        minute=d1.minute,
        second=d1.second,
        longitude=d1.longitude,
        latitude=d1.latitude,
    )

def make_d81_horoscope(d1: Horror_scope) -> Horror_scope:
    return make_navamsa_horoscope(make_navamsa_horoscope(d1))
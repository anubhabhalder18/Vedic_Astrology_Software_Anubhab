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

from Data_Types import Planet, Horror_scope

def make_d4_horoscope(d1: Horror_scope) -> Horror_scope:
    """D4 — Chaturthamsa chart calculation"""

    D4_PART = 30 / 4   # 7.5° per division

    def d4_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)             # 0–11
        inside = lon % 30                  # 0–30

        part = int(inside // D4_PART)      # 0,1,2,3 → 4 divisions

        # % inside the division
        inside_part = inside - part * D4_PART
        percent = inside_part / D4_PART
        new_deg = percent * 30             # 0°–30°

        # sign shift: jump 3 signs for every division
        new_rashi = (rashi + part * 3) % 12

        return new_rashi * 30 + new_deg

    def convert(planet: Planet):
        nl = d4_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 4)

    # Asc
    asc_lon = d4_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position") else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

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


from Data_Types import Planet, Horror_scope

def make_d10_horoscope(d1: Horror_scope) -> Horror_scope:
    """D10 — Dasamsa chart based on precise odd-even rule"""

    D10_PART = 30 / 10     # 3° per division

    def d10_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)      # 0–11 (0=Aries)
        inside = lon % 30

        part = int(inside // D10_PART)   # 0–9

        # convert rashi to 1-based for rule logic (1–12)
        rashi1 = rashi + 1

        if rashi1 % 2 == 1:  
            # odd signs → starts from same rashi
            new_rashi = (rashi + part) % 12
        else:
            # even signs → starts 8 signs ahead
            start = (rashi + 8) % 12
            new_rashi = (start + part) % 12

        # compute proportional degrees inside D10 part
        inside_part = inside - part * D10_PART
        percent = inside_part / D10_PART
        new_deg = percent * 30

        return new_rashi * 30 + new_deg

    def convert(planet: Planet):
        nl = d10_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 10)

    # Ascendant
    asc_lon = d10_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

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


from Data_Types import Planet, Horror_scope

# Mesha→Leo, Vrishabha→Virgo, Mithuna→Libra ... etc



def make_nadid30_horoscope(d1: Horror_scope):
    """
    start_array = list of 12 integers (0–11) defining from which rashi
    each sign's D30 first slice starts.
    Example: start_array[0] = rashi index of start rashi for Mesha (Aries).
    After that slice, signs progress forward.
    """
    start_array = [6,10,3,1,  5,9,7,11, 2,0,4,8 ]
    def d30_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # original sign 0–11
        deg_in_sign = lon % 30              # 0–30 degrees
        slice_index = int(deg_in_sign)      # 30 slices → 1° each (0–29)

        start_rashi = start_array[rashi]    # starting rashi of D30
        new_rashi = (start_rashi + slice_index) % 12

        # proportional degree mapping (0–30 deg stays same)
        return new_rashi * 30 + (deg_in_sign % 1) * 30

    def convert(pl: Planet):
        nl = d30_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 30)

    # Ascendant
    asc_lon = d30_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

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


from Data_Types import Planet, Horror_scope

def make_d16_horoscope(d1: Horror_scope) -> Horror_scope:
    """Returns D16 Shodashamsha chart using classical movable/fixed/dual starting-rashi rules."""
    
    D16_PART = 30 / 16  # 1.875° (1° 52' 30'')

    # rashi groups
    MOVABLE = {0, 3, 6, 9}        # Aries Cancer Libra Capricorn
    FIXED = {1, 4, 7, 10}         # Taurus Leo Scorpio Aquarius
    DUAL = {2, 5, 8, 11}          # Gemini Virgo Sagittarius Pisces

    # starting rashis for first shodashamsha
    START_MOV = 0   # Aries
    START_FIX = 4   # Leo
    START_DUAL = 8  # Sagittarius

    def d16_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)        # D1 sign 0–11
        inside = lon % 30             # 0–30°

        part = int(inside // D16_PART)  # shodashamsha index 0–15

        # find first part rashi
        if rashi in MOVABLE:
            base = START_MOV
        elif rashi in FIXED:
            base = START_FIX
        else:
            base = START_DUAL

        new_rashi = (base + part) % 12

        # proportional degree inside D16 part
        inside_part = inside - part * D16_PART
        percent = inside_part / D16_PART
        new_deg = percent * 30  # 0–30°

        return new_rashi * 30 + new_deg

    def convert(pl: Planet):
        nl = d16_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 16)

    # Ascendant convert
    asc_lon = d16_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

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

from Data_Types import Planet, Horror_scope

def make_d12_horoscope(d1: Horror_scope) -> Horror_scope:
    """Returns D12 Dwadasamsa (Parashari method) from D1."""

    D12_PART = 30 / 12  # 2.5° per part

    def d12_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)      # base sign 0–11
        inside = lon % 30           # degrees inside sign (0–30)

        # division index (0 to 11)
        part = int(inside // D12_PART)

        # D12 sign shift — starts from same D1 sign, then forward
        new_rashi = (rashi + part) % 12

        # proportional degree inside D12 section
        inside_part = inside - part * D12_PART
        percent = inside_part / D12_PART
        new_deg = percent * 30      # 0–30°

        return new_rashi * 30 + new_deg

    # convert generic planet
    def convert(pl: Planet):
        nl = d12_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 12)

    # Convert Asc
    asc_lon = d12_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

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


def make_d144_horoscope(d1:Horror_scope)->Horror_scope:
    return make_d12_horoscope(make_d12_horoscope(d1))
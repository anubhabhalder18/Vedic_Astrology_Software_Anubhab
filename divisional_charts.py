from Data_Types import Planet, chart_details,Horror_scope,position
from Data_Types import Planet, chart_details, Horror_scope, position

def make_navamsa_horoscope(d1: Horror_scope) -> Horror_scope:
    """returns a new Horror_scope (D9 Navamsha) with correct 0–3°20′ proportional degree mapping"""

    NAV_PART = 30 / 9  # 3°20' = 3.333333333°

    def navamsa_long(longitude: float) -> float:
        lon = longitude % 360
        rashi = int(lon // 30)                    # 0–11
        inside = lon % 30                         # 0–30 inside sign
        part = int(inside // NAV_PART)            # 0–8

        # proportion inside this navamsha division
        inside_part = inside - part * NAV_PART
        percent = inside_part / NAV_PART
        nav_deg = percent * 30                   # 0°–30° inside navamsha

        # final navamsha sign
        new_sign = (rashi * 9 + part) % 12
        return new_sign * 30 + nav_deg

    def convert(planet: Planet):
        nl = navamsa_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 9)

    # Ascendant conversion
    asc_long = navamsa_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 Convert Special Lagnas also
    nav_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            nl = navamsa_long(sp.planet_position.longitude)
            nav_special_lagnas.append(Planet.make(sp.name, nl, 0))

    # Construct Navamsa Horoscope (D9)
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
        special_lagnas=nav_special_lagnas      # 🔥 now included
    )

from Data_Types import Planet, chart_details, Horror_scope, position
from Data_Types import Planet, chart_details, Horror_scope, position

def make_drekkana_horoscope(d1: Horror_scope) -> Horror_scope:
    """returns a new Horror_scope (D3 Drekkana) derived from D1"""

    D3_PART = 30 / 3  # 10 degrees

    def drekkana_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)          # original sign 0–11
        inside = lon % 30               # 0–30 inside sign

        part = int(inside // D3_PART)   # 0,1,2 → 3 parts
        # Drekkana rule: jump 4 signs for each part
        new_rashi = (rashi + part * 4) % 12

        inside_part = inside - part * D3_PART     # 0–10°
        percent = inside_part / D3_PART           # 0.0–1.0
        new_deg = percent * 30                    # 0°–30° inside D3

        return new_rashi * 30 + new_deg

    def convert(planet: Planet):
        d3_lon = drekkana_long(planet.planet_position.longitude)
        return Planet.make(planet.name, d3_lon, planet.speed * 3)

    # Ascendant conversion
    asc_lon = drekkana_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    new_asc = Planet.make("Ascendant", asc_lon, 0)

    # 🔥 Convert SPECIAL LAGNAS too
    d3_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            d3_lon = drekkana_long(sp.planet_position.longitude)
            d3_special_lagnas.append(Planet.make(sp.name, d3_lon, 0))

    # Build the new D3 Horoscope object
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
        special_lagnas=d3_special_lagnas        # 🔥 Included now
    )

def make_d81_horoscope(d1: Horror_scope) -> Horror_scope:
    return make_navamsa_horoscope(make_navamsa_horoscope(d1))

from Data_Types import Planet, Horror_scope
from Data_Types import Planet, chart_details, Horror_scope, position

def make_d4_horoscope(d1: Horror_scope) -> Horror_scope:
    """D4 — Chaturthamsa chart calculation"""

    D4_PART = 30 / 4   # 7.5° per division

    def d4_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)             # 0–11
        inside = lon % 30                  # 0–30

        part = int(inside // D4_PART)      # 0,1,2,3 → 4 parts

        # progress inside division
        inside_part = inside - part * D4_PART
        percent = inside_part / D4_PART
        new_deg = percent * 30             # 0–30° inside D4

        # sign shift: jump 3 signs for each division
        new_rashi = (rashi + part * 3) % 12
        return new_rashi * 30 + new_deg

    def convert(planet: Planet):
        new_lon = d4_long(planet.planet_position.longitude)
        return Planet.make(planet.name, new_lon, planet.speed * 4)

    # Ascendant conversion
    asc_lon = d4_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

    # 🔥 Convert SPECIAL LAGNAS to D4 too
    d4_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            slon = d4_long(sp.planet_position.longitude)
            d4_special_lagnas.append(Planet.make(sp.name, slon, 0))

    # Build D4 Horoscope
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
        special_lagnas=d4_special_lagnas      # 🔥 Added
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

from Data_Types import Planet, chart_details, Horror_scope, position

def make_d10_horoscope(d1: Horror_scope) -> Horror_scope:
    """D10 — Dasamsa chart based on precise odd-even rule"""

    D10_PART = 30 / 10     # 3° per division

    def d10_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)      # 0–11
        inside = lon % 30           # 0–30 inside sign

        part = int(inside // D10_PART)   # 0–9 (10 parts)

        # Convert rashi to 1-based index for Dasamsa rule
        rashi1 = rashi + 1

        if rashi1 % 2 == 1:  
            # odd signs → Dasamsa begins from same sign
            new_rashi = (rashi + part) % 12
        else:
            # even signs → Dasamsa begins 8 signs ahead
            start = (rashi + 8) % 12
            new_rashi = (start + part) % 12

        inside_part = inside - part * D10_PART
        percent = inside_part / D10_PART
        new_deg = percent * 30        # 0–30° in D10

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

    # 🔥 Convert SPECIAL LAGNAS in D10 also
    d10_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            slon = d10_long(sp.planet_position.longitude)
            d10_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d10_special_lagnas       # 🔥 added here
    )


from Data_Types import Planet, Horror_scope

# Mesha→Leo, Vrishabha→Virgo, Mithuna→Libra ... etc

from Data_Types import Planet, chart_details, Horror_scope, position

def make_nadid30_horoscope(d1: Horror_scope):
    """
    D30 — Nādi Trimsamsa chart (30 divisions of 1° each)
    start_array indicates where each sign's 30 slices begin.
    """

    start_array = [6,10,3,1, 5,9,7,11, 2,0,4,8]   # fixed Nādi starting points per sign

    def d30_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # 0–11 base sign
        deg_in_sign = lon % 30               # 0–30°
        slice_index = int(deg_in_sign)       # 1° slices → 0–29

        start_rashi = start_array[rashi]     # start point for that sign
        new_rashi = (start_rashi + slice_index) % 12

        # Keep proportional degree inside slice
        return new_rashi * 30 + (deg_in_sign % 1) * 30

    def convert(pl: Planet):
        nl = d30_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 30)

    # Ascendant conversion
    asc_lon = d30_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

    # 🔥 Special Lagnas conversion to D30 (Nādi)
    d30_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            slon = d30_long(sp.planet_position.longitude)
            d30_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d30_special_lagnas      # 🔥 added here
    )


from Data_Types import Planet, Horror_scope
from Data_Types import Planet, chart_details, Horror_scope, position

def make_d16_horoscope(d1: Horror_scope) -> Horror_scope:
    """Returns D16 Shodashamsha chart using classical movable/fixed/dual starting-rashi rules."""

    D16_PART = 30 / 16  # 1.875° per part

    MOVABLE = {0, 3, 6, 9}        # Aries, Cancer, Libra, Capricorn
    FIXED = {1, 4, 7, 10}         # Taurus, Leo, Scorpio, Aquarius
    DUAL = {2, 5, 8, 11}          # Gemini, Virgo, Sagittarius, Pisces

    START_MOV = 0   # Aries
    START_FIX = 4   # Leo
    START_DUAL = 8  # Sagittarius

    def d16_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)
        inside = lon % 30

        part = int(inside // D16_PART)  # 0–15

        if rashi in MOVABLE:
            base = START_MOV
        elif rashi in FIXED:
            base = START_FIX
        else:
            base = START_DUAL

        new_rashi = (base + part) % 12

        inside_part = inside - part * D16_PART
        percent = inside_part / D16_PART
        new_deg = percent * 30

        return new_rashi * 30 + new_deg

    def convert(pl: Planet):
        nl = d16_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 16)

    # Ascendant
    asc_lon = d16_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

    # 🔥 SPECIAL LAGNAS conversion to D16 (Shodashamsha)
    d16_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            slon = d16_long(sp.planet_position.longitude)
            d16_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d16_special_lagnas   # 🔥 added here
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
from Data_Types import Planet, chart_details, Horror_scope, position

def make_d12_horoscope(d1: Horror_scope) -> Horror_scope:
    """Returns D12 Dwadasamsa (Parashari method) from D1."""

    D12_PART = 30 / 12  # 2.5° per part

    def d12_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)      # 0–11
        inside = lon % 30           # 0–30° inside sign

        part = int(inside // D12_PART)   # 0–11

        # Dwadasamsa starts from same sign, then moves forward in order
        new_rashi = (rashi + part) % 12

        inside_part = inside - part * D12_PART
        percent = inside_part / D12_PART
        new_deg = percent * 30           # 0–30° inside D12

        return new_rashi * 30 + new_deg

    def convert(pl: Planet):
        nl = d12_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 12)

    # Ascendant conversion
    asc_lon = d12_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_lon, 0)

    # 🔥 Special Lagnas → Converted to D12
    d12_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            slon = d12_long(sp.planet_position.longitude)
            d12_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d12_special_lagnas    # 🔥 added here
    )


def make_d144_horoscope(d1:Horror_scope)->Horror_scope:
    return make_d12_horoscope(make_d12_horoscope(d1))



from Data_Types import Planet, chart_details, Horror_scope, position

def make_d24_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D24 (Chaturvimshamsha) chart based on odd/even sign starting rule."""

    D24_PART = 30 / 24  # 1.25° per division

    def d24_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)       # 0–11
        inside = lon % 30            # 0–30°

        part = int(inside // D24_PART)  # 0–23

        # Odd-even sign rule:
        # rashi index even  -> starts from Leo (4)
        # rashi index odd   -> starts from Cancer (3)
        if rashi % 2 == 0:
            first_sign = 4   # Leo
        else:
            first_sign = 3   # Cancer

        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D24_PART
        percent = inside_part / D24_PART
        new_deg = percent * 30         # 0–30°

        return new_sign * 30 + new_deg

    def convert(pl: Planet):
        nl = d24_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 24)

    # Ascendant
    asc_long = d24_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 Convert SPECIAL LAGNAS also into D24 (not recomputed)
    d24_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d24_long(sp.planet_position.longitude)
            d24_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d24_special_lagnas      # 🔥 NOW INCLUDED
    )

from Data_Types import Planet, chart_details, Horror_scope, position

def make_d27_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D27 (Saptavimshamsha) chart according to element-based starting rule."""

    D27_PART = 30 / 27  # 1.111111111° per segment

    def d27_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)          # sign index 0–11
        inside = lon % 30               # 0–30° inside sign
        part = int(inside // D27_PART)  # 0–26

        # Determine element group starting point
        if rashi in (0, 4, 8):          # Fire signs
            first_sign = 0              # Aries
        elif rashi in (1, 5, 9):        # Earth signs
            first_sign = 3              # Cancer
        elif rashi in (2, 6, 10):       # Air signs
            first_sign = 6              # Libra
        else:                           # Water signs
            first_sign = 9              # Capricorn

        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D27_PART
        percent = inside_part / D27_PART
        d27_deg = percent * 30          # map to 0–30°

        return new_sign * 30 + d27_deg

    def convert(pl: Planet):
        nl = d27_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 27)

    # Ascendant conversion
    asc_long = d27_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 Convert Special Lagnas also (do NOT recompute)
    d27_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas is not None:
        for sp in d1.special_lagnas:
            slon = d27_long(sp.planet_position.longitude)
            d27_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d27_special_lagnas     # 🔥 added here
    )

def make_d30_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return Parashari D30 Trimshamsha chart based on fixed sign mapping tables."""

    odd_signs = [0, 2, 4, 6, 8, 10]      # Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
    even_signs = [1, 3, 5, 7, 9, 11]     # Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces

    # D30 sign mapping tables (index matched with degree segment)
    odd_d30 = [
        0,   # Aries  (0–5) Mars
        10,  # Aquarius (5–10) Saturn
        8,   # Sagittarius (10–18) Jupiter
        2,   # Gemini (18–25) Mercury
        6    # Libra (25–30) Venus
    ]

    even_d30 = [
        1,   # Taurus (0–5) Venus
        5,   # Virgo (5–12) Mercury
        11,  # Pisces (12–20) Jupiter
        9,   # Capricorn (20–25) Saturn
        7    # Scorpio (25–30) Mars
    ]

    def d30_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)        # 0–11
        inside = lon % 30             # degrees inside the sign

        # Odd / Even sign selection
        if rashi in odd_signs:
            # ODD SIGN TABLE
            if inside < 5:
                d30_sign = odd_d30[0]
            elif inside < 10:
                d30_sign = odd_d30[1]
            elif inside < 18:
                d30_sign = odd_d30[2]
            elif inside < 25:
                d30_sign = odd_d30[3]
            else:
                d30_sign = odd_d30[4]
        else:
            # EVEN SIGN TABLE
            if inside < 5:
                d30_sign = even_d30[0]
            elif inside < 12:
                d30_sign = even_d30[1]
            elif inside < 20:
                d30_sign = even_d30[2]
            elif inside < 25:
                d30_sign = even_d30[3]
            else:
                d30_sign = even_d30[4]

        # Trimshamsha degree is 0° inside allotted sign
        return d30_sign * 30

    def convert(planet: Planet):
        nl = d30_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 30)

    asc_long = d30_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
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

from Data_Types import Planet, chart_details, Horror_scope, position

def make_d30_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return Parashari D30 Trimshamsha chart based on fixed sign mapping tables."""

    odd_signs = [0, 2, 4, 6, 8, 10]       # Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
    even_signs = [1, 3, 5, 7, 9, 11]      # Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces

    # D30 mapping tables
    odd_d30 = [0, 10, 8, 2, 6]   # Aries → Aquarius → Sagittarius → Gemini → Libra
    even_d30 = [1, 5, 11, 9, 7]  # Taurus → Virgo → Pisces → Capricorn → Scorpio

    def d30_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)
        inside = lon % 30

        if rashi in odd_signs:
            if inside < 5:
                d30_sign = odd_d30[0]
            elif inside < 10:
                d30_sign = odd_d30[1]
            elif inside < 18:
                d30_sign = odd_d30[2]
            elif inside < 25:
                d30_sign = odd_d30[3]
            else:
                d30_sign = odd_d30[4]
        else:
            if inside < 5:
                d30_sign = even_d30[0]
            elif inside < 12:
                d30_sign = even_d30[1]
            elif inside < 20:
                d30_sign = even_d30[2]
            elif inside < 25:
                d30_sign = even_d30[3]
            else:
                d30_sign = even_d30[4]

        # Always start from 0° inside mapped sign
        return d30_sign * 30

    def convert(pl: Planet):
        nl = d30_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 30)

    # Ascendant
    asc_long = d30_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 Apply D30 mapping to Special Lagnas too (DO NOT recalculate them)
    d30_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d30_long(sp.planet_position.longitude)
            d30_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d30_special_lagnas     # 🔥 included here
    )
from Data_Types import Planet, chart_details, Horror_scope, position

def make_d20_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D20 (Vimsamsa) chart as per Parashari method with special lagnas included."""

    D20_PART = 30 / 20   # 1.5° per division

    movable = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
    fixed   = [1, 4, 7, 10]      # Taurus, Leo, Scorpio, Aquarius
    dual    = [2, 5, 8, 11]      # Gemini, Virgo, Sagittarius, Pisces

    def d20_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)
        inside = lon % 30
        part = int(inside // D20_PART)    # 0–19

        # Determine starting sign
        if rashi in movable:
            first_sign = 0      # Aries
        elif rashi in fixed:
            first_sign = 8      # Sagittarius
        else:
            first_sign = 4      # Leo

        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D20_PART
        percent = inside_part / D20_PART
        d20_deg = percent * 30

        return new_sign * 30 + d20_deg

    def convert(pl: Planet):
        nl = d20_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 20)

    # Ascendant
    asc_long = d20_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 Convert SPECIAL LAGNAS — do NOT recalculate them
    d20_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d20_long(sp.planet_position.longitude)
            d20_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d20_special_lagnas      # 🔥 added here
    )

from Data_Types import Planet, chart_details, Horror_scope, position

def make_d40_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D40 (Khavedamsa) chart as per Parashari method with special lagnas included."""

    D40_PART = 30 / 40  # 0.75° per division

    odd_signs  = [0, 2, 4, 6, 8, 10]      # Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
    even_signs = [1, 3, 5, 7, 9, 11]      # Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces

    def d40_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)
        inside = lon % 30
        part = int(inside // D40_PART)      # 0–39

        # Starting sign
        if rashi in odd_signs:
            first_sign = 0    # Aries
        else:
            first_sign = 6    # Libra

        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D40_PART
        percent = inside_part / D40_PART
        d40_deg = percent * 30              # proportional degree inside new sign

        return new_sign * 30 + d40_deg

    def convert(pl: Planet):
        nl = d40_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 40)

    # Ascendant conversion
    asc_long = d40_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 Convert SPECIAL LAGNAS — do NOT recompute them
    d40_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d40_long(sp.planet_position.longitude)
            d40_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d40_special_lagnas       # 🔥 stored here
    )


from Data_Types import Planet, chart_details, Horror_scope, position

def make_d45_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D45 (Akshavedamsa) chart according to Parashara method with special lagnas included."""

    D45_PART = 30 / 45  # 0.6666666667 degrees per part (2/3°)

    movable = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
    fixed   = [1, 4, 7, 10]      # Taurus, Leo, Scorpio, Aquarius
    dual    = [2, 5, 8, 11]      # Gemini, Virgo, Sagittarius, Pisces

    def d45_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)
        inside = lon % 30
        part = int(inside // D45_PART)     # 0–44

        if rashi in movable:
            first_sign = 0      # Aries
        elif rashi in fixed:
            first_sign = 4      # Leo
        else:
            first_sign = 8      # Sagittarius

        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D45_PART
        percent = inside_part / D45_PART
        d45_deg = percent * 30            # 0–30° inside D45 sign

        return new_sign * 30 + d45_deg

    def convert(pl: Planet):
        nl = d45_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 45)

    # Ascendant conversion
    asc_long = d45_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 SPECIAL LAGNAS — inherit & convert (DO NOT recalculate)
    d45_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d45_long(sp.planet_position.longitude)
            d45_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d45_special_lagnas      # 🔥 stored here
    )
from Data_Types import Planet, chart_details, Horror_scope, position

def make_d60_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D60 (Shashtiamsa) chart according to Parashari method with special lagnas included."""

    D60_PART = 30 / 60   # 0.5 degrees per division

    def d60_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)             # 0–11 base sign
        inside = lon % 30                  # 0–30 degrees
        part = int(inside // D60_PART)     # 0–59 segment index

        # 1st Shashtiamsa starts from the same rashi
        first_sign = rashi

        # Each Siṁshāṁśa moves 1 sign forward cyclically
        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D60_PART
        percent = inside_part / D60_PART
        d60_deg = percent * 30             # mapped 0–30 degrees

        return new_sign * 30 + d60_deg

    def convert(pl: Planet):
        nl = d60_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 60)

    # Ascendant
    asc_long = d60_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 SPECIAL LAGNAS — mapping only (NO recalculation)
    d60_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d60_long(sp.planet_position.longitude)
            d60_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d60_special_lagnas     # 🔥 added here
    )

def make_d5_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D5 (Panchamsa) chart as per Parashari method."""

    D5_PART = 30 / 5  # 6 degrees per division

    movable = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
    fixed   = [1, 4, 7, 10]      # Taurus, Leo, Scorpio, Aquarius
    dual    = [2, 5, 8, 11]      # Gemini, Virgo, Sagittarius, Pisces

    def d5_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)                # base sign index 0–11
        inside = lon % 30                     # degree inside base sign
        part = int(inside // D5_PART)         # 0–4 five divisions inside sign

        # Determine the FIRST Panchamsa sign based on nature
        if rashi in movable:
            first_sign = rashi
        elif rashi in fixed:
            first_sign = (rashi + 4) % 12     # 5th from sign = +4
        else:
            first_sign = (rashi + 8) % 12     # 9th from sign = +8

        # Panchamsa sign = first sign + part ( cyclic order )
        new_sign = (first_sign + part) % 12

        # Degree inside part proportionally mapped to 0–30
        inside_part = inside - part * D5_PART
        percent = inside_part / D5_PART
        d5_deg = percent * 30

        return new_sign * 30 + d5_deg

    def convert(planet: Planet):
        nl = d5_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 5)

    asc_long = d5_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
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

from Data_Types import Planet, chart_details, Horror_scope, position

def make_d5_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D5 (Panchamsa) chart as per Parashari method with special lagnas included."""

    D5_PART = 30 / 5  # 6 degrees per division

    movable = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
    fixed   = [1, 4, 7, 10]      # Taurus, Leo, Scorpio, Aquarius
    dual    = [2, 5, 8, 11]      # Gemini, Virgo, Sagittarius, Pisces

    def d5_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)                 # base sign 0–11
        inside = lon % 30                      # 0–30° inside sign
        part = int(inside // D5_PART)          # 0–4

        # Starting Panchamsa sign
        if rashi in movable:
            first_sign = rashi
        elif rashi in fixed:
            first_sign = (rashi + 4) % 12      # 5th from sign
        else:
            first_sign = (rashi + 8) % 12      # 9th from sign

        new_sign = (first_sign + part) % 12

        inside_part = inside - part * D5_PART
        percent = inside_part / D5_PART
        d5_deg = percent * 30                 # 0–30°

        return new_sign * 30 + d5_deg

    def convert(pl: Planet):
        nl = d5_long(pl.planet_position.longitude)
        return Planet.make(pl.name, nl, pl.speed * 5)

    # Ascendant conversion
    asc_long = d5_long(
        d1.ascendant.longitude if not hasattr(d1.ascendant, "planet_position")
        else d1.ascendant.planet_position.longitude
    )
    asc = Planet.make("Ascendant", asc_long, 0)

    # 🔥 SPECIAL LAGNAS — map only, do NOT recompute
    d5_special_lagnas = []
    if hasattr(d1, "special_lagnas") and d1.special_lagnas:
        for sp in d1.special_lagnas:
            slon = d5_long(sp.planet_position.longitude)
            d5_special_lagnas.append(Planet.make(sp.name, slon, 0))

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
        special_lagnas=d5_special_lagnas      # 🔥 added here
    )

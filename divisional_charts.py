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



def make_d24_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D24 (Chaturvimshamsha) chart based on odd/even sign starting signs rule."""

    D24_PART = 30 / 24  # 1.25 degrees per segment

    def d24_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # base rashi 0–11
        inside = lon % 30                    # degrees inside rashi (0–30)
        part = int(inside // D24_PART)       # D24 segment index 0–23

        # Find baseline sign index of segment-1 depending on odd/even sign
        if rashi % 2 == 0:   # rashi index even → odd sign numbers (Aries = 0 index so even index = odd sign)
            first_sign = 4   # Leo (index 4)
        else:
            first_sign = 3   # Cancer (index 3)

        # New sign mapping
        new_sign = (first_sign + part) % 12

        # Degree inside segment
        inside_part = inside - part * D24_PART
        percent = inside_part / D24_PART
        d24_deg = percent * 30              # map to 0–30°

        return new_sign * 30 + d24_deg

    def convert(planet: Planet):
        nl = d24_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 24)

    asc_long = d24_long(
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


def make_d27_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D27 (Saptavimshamsha) chart according to element-based starting rule."""

    D27_PART = 30 / 27  # 1.111111111° per segment

    def d27_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # base sign 0–11
        inside = lon % 30                    # degrees inside the sign
        part = int(inside // D27_PART)       # D27 segment index 0–26

        # Determine element of sign and starting sign
        if rashi in (0, 4, 8):         # Aries, Leo, Sagittarius → Fire
            first_sign = 0             # Aries
        elif rashi in (1, 5, 9):       # Taurus, Virgo, Capricorn → Earth
            first_sign = 3             # Cancer
        elif rashi in (2, 6, 10):      # Gemini, Libra, Aquarius → Air
            first_sign = 6             # Libra
        else:                          # Cancer, Scorpio, Pisces → Water
            first_sign = 9             # Capricorn

        # New sign = starting_point + segment index moving direct cyclically
        new_sign = (first_sign + part) % 12

        # Degree inside segment mapped to 0–30°
        inside_part = inside - part * D27_PART
        percent = inside_part / D27_PART
        d27_deg = percent * 30

        return new_sign * 30 + d27_deg

    def convert(planet: Planet):
        nl = d27_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 27)

    asc_long = d27_long(
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


def make_d20_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D20 (Vimsamsa) chart as per Parashari method."""

    D20_PART = 30 / 20   # 1.5 degrees per division

    # Lists of rashi indices by nature
    movable = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
    fixed   = [1, 4, 7, 10]      # Taurus, Leo, Scorpio, Aquarius
    dual    = [2, 5, 8, 11]      # Gemini, Virgo, Sagittarius, Pisces

    def d20_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # sign index 0–11
        inside = lon % 30                    # degrees inside the sign
        part = int(inside // D20_PART)       # 0–19 Vimsamsa segment

        # Determine start sign based on nature
        if rashi in movable:
            first_sign = 0      # Aries
        elif rashi in fixed:
            first_sign = 8      # Sagittarius
        else:
            first_sign = 4      # Leo

        # Vimsamsa sign = first sign + segment index (cyclic zodiac)
        new_sign = (first_sign + part) % 12

        # Convert to final longitude (degree inside vimshamsa = proportional)
        inside_part = inside - part * D20_PART
        percent = inside_part / D20_PART
        d20_deg = percent * 30               # 0–30° inside D20 sign

        return new_sign * 30 + d20_deg

    def convert(planet: Planet):
        nl = d20_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 20)

    asc_long = d20_long(
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

def make_d40_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D40 (Khavedamsa) chart as per Parashari method."""

    D40_PART = 30 / 40  # 0.75 degrees per division

    odd_signs = [0, 2, 4, 6, 8, 10]      # Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
    even_signs = [1, 3, 5, 7, 9, 11]     # Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces

    def d40_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # sign number 0–11
        inside = lon % 30                    # degrees in sign
        part = int(inside // D40_PART)       # 0–39 division

        # Starting sign based on odd/even
        if rashi in odd_signs:
            first_sign = 0     # Aries
        else:
            first_sign = 6     # Libra

        # D40 sign = start sign + part (cyclic)
        new_sign = (first_sign + part) % 12

        # degree inside segment proportionally mapped to 0–30
        inside_part = inside - part * D40_PART
        percent = inside_part / D40_PART
        d40_deg = percent * 30

        return new_sign * 30 + d40_deg

    def convert(planet: Planet):
        nl = d40_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 40)

    asc_long = d40_long(
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


def make_d45_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D45 (Akshavedamsa) chart according to Parashara method."""

    D45_PART = 30 / 45  # 0.6666666667 degrees per part (2/3 degree)

    movable = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
    fixed   = [1, 4, 7, 10]      # Taurus, Leo, Scorpio, Aquarius
    dual    = [2, 5, 8, 11]      # Gemini, Virgo, Sagittarius, Pisces

    def d45_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)               # 0–11 sign index
        inside = lon % 30                    # degrees inside sign
        part = int(inside // D45_PART)       # 0–44 division index

        # Determine starting sign
        if rashi in movable:
            first_sign = 0      # Aries
        elif rashi in fixed:
            first_sign = 4      # Leo
        else:
            first_sign = 8      # Sagittarius

        # D45 sign = first sign + part index (cyclic)
        new_sign = (first_sign + part) % 12

        # Degree inside D45 division proportionally mapped to 0–30
        inside_part = inside - part * D45_PART
        percent = inside_part / D45_PART
        d45_deg = percent * 30

        return new_sign * 30 + d45_deg

    def convert(planet: Planet):
        nl = d45_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 45)

    asc_long = d45_long(
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


def make_d60_horoscope(d1: Horror_scope) -> Horror_scope:
    """Return D60 (Shashtiamsa) chart according to Parashari method."""

    D60_PART = 30 / 60   # 0.5 degrees per division

    def d60_long(longitude):
        lon = longitude % 360
        rashi = int(lon // 30)              # base sign (0–11)
        inside = lon % 30                   # degrees inside sign
        part = int(inside // D60_PART)      # segment index 0–59

        # First D60 sign = same as the rashi sign where the planet is placed
        first_sign = rashi

        # Each part moves 1 sign forward cyclically
        new_sign = (first_sign + part) % 12

        # Degree inside part proportionally mapped to 0–30
        inside_part = inside - part * D60_PART
        percent = inside_part / D60_PART
        d60_deg = percent * 30

        return new_sign * 30 + d60_deg

    def convert(planet: Planet):
        nl = d60_long(planet.planet_position.longitude)
        return Planet.make(planet.name, nl, planet.speed * 60)

    asc_long = d60_long(
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


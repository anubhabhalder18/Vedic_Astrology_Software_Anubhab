import swisseph as swe
swe.set_ephe_path('ephe')
swe.set_sid_mode(swe.SIDM_TRUE_CITRA)

from Data_Types import Planet, chart_details, Horror_scope
from Convert import read_ast

# ---- Astral for Sunrise ----
from astral.sun import sun
from astral import LocationInfo
from datetime import date

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
}

LAGNA_SPEEDS = {
    "Bhava Lagna (BL)": 15,
    "Hora Lagna (HL)": 30,
    "3rd house Lagna (3L)": 45,
    "Vidya Lagna (ViL)": 60,
    "5th house Lagna (5L)": 75,
    "6th Lagna (6L)": 90,
    "Shiva Lagna (ML)": 105,
    "8th house Lagna (8L)": 120,
    "Vyasa Lagna (VyL)": 135,
    "10th house Lagna (10L)": 150,
    "11th house Lagna (11L)": 165,
    "12th Lagna (YL)": 180,
    "d24 lagna": 15 * 24,
    "d45 lagna": 15 * 45,
    "d40 lagna": 15 * 40
}

# -------------------------------------------------------
# WORKING LOCAL SUNRISE (ASTRAL, RESPECTING chart.timezone)
# -------------------------------------------------------
from astral import Observer
from astral.sun import dawn, dusk
from datetime import date, timedelta, timezone
from Data_Types import chart_details

HALF_DISC_DEPRESSION = -0.4338   # center of sun visible

def _local_tz_from_chart(chart: chart_details) -> timezone:
    offset_hours = -chart.timezone        # your convention
    return timezone(timedelta(hours=offset_hours))


def get_sunrise_decimal(chart: chart_details) -> float:
    """LOCAL sunrise when Sun's CENTRE first becomes visible."""
    observer = Observer(
        latitude=chart.latitude,
        longitude=chart.longitude,
        elevation=getattr(chart, "altidude", 0.0),
    )
    tz = _local_tz_from_chart(chart)

    sr_local = dawn(
        observer,
        date=date(chart.year, chart.month, chart.date),
        tzinfo=tz,
        depression=HALF_DISC_DEPRESSION     # <-- mid-disc SUNRISE
    )

    return sr_local.hour + sr_local.minute / 60 + sr_local.second / 3600.0


def get_sunset_decimal(chart: chart_details) -> float:
    """LOCAL sunset when Sun's CENTRE last disappears."""
    observer = Observer(
        latitude=chart.latitude,
        longitude=chart.longitude,
        elevation=getattr(chart, "altidude", 0.0),
    )
    tz = _local_tz_from_chart(chart)

    ss_local = dusk(
        observer,
        date=date(chart.year, chart.month, chart.date),
        tzinfo=tz,
        depression=HALF_DISC_DEPRESSION     # <-- mid-disc SUNSET
    )

    return ss_local.hour + ss_local.minute / 60 + ss_local.second / 3600.0


# -------------------------------------------------------
# ASCENDANT
# -------------------------------------------------------
def get_asc(chart: chart_details):
    jd_ut = swe.julday(chart.year, chart.month, chart.date,
                       chart.time_in_decimal() + chart.timezone)

    asc = swe.houses_ex(jd_ut, chart.latitude, chart.longitude, b'P',
                        swe.FLG_SWIEPH | swe.FLG_TRUEPOS | swe.FLG_SIDEREAL)[0][0]

    next_asc = swe.houses_ex(jd_ut + 1, chart.latitude, chart.longitude, b'P',
                             swe.FLG_SWIEPH | swe.FLG_TRUEPOS | swe.FLG_SIDEREAL)[0][0]
    speed = (next_asc - asc) * 24
    return Planet.make("Ascendant", asc, speed)


# -------------------------------------------------------
# PLANETS
# -------------------------------------------------------
def get_planet(chart: chart_details, planet: str):
    is_ketu = (planet == "Ketu")
    planet_key = "Rahu" if is_ketu else planet

    jd_ut = swe.julday(chart.year, chart.month, chart.date,
                       chart.hour + chart.minute / 60 + chart.second / 3600 + chart.timezone)

    swe.set_topo(chart.longitude, chart.latitude, chart.altidude)
    body_id = PLANETS[planet_key]

    lon = swe.calc_ut(jd_ut, body_id,
                      swe.FLG_SWIEPH | swe.FLG_TRUEPOS | swe.FLG_SIDEREAL)[0][0]
    if is_ketu:
        lon = (lon + 180) % 360

    next_lon = swe.calc_ut(jd_ut + 1/86400, body_id,
                           swe.FLG_SWIEPH | swe.FLG_TRUEPOS | swe.FLG_SIDEREAL)[0][0]
    if is_ketu:
        next_lon = (next_lon + 180) % 360

    speed = (next_lon - lon) * 86400
    return Planet.make(planet, lon, speed)


# -------------------------------------------------------
# SPECIAL LAGNAS
# -------------------------------------------------------
def calculate_special_lagnas(chart: chart_details, sunrise_sun_long: float):
    birth_time = chart.hour + chart.minute/60 + chart.second/3600
    sunrise = get_sunrise_decimal(chart)      # LOCAL sunrise time
    elapsed = birth_time - sunrise            # hours since sunrise
    if(elapsed<0):
        elapsed+=24
    sun_deg=elapsed*1/24
    result = []
    for name, speed in LAGNA_SPEEDS.items():
        # exact GUI formula: base_deg + (speed * elapsed + 30)
        final = (sunrise_sun_long-sun_deg + (speed * elapsed )) % 360
        result.append(Planet.make(name, final, 0))
    return result


# -------------------------------------------------------
# HELPER: LOCAL SUNRISE DECIMAL → JULIAN DAY (UT)
# -------------------------------------------------------
def sunrise_decimal_to_jd_ut(chart: chart_details, sunrise_local_dec: float) -> float:
    """
    Convert LOCAL sunrise decimal to JD in UT for Swiss Ephemeris.

    Your convention: UT = local + timezone
    """
    ut_dec = sunrise_local_dec + chart.timezone
    jd_sunrise_ut = swe.julday(chart.year, chart.month, chart.date, ut_dec)
    return jd_sunrise_ut


# -------------------------------------------------------
# HOROSCOPE
# -------------------------------------------------------
def make_horoscope(chart: chart_details):
    jd_ut = swe.julday(chart.year, chart.month, chart.date,
                       chart.hour + chart.minute / 60 + chart.second / 3600 + chart.timezone)
    weekday = [ 'Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday','Sunday'][swe.day_of_week(jd_ut)]

    asc = get_asc(chart)
    sun = get_planet(chart, "Sun")
    moon = get_planet(chart, "Moon")
    mercury = get_planet(chart, "Mercury")
    venus = get_planet(chart, "Venus")
    mars = get_planet(chart, "Mars")
    jupiter = get_planet(chart, "Jupiter")
    saturn = get_planet(chart, "Saturn")
    rahu = get_planet(chart, "Rahu")
    ketu = get_planet(chart, "Ketu")

    # ---- Sun at sunrise (if you really want sunrise Sun) ----
    sunrise_dec = get_sunrise_decimal(chart)            # local
    jd_sunrise_ut = sunrise_decimal_to_jd_ut(chart, sunrise_dec)
    swe.set_topo(chart.longitude, chart.latitude, chart.altidude)
    body_id = swe.SUN

    rising_sun_long = swe.calc_ut(jd_sunrise_ut, body_id,
                      swe.FLG_SWIEPH | swe.FLG_TRUEPOS | swe.FLG_SIDEREAL)[0][0]
    # Use sunrise Sun longitude for special lagnas:
    sun_long = rising_sun_long
    special_lagnas = calculate_special_lagnas(chart, sun_long)

    horoscope_obj = Horror_scope(
        ascendant=asc,
        natal_chart=chart,
        Sun=sun,
        Moon=moon,
        Mercury=mercury,
        Venus=venus,
        Mars=mars,
        Jupiter=jupiter,
        Saturn=saturn,
        Rahu=rahu,
        Ketu=ketu,
        weekday=weekday,
        date=chart.date,
        month=chart.month,
        year=chart.year,
        hour=chart.hour,
        minute=chart.minute,
        second=chart.second,
        longitude=chart.longitude,
        latitude=chart.latitude,
        special_lagnas=special_lagnas
    )
    return horoscope_obj


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
if __name__ == "__main__":
    chart = read_ast("a.ast")

    nat_chart = make_horoscope(chart)

    print("\n----- SPECIAL LAGNAS -----")
    for sp in nat_chart.special_lagnas:
        print(f"{sp.name}: {sp.planet_position.longitude:.4f}°")

    # Debug sunrise / sunset if you want to see them:
    sr_dec = get_sunrise_decimal(chart)
    ss_dec = get_sunset_decimal(chart)
    print(f"\nSunrise (local, decimal hours): {sr_dec:.4f}")
    print(f"Sunset  (local, decimal hours): {ss_dec:.4f}")

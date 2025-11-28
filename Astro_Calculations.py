import swisseph as swe

swe.set_ephe_path('ephe')
swe.set_sid_mode(swe.SIDM_TRUE_CITRA)

#correction=(45-44)/60+(12.28-53.63)/3600

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

from Data_Types import Planet, chart_details,Horror_scope
from Convert import jhd_file_to_chart_details, ast_file_to_chart_details, save_as_ast, read_ast


def get_asc(chart: chart_details):
    #swe.set_sid_mode(swe.SIDM_TRUE_CITRA)  # Lahiri Ayanamsa
    #print(chart.time_in_decimal()+chart.timezone)
    jd_ut = swe.julday(chart.year, chart.month, chart.date, chart.time_in_decimal()+chart.timezone)  
    jd_next=swe.julday(chart.year, chart.month, chart.date, chart.time_in_decimal()+chart.timezone+1)
    next_asc = swe.houses_ex(jd_next, chart.latitude, chart.longitude,b'P',   swe.FLG_SWIEPH| swe.FLG_TRUEPOS|swe.FLG_SIDEREAL)[0][0]
    longitude = chart.longitude
    latitude = chart.latitude
    #print(longitude, latitude)
    asc = swe.houses_ex(jd_ut, latitude, longitude,b'P',   swe.FLG_SWIEPH| swe.FLG_TRUEPOS|swe.FLG_SIDEREAL)[0][0]
    speed = (next_asc - asc)*24
    asc_position = Planet.make("Ascendant", asc, speed)
    return asc_position

def get_planet(chart: chart_details, planet: str):
    is_ketu = (planet == "Ketu")
    planet_key = "Rahu" if is_ketu else planet

    jd_ut = swe.julday(
        chart.year,
        chart.month,
        chart.date,
        chart.hour + chart.minute / 60 + chart.second / 3600 + chart.timezone
    )
    #swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
    swe.set_topo(chart.longitude, chart.latitude, chart.altidude)
    planet_id = PLANETS[planet_key]
    planet_info = swe.calc_ut(jd_ut, planet_id, swe.FLG_SWIEPH| swe.FLG_TRUEPOS|swe.FLG_SIDEREAL| swe.FLG_TRUEPOS)
    curr_long = planet_info[0][0] #+ correction

    if is_ketu:
        curr_long = (curr_long + 180) % 360  

    next_info = swe.calc_ut(jd_ut + 1/86400, planet_id, swe.FLG_SWIEPH| swe.FLG_TRUEPOS|swe.FLG_SIDEREAL| swe.FLG_TRUEPOS)
    next_long = next_info[0][0]
    if is_ketu:
        next_long = (next_long + 180) % 360

    # --- Correct speed calculation ---
    diff = next_long - curr_long
    speed = diff * 86400

    planet_obj = Planet.make(planet, curr_long, speed)
    return planet_obj



def make_horoscope(chart: chart_details):
    jd_ut = swe.julday(
        chart.year,
        chart.month,
        chart.date,
        chart.hour + chart.minute / 60 + chart.second / 3600 + chart.timezone
    )
    wi=swe.day_of_week(jd_ut)
    weekday_list=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    weekday=weekday_list[(wi+1)]
    horoscope_obj = Horror_scope(
        ascendant=get_asc(chart),
        natal_chart=chart,
        Sun=get_planet(chart, "Sun"),
        Moon=get_planet(chart, "Moon"),
        Mercury=get_planet(chart, "Mercury"),
        Venus=get_planet(chart, "Venus"),
        Mars=get_planet(chart, "Mars"),
        Jupiter=get_planet(chart, "Jupiter"),
        Saturn=get_planet(chart, "Saturn"),
        Rahu=get_planet(chart, "Rahu"),
        Ketu=get_planet(chart, "Ketu"),
        weekday=weekday,
        date=chart.date,
        month=chart.month,
        year=chart.year,
        hour=chart.hour,
        minute=chart.minute,
        second=chart.second,
        longitude=chart.longitude,
        latitude=chart.latitude,
    )
    return horoscope_obj





from Draw_chart import * 


if __name__ == "__main__":
    chart = read_ast("a.ast")
    chart.print_details()
    nat_chart=make_horoscope(chart)
    nat_chart.print_horoscope()
    start_chart_menu(nat_chart)    

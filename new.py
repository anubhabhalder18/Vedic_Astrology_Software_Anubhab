import swisseph as swe
swe.set_ephe_path('ephe')


swe.set_sid_mode(swe.SIDM_TRUE_CITRA)  # Lahiri Ayanamsa

jd_ut = swe.julday(2004, 3, 18, 22+4/60+44/3600-5.5)  # Example: Jan 1, 2000 at 12:00 UTC




longitude = 88+22/60
latitude = 22+34/60

asc = swe.houses_ex(jd_ut, latitude, longitude,b'P',   swe.FLG_SIDEREAL)[0][0]

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



print(f"Ascendant: {asc}")

for planet_name, planet_id in PLANETS.items():
    planet_info = swe.calc_ut(jd_ut, planet_id, swe.FLG_SIDEREAL)
    planet_longitude = planet_info[0][0]
    print(f"{planet_name}: {planet_longitude:.16f}°")

weekday = swe.day_of_week(jd_ut+1)
weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
print(f"Day of the week: {weekday_names[weekday]}")  


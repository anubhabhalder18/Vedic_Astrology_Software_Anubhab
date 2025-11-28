from dataclasses import dataclass
import math

rashis=[
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
    ]
nakshatras=[
            "Ashwini",
            "Bharani",
            "Krittika",
            "Rohini",
            "Mrigashira",
            "Ardra",
            "Punarvasu",
            "Pushya",
            "Ashlesha",
            "Magha",
            "Purva Phalguni",
            "Uttara Phalguni",
            "Hasta",
            "Chitra",
            "Swati",
            "Vishakha",
            "Anuradha",
            "Jyeshtha",
            "Mula",
            "Purva Ashadha",
            "Uttara Ashadha",
            "Shravana",
            "Dhanishta",
            "Shatabhisha",
            "Purva Bhadrapada",
            "Uttara Bhadrapada",
            "Revati"
        ]
nak_len=13+1/3

@dataclass
class chart_details:
    name:str
    date:int
    month:int
    year:int
    hour:int
    minute:int
    second:float
    longitude:float
    latitude:float
    timezone:float
    altidude:float=0.0

    
    def print_details(self):
        print(f"Name: {self.name}")
        print(f"Date: {self.date}-{self.month}-{self.year}")
        print(f"Time: {self.hour}:{self.minute}:{self.second:.2f}")
        print(f"longitude: {self.longitude}")
        print(f"Latitude: {self.latitude}")
        print(f"Timezone: {self.timezone} hours")
        print(f"Altitude: {self.altidude} meters")
    def time_in_decimal(self):
        return self.hour + self.minute / 60 + self.second / 3600
    
@dataclass
class position:
    longitude:float
    rashi:str
    degree:int
    minute:int
    second:float
    nakshatra:str
    nakshatra_index:int
    nak_portion:float
    pada:int
    def make(x):
        longitude=x%360
        rashi_index=int(longitude//30)
        rashi=rashis[rashi_index%12]
        degree_in_rashi=int(longitude%30)
        minute_in_rashi=int((longitude*60)%60)
        second_in_rashi=(longitude*3600)%60
        nak_number=longitude/nak_len
        nakshatra_index=(math.ceil(nak_number)-1)%27
        nak_portion_deg=longitude - (nakshatra_index)*nak_len
        nak_portion=(nak_portion_deg/nak_len)*100
        nakshatra=nakshatras[nakshatra_index]
        if nak_portion<25:
            pada=1
        elif nak_portion<50:
            pada=2
        elif nak_portion<75:
            pada=3
        else:
            pada=4
        return position(
            longitude=longitude,
            rashi=rashi,
            degree=degree_in_rashi,
            minute=minute_in_rashi,
            second=second_in_rashi,
            nakshatra=nakshatra,
            nakshatra_index=nakshatra_index+1,
            nak_portion=nak_portion,
            pada=pada
        )
    def print_position(self):
        print(f"Longitude: {self.longitude:.6f}°")
        print(f"Rashi: {self.rashi}")
        print(f"Degree: {self.degree}° {self.minute}' {self.second:.2f}''")
        print(f"Nakshatra: {self.nakshatra} (Index: {self.nakshatra_index})")
        print(f"Nakshatra Portion: {self.nak_portion:.2f}%")
        print(f"Pada: {self.pada}")


@dataclass
class Planet:
    name:str
    planet_position:position
    speed:float
    def make(name, longitude, speed):
        return Planet(
            name=name,
            planet_position=position.make(longitude),
            speed=speed
        )
    def print_planet(self):
        print(f"Planet Name: {self.name}")
        self.planet_position.print_position()
        print(f"Speed: {self.speed:.6f}°/day")
    
@dataclass
class Horror_scope:
    ascendant:position
    natal_chart:chart_details
    Sun:Planet
    Moon:Planet
    Mercury:Planet
    Venus:Planet
    Mars:Planet
    Jupiter:Planet
    Saturn:Planet
    Rahu:Planet
    Ketu:Planet
    weekday:str
    

    def print_horoscope(self):
        print("Horoscope Details:")
        print("Ascendant:")
        self.ascendant.print_planet()
        print("\nPlanets:")
        for planet in [self.Sun, self.Moon, self.Mercury, self.Venus, self.Mars, self.Jupiter, self.Saturn, self.Rahu, self.Ketu]:
            planet.print_planet()
            print("")
        print(f"Weekday: {self.weekday}")



if __name__ == "__main__":
    pos=position.make(306.753)
    pos.print_position()

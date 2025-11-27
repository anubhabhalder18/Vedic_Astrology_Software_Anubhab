from dataclasses import dataclass

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


@dataclass
class chart_details:
    name:str
    date:int
    month:int
    year:int
    hour:int
    minute:int
    second:float
    longitude_deg:float
    longitude_min:float
    longitude_sec:float
    latitude_deg:float
    latitude_min:float
    latitude_sec:float
    timezone:float

    
    def make(array):
        return chart_details(
            name=array[0],
            date=int(array[1]),
            month=int(array[2]),
            year=int(array[3]),
            longitude_deg=float(array[4]),
            longitude_min=float(array[5]),
            latitude_deg=float(array[6]),
            latitude_min=float(array[7]),
            latitude_sec=float(array[8]),
            timezone=float(array[9]),
        )
    def print_details(self):
        print(f"Name: {self.name}")
        print(f"Date: {self.date}-{self.month}-{self.year}")
        print(f"Time: {self.hour}:{self.minute}:{self.second:.2f}")
        print(f"Longitude: {self.longitude_deg}° {self.longitude_min}' {self.longitude_sec}''")
        print(f"Latitude: {self.latitude_deg}° {self.latitude_min}' {self.latitude_sec}''")
        print(f"Timezone: {self.timezone} hours")
    def time_in_decimal(self):
        return self.hour + self.minute / 60 + self.second / 3600
    def longitude_in_decimal(self):
        return self.longitude_deg + self.longitude_min / 60 + self.longitude_sec / 3600
    def latitude_in_decimal(self):
        return self.latitude_deg + self.latitude_min / 60 + self.latitude_sec / 3600

@dataclass
class position:
    longitude:float
    rashi:str
    degree_in_rashi:int
    minute_in_rashi:int
    second_in_rashi:float
    nakshatra:str
    nakshatra_index:int
    pada:int
    def make(longitude):
        rashi_index=int(longitude//30)
        rashi=rashis[rashi_index]
        degree_in_rashi=int(longitude%30)
        minute_in_rashi=int((longitude*60)%60)
        second_in_rashi=(longitude*3600)%60
        nakshatra_index=int((longitude%30)//(13+1/3))
        nakshatra=nakshatras[nakshatra_index]
        pada=int(((longitude%30)%(13+1/3))//(13+1/3)/4*4)+1
        return position(
            longitude=longitude,
            rashi=rashi,
            degree_in_rashi=degree_in_rashi,
            minute_in_rashi=minute_in_rashi,
            second_in_rashi=second_in_rashi,
            nakshatra=nakshatra,
            nakshatra_index=nakshatra_index,
            pada=pada
        )


@dataclass
class planet:
    name:str
    planet_position:position
    speed:float
    def make(name, longitude, speed):
        return planet(
            name=name,
            planet_position=position.make(longitude),
            speed=speed
        )


from dataclasses import dataclass


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
    timezone_hour:float
    timezone_min:float
    
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
            timezone_hour=float(array[9]),
            timezone_min=float(array[10])
        )
    def print_details(self):
        print(f"Name: {self.name}")
        print(f"Date: {self.date}-{self.month}-{self.year}")
        print(f"Time: {self.hour}:{self.minute}:{self.second}")
        print(f"Longitude: {self.longitude_deg}° {self.longitude_min}' {self.longitude_sec}''")
        print(f"Latitude: {self.latitude_deg}° {self.latitude_min}' {self.latitude_sec}''")
        print(f"Timezone: {self.timezone_hour} hours {self.timezone_min} minutes")
    def time_in_decimal(self):
        return self.hour + self.minute / 60 + self.second / 3600
    def longitude_in_decimal(self):
        return self.longitude_deg + self.longitude_min / 60 + self.longitude_sec / 3600
    def latitude_in_decimal(self):
        return self.latitude_deg + self.latitude_min / 60 + self.latitude_sec / 3600

import os
from Data_Types import chart_details

def jhd_to_text(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    name=filename.split('.')[0]
    with open(path, 'r') as f:
        return name+'\n'+f.read()

def text_to_chart_details(text):
    lines = text.strip().split('\n')

    date=int(lines[1])
    month=int(lines[2])
    year=int(lines[3])
    time=float(lines[4])
    time_zone=float(lines[5])
    longitude=float(lines[6])
    latitude=float(lines[7])
    time_hour=time//1
    time_min=((time - time_hour)*60)//1
    time_sec=((((time - time_hour)*60)-time_min)*60)
    longitude_deg=longitude//1
    longitude_min=((longitude - longitude_deg)*60)//1
    longitude_sec=((((longitude - longitude_deg)*60)-longitude_min)*60)
    latitude_deg=latitude//1
    latitude_min=((latitude - latitude_deg)*60)//1
    latitude_sec=((((latitude - latitude_deg)*60)-latitude_min)*60)
    chart=chart_details(
        name=lines[0],
        date=int(date),
        month=int(month),
        year=int(year),
        hour=int(time_hour),
        minute=int(time_min),
        second=float(time_sec),
        longitude_deg=float(longitude_deg),
        longitude_min=float(longitude_min),
        longitude_sec=float(longitude_sec),
        latitude_deg=float(latitude_deg),
        latitude_min=float(latitude_min),
        latitude_sec=float(latitude_sec),
        timezone_hour=float(time_hour),
        timezone_min=float(time_min)
    )
    return chart

def jhd_file_to_chart_details(filename):
    text=jhd_to_text(filename)
    chart=text_to_chart_details(text)
    return chart

if __name__ == "__main__":
    chart=jhd_file_to_chart_details('a.jhd')
    chart.print_details()


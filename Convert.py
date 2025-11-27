import os
from Data_Types import chart_details

def get_time(t:str):
    west=1
    if(t[0]=='-'):
        west=-1
        t=t[1:]

    t=float(t)
    hours=int(t//1)
    minutes=(t-hours)*100
    minutes_int=int(minutes//1)
    seconds=(minutes-minutes_int)*100
    return (hours + minutes_int / 60 + seconds / 3600)*west




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
    time=get_time(lines[4])
    time_zone=get_time(lines[5])
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
        timezone=float(time_zone),
    )
    return chart

def jhd_file_to_chart_details(filename):
    text=jhd_to_text(filename)
    chart=text_to_chart_details(text)
    return chart

def save_as_ast(chart:chart_details, filename:str):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'w') as f:
        f.write(f"{chart.name}\n")
        f.write(f"{chart.date}-{chart.month}-{chart.year}\n")
        f.write(f"{chart.hour}:{chart.minute}:{chart.second}\n")
        f.write(f"{chart.longitude_deg} {chart.longitude_min} {chart.longitude_sec}\n")
        f.write(f"{chart.latitude_deg} {chart.latitude_min} {chart.latitude_sec}\n")
        f.write(f"Timezone:{chart.timezone}\n")
def read_ast(filename:str):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        lines = f.readlines()
        name = lines[0].strip()
        date_parts = lines[1].strip().split('-')
        date = int(date_parts[0])
        month = int(date_parts[1])
        year = int(date_parts[2])
        time_parts = lines[2].strip().split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = float(time_parts[2])
        longitude_parts = lines[3].strip().split(' ')
        longitude_deg = float(longitude_parts[0])
        longitude_min = float(longitude_parts[1])
        longitude_sec = float(longitude_parts[2])
        latitude_parts = lines[4].strip().split(' ')
        latitude_deg = float(latitude_parts[0])
        latitude_min = float(latitude_parts[1])
        latitude_sec = float(latitude_parts[2])
        timezone=float(lines[5].strip().split(':')[1])
        
        chart=chart_details(
            name=name,
            date=date,
            month=month,
            year=year,
            hour=hour,
            minute=minute,
            second=second,
            longitude_deg=longitude_deg,
            longitude_min=longitude_min,
            longitude_sec=longitude_sec,
            latitude_deg=latitude_deg,
            latitude_min=latitude_min,
            latitude_sec=latitude_sec,
            timezone=timezone,
        )
        return chart

def ast_file_to_chart_details(filename:str):
    chart=read_ast(filename)
    return chart  
if __name__ == "__main__":
    chart=jhd_file_to_chart_details('a.jhd')
    chart.print_details()
    save_as_ast(chart, 'a.ast')
    chart2=ast_file_to_chart_details('a.ast')
    chart2.print_details()


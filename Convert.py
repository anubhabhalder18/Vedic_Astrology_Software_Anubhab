import os
from Data_Types import chart_details

def get_time(t: str):
    
    t = t + "0000000"
    west = 1

    if t[0] == "-":
        west = -1
        t = t[1:]

    if "." in t:
        hours_str, rest = t.split(".", 1)
    else:   
        hours_str, rest = t, ""

    hours = int(hours_str)

    minutes = int(rest[0:2]) if len(rest) >= 2 else 0
    sec_whole = int(rest[2:4]) if len(rest) >= 4 else 0
    sec_frac = float("0." + rest[4:]) if len(rest) >= 5 else 0.0

    seconds = sec_whole + sec_frac


    return (hours + minutes / 60 + seconds / 3600) * west

def get_deg(lat_str: str):
    lat_str = lat_str + "0000000"
    north = 1

    if lat_str[0] == "-":
        north = -1
        lat_str = lat_str[1:]

    if "." in lat_str:
        degrees_str, rest = lat_str.split(".", 1)
    else:   
        degrees_str, rest = lat_str, ""

    degrees = int(degrees_str)

    minutes = int(rest[0:2]) if len(rest) >= 2 else 0
    sec_whole = int(rest[2:4]) if len(rest) >= 4 else 0
    sec_frac = float("0." + rest[4:]) if len(rest) >= 5 else 0.0

    seconds = sec_whole + sec_frac


    return (degrees + minutes / 60 + seconds / 3600) * north




def jhd_to_text(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    name=filename.split('.')[0]
    with open(path, 'r') as f:
        return name+'\n'+f.read()

def text_to_chart_details(text):
    lines = text.strip().split('\n')

    month=int(lines[1])
    date=int(lines[2])
    year=int(lines[3])
    time=get_time(lines[4])
    time_zone=get_time(lines[5])
    longitude=get_deg(lines[6])
    latitude=get_deg(lines[7])
    time_hour=time//1
    time_min=((time - time_hour)*60)//1
    time_sec=((((time - time_hour)*60)-time_min)*60)
    chart=chart_details(
        name=lines[0],
        date=int(date),
        month=int(month),
        year=int(year),
        hour=int(time_hour),
        minute=int(time_min),
        second=float(time_sec),
        longitude=float(longitude),
        latitude=float(latitude),
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
        f.write(f"longitude:{chart.longitude}\n")
        f.write(f"latitude:{chart.latitude}\n")
        f.write(f"Timezone:{chart.timezone}\n")
        f.write(f"Altitude:{chart.altidude}\n")
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
        longtidude=lines[3].strip().split(':')[1]
        latitude=lines[4].strip().split(':')[1]
        timezone=float(lines[5].strip().split(':')[1])
        altude=float(lines[6].strip().split(':')[1])

        
        chart=chart_details(
            name=name,
            date=date,
            month=month,
            year=year,
            hour=hour,
            minute=minute,
            second=second,
            longitude=float(longtidude),
            latitude=float(latitude),
            timezone=timezone,
            altidude=altude
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
    


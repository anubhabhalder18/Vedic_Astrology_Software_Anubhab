import tkinter as tk
from math import cos, sin, radians
import tkinter as tk
from math import cos, sin, radians
import tkinter as tk
from math import cos, sin, radians

import tkinter as tk
import tkinter as tk
import tkinter as tk

def draw_fixed_rashi_chart(horoscope, size=750):
    """
    Draw a fixed-Rashi North Indian chart.
    Only prints Ascendant and planets (no rashi names).
    With triangle-aware alignment (Leo/Scorpio left, Virgo/Sagittarius right).
    """

    # ---- rashi index from longitude ----
    def sign_index(body):
        lon = body.planet_position.longitude % 360
        return int(lon // 30)

    PLANET_LABELS = {
        "Sun": "Su", "Moon": "Mo", "Mercury": "Me", "Venus": "Ve",
        "Mars": "Ma", "Jupiter": "Ju", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"
    }

    # ---- collect contents per rashi ----
    rashi_contents = {i: [] for i in range(12)}
    asc = sign_index(horoscope.ascendant)
    rashi_contents[asc].append("As")
    for pname, short in PLANET_LABELS.items():
        pobj = getattr(horoscope, pname)
        r = sign_index(pobj)
        rashi_contents[r].append(short)

    # ---- Tkinter ----
    win = tk.Toplevel()
    win.title("Fixed-Rashi North Indian Chart")
    canvas = tk.Canvas(win, width=size, height=size, bg="white")
    canvas.pack()

    cell = size / 3

    # ---- grid ----
    for i in range(4):
        canvas.create_line(0, i * cell, size, i * cell, width=2)
        canvas.create_line(i * cell, 0, i * cell, size, width=2)

    # ---- corner diagonals ----
    canvas.create_line(0, 0, cell, cell, width=2)
    canvas.create_line(size, 0, 2 * cell, cell, width=2)
    canvas.create_line(0, size, cell, 2 * cell, width=2)
    canvas.create_line(size, size, 2 * cell, 2 * cell, width=2)

    # ---- rashi centers (unchanged) ----
    def rc(xf, yf): return xf * cell, yf * cell

    rashi_center = {
        0:  rc(1.5, 0.50),  # Aries
        1:  rc(0.78, 0.38), # Taurus
        2:  rc(0.38, 0.85), # Gemini
        3:  rc(0.50, 1.50), # Cancer
        4:  rc(0.72, 2.16), # Leo ✔ tuned
        5:  rc(0.34, 2.86), # Virgo ✔ tuned
        6:  rc(1.50, 2.50), # Libra
        7:  rc(2.72, 2.89), # Scorpio ✔ tuned
        8:  rc(2.28, 2.20), # Sagittarius ✔ tuned
        9:  rc(2.50, 1.50), # Capricorn
        10: rc(2.75, 0.75), # Aquarius
        11: rc(2.26, 0.30), # Pisces
    }

    # ---- alignment override by rashi index ----
    LEFT_ALIGN  = {4, 7}      # Leo & Scorpio
    RIGHT_ALIGN = {5, 8}      # Virgo & Sagittarius
    # all others = center alignment

    # ---- draw planets ----
    for rashi in range(12):
        cx, cy = rashi_center[rashi]
        items = rashi_contents[rashi]
        if not items:
            continue

        rows = [items[i:i+2] for i in range(0, len(items), 2)]
        start_y = cy - (len(rows) - 1) * 11

        # alignment offset logic
        for idx, row in enumerate(rows):
            line = " ".join(row)

            if rashi in LEFT_ALIGN:
                # push near left boundary of triangle
                x = cx - (cell * 0.23)
                anchor = "w"  # left-justified
            elif rashi in RIGHT_ALIGN:
                # push near right boundary of triangle
                x = cx + (cell * 0.23)
                anchor = "e"  # right-justified
            else:
                # centered houses
                x = cx
                anchor = "center"

            canvas.create_text(
                x,
                start_y + idx * 22,
                text=line,
                font=("Arial", 15, "bold"),
                fill="black",
                anchor=anchor
            )

    return win

import tkinter as tk

def start_chart_menu(horoscope):
    """
    Main Tkinter window with menu to open North Indian chart correctly
    without blank/black screen.
    """

    root = tk.Tk()
    root.title("Astrology Toolkit")
    root.geometry("520x260")
    root.configure(bg="white")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    chart_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Charts", menu=chart_menu)

    # charts --------
    def open_north_chart():
        # deferred call ensures canvas is drawn properly (prevents black window)
        root.after(10, lambda: draw_fixed_rashi_chart(horoscope))

    chart_menu.add_command(label="North Indian Chart", command=open_north_chart)

    # Exit --------
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)

    label = tk.Label(
        root,
        text="Select  Charts → North Indian Chart",
        font=("Arial", 15, "bold"),
        bg="white"
    )
    label.pack(expand=True)

    root.mainloop()

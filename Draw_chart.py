import tkinter as tk
from math import cos, sin, radians
import tkinter as tk
from math import cos, sin, radians
import tkinter as tk
from math import cos, sin, radians

import tkinter as tk
import tkinter as tk
import tkinter as tk
import tkinter as tk

RASHI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
import tkinter as tk

RASHI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def draw_fixed_rashi_chart(horoscope, size=250, Badhaka=[1,10]):
    """
    Draw fixed-rashi North Indian chart.
    Badhaka = list of rashi indexes or rashi names → those areas painted orange.
    """

    # ---- convert Badhaka to indexes ----
    badhaka_index = set()
    if Badhaka:
        for b in Badhaka:
            if isinstance(b, int):
                badhaka_index.add(b % 12)
            elif isinstance(b, str) and b in RASHI_NAMES:
                badhaka_index.add(RASHI_NAMES.index(b))

    # ---- rashi index from longitude ----
    def sign_index(body):
        return int((body.planet_position.longitude % 360) // 30)

    PLANET_LABELS = {
        "Sun": "Su", "Moon": "Mo", "Mercury": "Me", "Venus": "Ve",
        "Mars": "Ma", "Jupiter": "Ju", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"
    }

    rashi_contents = {i: [] for i in range(12)}
    asc = sign_index(horoscope.ascendant)
    rashi_contents[asc].append("As")
    for pname, short in PLANET_LABELS.items():
        rashi_contents[sign_index(getattr(horoscope, pname))].append(short)

    win = tk.Toplevel()
    canvas = tk.Canvas(win, width=size, height=size, bg="white")
    canvas.pack()
    cell = size / 3

    # ---- rashi → exact triangle or rectangle shape ----
    # each entry stores (col, row, type, triangle-type if needed)
    # type: "rect" or "tri"
    SHAPES = {
        0:  (1, 0, "rect", None),     # Aries
        1:  (0, 0, "tri", "UR"),      # Taurus
        2:  (0, 0, "tri", "LL"),      # Gemini
        3:  (0, 1, "rect", None),     # Cancer
        4:  (0, 2, "tri", "UR"),      # Leo
        5:  (0, 2, "tri", "LL"),      # Virgo
        6:  (1, 2, "rect", None),     # Libra
        7:  (2, 2, "tri", "LR"),      # Scorpio
        8:  (2, 2, "tri", "UL"),      # Sagittarius
        9:  (2, 1, "rect", None),     # Capricorn
        10: (2, 0, "tri", "LR"),      # Aquarius
        11: (2, 0, "tri", "UL"),      # Pisces
    }

    # ---- paint Badhaka (triangle-aware) ----
    for rashi in badhaka_index:
        col, row, typ, tri = SHAPES[rashi]
        x0, y0 = col * cell, row * cell

        if typ == "rect":
            canvas.create_rectangle(x0, y0, x0 + cell, y0 + cell,
                                    fill="orange", width=0)
        else:
            # triangle fill
            if tri == "UR":      # upper right
                pts = [x0, y0, x0 + cell, y0, x0 + cell, y0 + cell]
            elif tri == "LL":    # lower left
                pts = [x0, y0 + cell, x0, y0, x0 + cell, y0 + cell]
            elif tri == "LR":    # lower right
                pts = [x0 + cell, y0 + cell, x0 + cell, y0, x0, y0 + cell]
            elif tri == "UL":    # upper left
                pts = [x0, y0, x0 + cell, y0, x0, y0 + cell]

            canvas.create_polygon(pts, fill="orange", outline="", width=0)

    # ---- draw grid & diagonals ----
    for i in range(4):
        canvas.create_line(0, i * cell, size, i * cell, width=2)
        canvas.create_line(i * cell, 0, i * cell, size, width=2)

    canvas.create_line(0, 0, cell, cell, width=2)
    canvas.create_line(size, 0, 2*cell, cell, width=2)
    canvas.create_line(0, size, cell, 2*cell, width=2)
    canvas.create_line(size, size, 2*cell, 2*cell, width=2)

    # ---- center locations (unchanged) ----
    def rc(xf, yf): return xf * cell, yf * cell
    rashi_center = {
        0: rc(1.5, 0.50), 1: rc(0.78, 0.38), 2: rc(0.38, 0.85),
        3: rc(0.50, 1.50), 4: rc(0.72, 2.16), 5: rc(0.34, 2.86),
        6: rc(1.50, 2.50), 7: rc(2.72, 2.89), 8: rc(2.28, 2.20),
        9: rc(2.50, 1.50), 10: rc(2.75, 0.75), 11: rc(2.26, 0.30),
    }

    # ---- alignment rules ----
    LEFT_ALIGN  = {4, 7}   # Leo, Scorpio
    RIGHT_ALIGN = {5, 8}   # Virgo, Sagittarius

    # ---- draw planets / Asc ----
    for rashi in range(12):
        cx, cy = rashi_center[rashi]
        items = rashi_contents[rashi]
        if not items:
            continue

        rows = [items[i:i+2] for i in range(0, len(items), 2)]
        start_y = cy - (len(rows) - 1) * 11

        for idx, row in enumerate(rows):
            msg = " ".join(row)
            if rashi in LEFT_ALIGN:
                x, anchor = cx - (cell * 0.23), "w"
            elif rashi in RIGHT_ALIGN:
                x, anchor = cx + (cell * 0.23), "e"
            else:
                x, anchor = cx, "center"

            canvas.create_text(
                x,
                start_y + idx * 22,
                text=msg,
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
    def open_east_chart():
        # deferred call ensures canvas is drawn properly (prevents black window)
        root.after(10, lambda: draw_fixed_rashi_chart(horoscope))

    chart_menu.add_command(label="East Indian Chart", command=open_east_chart)

    # Exit --------
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)

    label = tk.Label(
        root,
        text="Select  Charts → East Indian Chart",
        font=("Arial", 15, "bold"),
        bg="white"
    )
    label.pack(expand=True)

    root.mainloop()

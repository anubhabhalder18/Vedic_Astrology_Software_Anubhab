import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta

from Data_Types import chart_details, Planet, Horror_scope, position
from Astro_Calculations import make_horoscope
from divisional_charts import make_navamsa_horoscope, make_d81_horoscope, make_drekkana_horoscope

# ------------------------------------------------
# GLOBAL HOROSCOPE (always current chart in use)
# ------------------------------------------------
horoscope: Horror_scope | None = None

# ------------------------------------------------
# CONSTANTS FOR NAKSHATRA / DASHA
# ------------------------------------------------
rashis = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

nakshatras = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
    "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada",
    "Uttara Bhadrapada","Revati"
]

nak_len = 13 + 1/3

# 27 Nakshatras in exact order
NAKSHATRA_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Vimshottari Dasha Lords in sequence
VIMSHOTTARI_ORDER = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury"
]

# Map each Nakshatra → Dasha lord
NAK_LORDS = (VIMSHOTTARI_ORDER * 3)[:27]

# Years of each Mahadasha
DASHA_YEARS = {
    "Ketu": 7,# change to 7
    "Venus": 20,# change to 20
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

NAK_LEN = 360.0 / 27.0


# ------------------------------------------------
# DRAW FIXED NORTH INDIAN CHART
# ------------------------------------------------
def draw_fixed_rashi_chart(h: Horror_scope, size=600, canvas_override=None):
    # canvas override system
    if canvas_override is not None:
        canvas = canvas_override
    else:
        win = tk.Toplevel()
        canvas = tk.Canvas(win, width=size, height=size, bg="white")
        canvas.pack()

    cell = size / 3

    SH = {
        0:(1,0,"rect",None), 1:(0,0,"tri","UR"), 2:(0,0,"tri","LL"), 3:(0,1,"rect",None),
        4:(0,2,"tri","UR"), 5:(0,2,"tri","LL"), 6:(1,2,"rect",None), 7:(2,2,"tri","LR"),
        8:(2,2,"tri","UL"), 9:(2,1,"rect",None),10:(2,0,"tri","LR"),11:(2,0,"tri","UL")
    }

    def sign_index(obj):
        lon = obj.planet_position.longitude if hasattr(obj, "planet_position") else obj.longitude
        return int(lon % 360 // 30)

    labels = {
        "Sun":"Su","Moon":"Mo","Mercury":"Me","Venus":"Ve","Mars":"Ma",
        "Jupiter":"Ju","Saturn":"Sa","Rahu":"Ra","Ketu":"Ke"
    }

    rc = {i: [] for i in range(12)}
    rc[sign_index(h.ascendant)].append("As")
    for p in labels:
        rc[sign_index(getattr(h, p))].append(labels[p])

    # grid lines
    for i in range(4):
        canvas.create_line(0, i * cell, size, i * cell, width=2)
        canvas.create_line(i * cell, 0, i * cell, size, width=2)
    canvas.create_line(0, 0, cell, cell, width=2)
    canvas.create_line(size, 0, 2 * cell, cell, width=2)
    canvas.create_line(0, size, cell, 2 * cell, width=2)
    canvas.create_line(size, size, 2 * cell, 2 * cell, width=2)

    tri_bounds = {
        "UR": lambda x0,y0,x1,y1:(x0+0.55*cell,y0+0.05*cell,x1-0.05*cell,y0+0.40*cell),
        "LL": lambda x0,y0,x1,y1:(x0+0.05*cell,y1-0.45*cell,x0+0.45*cell,y1-0.05*cell),
        "LR": lambda x0,y0,x1,y1:(x1-0.45*cell,y1-0.45*cell,x1-0.05*cell,y1-0.05*cell),
        "UL": lambda x0,y0,x1,y1:(x0+0.05*cell,y0+0.05*cell,x0+0.45*cell,y0+0.45*cell)
    }
    RECT_MARGIN = 0.10
    LEFT = {4, 7}
    RIGHT = {5, 8}

    for r in range(12):
        col, row, typ, tri = SH[r]
        items = rc[r]
        if not items:
            continue
        x0, y0 = col * cell, row * cell
        x1, y1 = x0 + cell, y0 + cell
        if typ == "rect":
            xmin = x0 + cell * RECT_MARGIN
            ymin = y0 + cell * RECT_MARGIN
            xmax = x1 - cell * RECT_MARGIN
            ymax = y1 - cell * RECT_MARGIN
        else:
            xmin, ymin, xmax, ymax = tri_bounds[tri](x0, y0, x1, y1)

        n = len(items)
        avail = ymax - ymin
        fontsize = int((avail / (n + 0.8)) * 0.55)
        fontsize = max(10, min(fontsize, int(size * 0.07)))
        step = avail / (n + 0.8)
        for i, lbl in enumerate(items):
            yy = ymin + (i + 0.55) * step
            xx = (xmin + xmax) / 2
            anch = "center"
            if r in LEFT:
                xx = xmin; anch = "w"
            if r in RIGHT:
                xx = xmax; anch = "e"
            canvas.create_text(xx, yy, text=lbl, font=("Arial", fontsize, "bold"), anchor=anch)

    def details(event=None):
        win = tk.Toplevel()
        win.title("Chart Details")
        win.geometry("620x350")
        cols = ("Body", "Rashi-Deg-Min", "Nakshatra-Pada", "Speed")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140, anchor="center")
        tree.pack(fill="both", expand=True)

        asc_pos = h.ascendant.planet_position
        tree.insert("", "end", values=(
            "Asc",
            f"{asc_pos.rashi} {asc_pos.degree}°{asc_pos.minute}'",
            f"{asc_pos.nakshatra} (Pada {asc_pos.pada})",
            ""
        ))

        order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
        for p in order:
            pl = getattr(h, p)
            pos = pl.planet_position
            tree.insert("", "end", values=(
                p,
                f"{pos.rashi} {pos.degree}°{pos.minute}'",
                f"{pos.nakshatra} (Pada {pos.pada})",
                f"{pl.speed:.3f}"
            ))

    canvas.bind("<Button-1>", details)


# ------------------------------------------------
# SAVE / LOAD .AST CHARTS
# ------------------------------------------------
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


def save_ast(h: Horror_scope):
    file = filedialog.asksaveasfilename(
        initialdir=DATA_FOLDER,
        defaultextension=".ast",
        filetypes=[("AST", "*.ast")]
    )
    if not file:
        return
    nc = h.natal_chart
    with open(file, "w") as f:
        f.write(f"{nc.name}\n")
        f.write(f"{nc.date}-{nc.month}-{nc.year}\n")
        f.write(f"{nc.hour}:{nc.minute}:{nc.second}\n")
        f.write(f"longitude:{nc.longitude}\n")
        f.write(f"latitude:{nc.latitude}\n")
        f.write(f"Timezone:{nc.timezone}\n")
        f.write(f"Altitude:{nc.altidude}\n")
    messagebox.showinfo("Saved", "Chart exported.")


def load_ast() -> Horror_scope | None:
    global horoscope
    file = filedialog.askopenfilename(
        initialdir=DATA_FOLDER,
        filetypes=[("AST", "*.ast")]
    )
    if not file:
        return None
    with open(file) as f:
        lines = [x.strip() for x in f]
    nm = lines[0]
    d, m, y = map(int, lines[1].split("-"))
    h_, mi_, se_ = lines[2].split(":")
    h_ = int(h_)
    mi_ = int(mi_)
    se_ = float(se_)
    lon = float(lines[3].split(":")[1])
    lat = float(lines[4].split(":")[1])
    tz = float(lines[5].split(":")[1])
    alt = float(lines[6].split(":")[1])
    cd = chart_details(nm, d, m, y, h_, mi_, se_, lon, lat, tz, alt)
    horoscope = make_horoscope(cd)
    return horoscope


# ------------------------------------------------
# TRANSIT WINDOW
# ------------------------------------------------
def open_transit_tab(root, natal: Horror_scope):
    top = tk.Toplevel(root)
    top.title("Transit Chart")
    top.geometry("350x260")
    tk.Label(top, text="Enter Transit Date (DD-MM-YYYY):", font=("Arial", 12, "bold")).pack(pady=5)

    ed = ttk.Entry(top)
    ed.insert(0, "18-03-2025")
    ed.pack()

    def open_chart():
        try:
            d, m, y = map(int, ed.get().split("-"))
        except Exception:
            messagebox.showerror("Err", "Date must be DD-MM-YYYY")
            return
        cd = natal.natal_chart
        trans_cd = chart_details(cd.name + " Transit", d, m, y,
                                 cd.hour, cd.minute, cd.second,
                                 cd.longitude, cd.latitude, cd.timezone, cd.altidude)
        H = make_horoscope(trans_cd)
        win = tk.Toplevel()
        win.title("Transit")
        c = tk.Canvas(win, width=690, height=690, bg="white")
        c.pack()
        draw_fixed_rashi_chart(H, size=690, canvas_override=c)

    tk.Button(top, text="Open Transit Chart", command=open_chart).pack(pady=8)


# ------------------------------------------------
# VIMSHOTTARI DASHA EXPLORER (USES CURRENT HOROSCOPE)
# ------------------------------------------------
def create_vimshottari_window(parent):
    global horoscope
    if horoscope is None:
        messagebox.showerror("No Chart", "No horoscope loaded.")
        return
    d1: Horror_scope = horoscope

    win = tk.Toplevel(parent)
    win.title("Vimshottari Dasha — Single Window Explorer")
    win.geometry("1100x700")

    # ─ Frames
    left_frame = ttk.Frame(win)
    left_frame.pack(side="left", fill="y")

    right_frame = ttk.Frame(win)
    right_frame.pack(side="right", fill="both", expand=True)

    # ─ Input
    input_frame = ttk.LabelFrame(right_frame, text="Input")
    input_frame.pack(fill="x", padx=8, pady=6)

    labels = ["Moon Sign (1-12)", "Moon Degree (0-30)", "Moon Minute",
              "Birth Day", "Birth Month", "Birth Year"]

    find_index = {
        "Aries":1,"Taurus":2,"Gemini":3,"Cancer":4,"Leo":5,"Virgo":6,
        "Libra":7,"Scorpio":8,"Sagittarius":9,"Capricorn":10,"Aquarius":11,"Pisces":12
    }

    moon_pos = d1.Moon.planet_position
    nc = d1.natal_chart
    defaults = [
        find_index[moon_pos.rashi],
        moon_pos.degree,
        moon_pos.minute,
        nc.date,
        nc.month,
        nc.year
    ]

    entries = []
    for i, (lab, default) in enumerate(zip(labels, defaults)):
        ttk.Label(input_frame, text=lab).grid(row=i // 3, column=(i % 3) * 2, padx=5, pady=4, sticky="e")
        e = ttk.Entry(input_frame, width=8)
        e.insert(0, str(default))
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=4, sticky="w")
        entries.append(e)

    entry_sign, entry_deg, entry_min, entry_day, entry_month, entry_year = entries

    # ─ Tree (left)
    tree_frame = ttk.Frame(left_frame)
    tree_frame.pack(fill="both", expand=True, padx=6, pady=6)

    tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.heading("#0", text="Mahadasha Tree", anchor="w")
    tree.pack(side="left", fill="y", expand=True)
    tree_scroll.config(command=tree.yview)
    tree_scroll.pack(side="right", fill="y")

    # ─ Details
    detail_frame = ttk.LabelFrame(right_frame, text="Selected Details")
    detail_frame.pack(fill="both", expand=True, padx=8, pady=6)

    detail_text = tk.Text(detail_frame, wrap="word")
    detail_scroll = ttk.Scrollbar(detail_frame, orient="vertical", command=detail_text.yview)
    detail_text.configure(yscrollcommand=detail_scroll.set)
    detail_text.pack(side="left", fill="both", expand=True)
    detail_scroll.pack(side="right", fill="y")

    # ─ Build button
    btn_build = ttk.Button(right_frame, text="Build Mahadasha Tree")
    btn_build.pack(pady=4)

    node_data = {}

    # ---- Core functions ----
    def get_nakshatra(sign, deg, mins):
        total = (sign - 1) * 30 + deg + mins / 60.0
        index = int(total // NAK_LEN)
        part = total - index * NAK_LEN
        return NAKSHATRA_LIST[index], NAK_LORDS[index], part

    def generate_dasha_sequence(start_lord):
        i = VIMSHOTTARI_ORDER.index(start_lord)
        return VIMSHOTTARI_ORDER[i:] + VIMSHOTTARI_ORDER[:i]

    def calculate_dasha_periods(start, lord_seq, years_dict):
        periods = []
        current = start
        for lord in lord_seq:
            yrs = years_dict[lord]
            end = current + timedelta(days=yrs * 365.25)
            periods.append((lord, current, end))
            current = end
        return periods

    def compute_antardasha(maha_lord, start, end):
        seq = generate_dasha_sequence(maha_lord)
        total_years = DASHA_YEARS[maha_lord]
        res = []
        current = start
        for lord in seq:
            proportion = DASHA_YEARS[lord] / 120.0
            span = total_years * proportion * 365.25
            e = current + timedelta(days=span)
            res.append((lord, current, e))
            current = e
        return res

    def compute_pratyantardasha(antar_lord, start, end):
        seq = generate_dasha_sequence(antar_lord)
        full_days = (end - start).total_seconds() / (24 * 3600)
        antar_total_years = full_days / 365.25
        res = []
        current = start
        for lord in seq:
            proportion = DASHA_YEARS[lord] / 120.0
            span = antar_total_years * proportion * 365.25
            e = current + timedelta(days=span)
            res.append((lord, current, e))
            current = e
        return res

    def compute_progression(start, end, deg0=0.0, parts=12):
        total_days = (end - start).total_seconds() / (24 * 3600)
        first = total_days * ((30.0 - deg0) / 30.0) / parts
        left = total_days - first
        step = left / (parts - 1) if parts > 1 else left
        res = []
        cur = start
        for i in range(parts):
            span = first if i == 0 else step
            e = cur + timedelta(days=span)
            res.append((f"Part {i + 1}", cur, e))
            cur = e
        return res

    # ---- Build Mahadasha tree ----
    def build_mahadasha_tree():
        try:
            sign = int(entry_sign.get())
            deg = float(entry_deg.get())
            mins = float(entry_min.get())
            d = int(entry_day.get())
            m = int(entry_month.get())
            y = int(entry_year.get())
        except Exception:
            messagebox.showerror("Error", "Invalid Moon / birth input.")
            return

        birth = datetime(y, m, d)
        nak, lord, nak_deg = get_nakshatra(sign, deg, mins)
        seq = generate_dasha_sequence(lord)

        elapsed_years = DASHA_YEARS[lord] * (nak_deg / NAK_LEN)
        start = birth - timedelta(days=elapsed_years * 365.25)

        mahadashas = calculate_dasha_periods(start, seq, DASHA_YEARS)

        for item in tree.get_children():
            tree.delete(item)
        node_data.clear()
        detail_text.delete("1.0", "end")
        detail_text.insert("end", f"Moon → {nak} (Lord {lord}) | Offset {nak_deg:.2f}°\n\n")

        for lord2, s, e in mahadashas:
            nid = tree.insert("", "end", text=f"{lord2}: {s:%Y-%m-%d} → {e:%Y-%m-%d}")
            node_data[nid] = {"type": "maha", "lord": lord2, "start": s, "end": e}
            tree.insert(nid, "end", text="(click to load antardashas)")

    # ---- Tree open ----
    def on_tree_open(event):
        item = tree.focus()
        data = node_data.get(item)
        if not data:
            return
        children = tree.get_children(item)
        if len(children) == 1 and "(click to load" in tree.item(children[0], "text"):
            tree.delete(children[0])
            if data["type"] == "maha":
                for lord, s, e in compute_antardasha(data["lord"], data["start"], data["end"]):
                    cid = tree.insert(item, "end", text=f"{lord}: {s:%Y-%m-%d} → {e:%Y-%m-%d}")
                    node_data[cid] = {"type": "antar", "lord": lord, "start": s, "end": e}
                    tree.insert(cid, "end", text="(click to load pratyantardashas)")
            elif data["type"] == "antar":
                for lord, s, e in compute_pratyantardasha(data["lord"], data["start"], data["end"]):
                    cid = tree.insert(item, "end", text=f"{lord}: {s:%Y-%m-%d} → {e:%Y-%m-%d}")
                    node_data[cid] = {"type": "praty", "lord": lord, "start": s, "end": e}

    # ---- Tree select ----
    def on_tree_select(event):
        item = tree.focus()
        data = node_data.get(item)
        detail_text.delete("1.0", "end")
        if not data:
            return
        detail_text.insert("end",
                           f"{data['type'].title()}\nLord: {data['lord']}\n"
                           f"Start: {data['start']}\nEnd:   {data['end']}\n\n"
                           f"Use Progression panel to subdivide this period.\n")

    # ---------- PROGRESSION PANEL -------------
    prog_frame = ttk.LabelFrame(right_frame, text="Progression Calculator")
    prog_frame.pack(fill="x", padx=8, pady=8)

    ttk.Label(prog_frame, text="Starting Degrees (0-30):").grid(row=0, column=0, padx=4, sticky="e")
    entry_prog_deg = ttk.Entry(prog_frame, width=8)
    entry_prog_deg.insert(0, "0")
    entry_prog_deg.grid(row=0, column=1, padx=4)

    ttk.Label(prog_frame, text="Parts:").grid(row=0, column=2, padx=4, sticky="e")
    entry_prog_parts = ttk.Entry(prog_frame, width=8)
    entry_prog_parts.insert(0, "12")
    entry_prog_parts.grid(row=0, column=3, padx=4)

    btn_progress = ttk.Button(prog_frame, text="Compute Progression")
    btn_progress.grid(row=0, column=4, padx=12)

    def run_progression():
        item = tree.focus()
        data = node_data.get(item)
        if not data:
            messagebox.showinfo("Error", "Select a Mahadasha / Antardasha / Pratyantardasha first")
            return
        try:
            deg0 = float(entry_prog_deg.get())
            parts = int(entry_prog_parts.get())
        except Exception:
            messagebox.showerror("Error", "Invalid progression input")
            return

        res = compute_progression(data["start"], data["end"], deg0, parts)
        detail_text.delete("1.0", "end")
        detail_text.insert("end", f"Progression of {data['lord']} ({data['type']})\n\n")
        for name, s, e in res:
            detail_text.insert("end", f"{name}: {s} → {e}\n")

    # ---- Bindings ----
    btn_build.config(command=build_mahadasha_tree)
    tree.bind("<<TreeviewOpen>>", on_tree_open)
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    btn_progress.config(command=run_progression)

    for idx, ent in enumerate(entries):
        def bind_next(i):
            def _next(e):
                if i + 1 < len(entries):
                    entries[i + 1].focus_set()
                else:
                    build_mahadasha_tree()
            return _next
        ent.bind("<Return>", bind_next(idx))

    build_mahadasha_tree()


from divisional_charts import *

# ------------------------------------------------
# MAIN UI
# ------------------------------------------------
def create_custom_dasha_window(parent):
    global horoscope
    if horoscope is None:
        messagebox.showerror("No Chart", "No horoscope loaded.")
        return
    d1: Horror_scope = horoscope

    win = tk.Toplevel(parent)
    win.title("Vimshottari Rajan dasa Explorer")
    win.geometry("1100x720")
    win.focus_set()

    # STANDARD VIMSHOTTARI
    VIM_STD_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars",
                     "Rahu", "Jupiter", "Saturn", "Mercury"]
    VIM_STD_YEARS = {
        "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
        "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
    }
    NAK_LORDS = (VIM_STD_ORDER * 3)[:27]
    NAK_LEN = 360 / 27.0

    # MOON FRACTION
    def moon_nak_fraction():
        lon = d1.Moon.planet_position.longitude % 360
        idx = int(lon // NAK_LEN)
        frac = (lon - idx * NAK_LEN) / NAK_LEN
        return NAK_LORDS[idx], frac

    # USER CONFIG
    cfg = ttk.LabelFrame(win, text="Dasha Configuration")
    cfg.pack(fill="x", padx=6, pady=5)

    ttk.Label(cfg, text="Order #").grid(row=0, column=0)
    ttk.Label(cfg, text="Planet").grid(row=0, column=1)
    ttk.Label(cfg, text="Years").grid(row=0, column=2)

    order_boxes = []
    year_boxes = []
    for i, lord in enumerate(VIM_STD_ORDER):
        ttk.Label(cfg, text=str(i + 1)).grid(row=i + 1, column=0, sticky="e")
        cb = ttk.Combobox(cfg, values=VIM_STD_ORDER, width=9, state="readonly")
        cb.set(lord)
        cb.grid(row=i + 1, column=1)
        order_boxes.append(cb)

        e = ttk.Entry(cfg, width=7)
        e.insert(0, str(VIM_STD_YEARS[lord]))
        e.grid(row=i + 1, column=2)
        year_boxes.append(e)

    def get_settings():
        order = [cb.get() for cb in order_boxes]
        years = {}
        for cb, ent in zip(order_boxes, year_boxes):
            lord = cb.get()
            try:
                years[lord] = float(ent.get())
            except:
                years[lord] = VIM_STD_YEARS[lord]
        return order, years

    # PANELS
    main = ttk.Frame(win)
    main.pack(fill="both", expand=True)

    left = ttk.Frame(main)
    left.pack(side="left", fill="both", expand=False)

    right = ttk.Frame(main)
    right.pack(side="right", fill="both", expand=True)

    tree_scroll = ttk.Scrollbar(left, orient="vertical")
    tree = ttk.Treeview(left, yscrollcommand=tree_scroll.set)
    tree.heading("#0", text="Mahadasha / Antardasha")
    tree.pack(side="left", fill="both", expand=True)
    tree_scroll.config(command=tree.yview)
    tree_scroll.pack(side="right", fill="y")

    detail_frame = ttk.LabelFrame(right, text="Details")
    detail_frame.pack(fill="both", expand=True)
    details = tk.Text(detail_frame, wrap="word")
    details.pack(fill="both", expand=True)

    node_data = {}

    # ------------------ BUILD MAHADASHA --------------------
    def build_mahadasha():
        tree.delete(*tree.get_children())
        node_data.clear()
        details.delete("1.0", "end")

        order, years = get_settings()
        moon_lord, frac = moon_nak_fraction()

        birth = datetime(
            d1.natal_chart.year, d1.natal_chart.month, d1.natal_chart.date,
            d1.natal_chart.hour, d1.natal_chart.minute, int(d1.natal_chart.second)
        )

        # FIRST dasha must ALWAYS be first lord in custom order
        first_lord = order[0]
        first_years = years[first_lord]
        elapsed = first_years * frac
        start = birth - timedelta(days=elapsed * 365.25)

        periods = []
        cur = start
        for lord in order:
            span = timedelta(days=years[lord] * 365.25)
            end = cur + span
            periods.append((lord, cur, end))
            cur = end

        for lord, s, e in periods:
            nid = tree.insert("", "end", text=f"{lord}: {s:%Y-%m-%d} → {e:%Y-%m-%d}")
            node_data[nid] = {"type": "maha", "lord": lord, "start": s, "end": e}
            tree.insert(nid, "end", text="(double click for antardasha)")

    # ------------------ ANTARDASHA --------------------------
    def build_antardasha(maha_lord, start, end):
        order, years = get_settings()                # <-- always refresh
        full_days = (end - start).total_seconds() / 86400

        # use standard vimshottari RATIO
        seq = order[:]                               # custom sequence
        std_total = sum(VIM_STD_YEARS.values())
        cur = start
        ants = []
        for lord in seq:
            part = VIM_STD_YEARS[lord] / std_total
            span = full_days * part
            new_end = cur + timedelta(days=span)
            ants.append((lord, cur, new_end))
            cur = new_end
        return ants

    # TREE EVENTS
    def on_expand(event):
        item = tree.focus()
        data = node_data.get(item)
        if not data or data["type"] != "maha":
            return

        for c in tree.get_children(item):
            tree.delete(c)

        ants = build_antardasha(data["lord"], data["start"], data["end"])
        for lord, s, e in ants:
            cid = tree.insert(item, "end", text=f"   {lord}: {s:%Y-%m-%d} → {e:%Y-%m-%d}")
            node_data[cid] = {"type": "antar", "lord": lord, "start": s, "end": e}

    def on_select(event):
        item = tree.focus()
        data = node_data.get(item)
        details.delete("1.0", "end")
        if not data:
            return
        details.insert("end", f"{data['type'].title()} Dasha\n")
        details.insert("end", f"Lord: {data['lord']}\n")
        details.insert("end", f"Start: {data['start']}\n")
        details.insert("end", f"End:   {data['end']}\n")

    tree.bind("<Double-1>", on_expand)
    tree.bind("<<TreeviewSelect>>", on_select)

    ttk.Button(win, text="BUILD MAHADASHA", command=build_mahadasha).pack(pady=6)
    build_mahadasha()


def start_chart_menu():
    global horoscope
    if horoscope is None:
        messagebox.showerror("No chart", "No horoscope initialized.")
        return

    root = tk.Tk()
    root.title("Astrology Toolkit")
    root.geometry("1400x840")
    root.configure(bg="white")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    chart_frame = tk.Frame(root, bg="white")
    chart_frame.pack(fill="both", expand=True)

    # --- helpers for showing ---
    def show_one(hscope: Horror_scope):
        for w in chart_frame.winfo_children():
            w.destroy()
        cv = tk.Canvas(chart_frame, width=700, height=700, bg="white")
        cv.pack()
        draw_fixed_rashi_chart(hscope, size=700, canvas_override=cv)

    def show_all_charts():
        for w in chart_frame.winfo_children():
            w.destroy()

        rows = 2
        cols = 5
        chart_size = 260
        canv_w = canv_h = 260

        charts = [
            ("D1 Birth Chart", horoscope),
            ("D9 Navamsa", make_navamsa_horoscope(horoscope)),
            ("D3 Drekkana", make_drekkana_horoscope(horoscope)),
            ("D81 Chart", make_d81_horoscope(horoscope)),
            ("d4 chart",make_d4_horoscope(horoscope)),
            ("d10 chart",make_d10_horoscope(horoscope)),
            ("nadi d30 chart",make_nadid30_horoscope(horoscope)),
            ("d16 chart",make_d16_horoscope(horoscope)),
            ("d12 chart",make_d12_horoscope(horoscope)),
            ("d144 chart",make_d144_horoscope(horoscope))
        ]

        for idx, (label, hscope) in enumerate(charts):
            r = idx // cols
            c = idx % cols
            frame = tk.Frame(chart_frame, bg="white")
            frame.grid(row=r, column=c, padx=10, pady=10)

            tk.Label(frame, text=label, font=("Arial", 13, "bold"), bg="white").pack()

            cv = tk.Canvas(frame, width=canv_w, height=canv_h, bg="white", highlightthickness=0)
            cv.pack()
            draw_fixed_rashi_chart(hscope, size=chart_size, canvas_override=cv)

    # --- edit chart popup ---
    def edit_chart():
        global horoscope
        top = tk.Toplevel(root)
        top.title("Edit Birth Details")
        top.geometry("350x300")
        fields = {}
        nc = horoscope.natal_chart
        arr = [
            ("Name", nc.name),
            ("Date", nc.date),
            ("Month", nc.month),
            ("Year", nc.year),
            ("Hour", nc.hour),
            ("Minute", nc.minute),
            ("Second", nc.second),
            ("Longitude", nc.longitude),
            ("Latitude", nc.latitude),
            ("Timezone", nc.timezone),
            ("Altitude", nc.altidude)
        ]
        for i, (lbl, val) in enumerate(arr):
            tk.Label(top, text=lbl).grid(row=i, column=0, sticky="w")
            e = tk.Entry(top)
            e.insert(0, str(val))
            e.grid(row=i, column=1)
            fields[lbl] = e

        def apply():
            global horoscope
            for lbl, e in fields.items():
                v = e.get()
                if lbl == "Name":
                    setattr(nc, lbl.lower(), v)
                else:
                    setattr(nc, lbl.lower(), eval(v))
            horoscope = make_horoscope(nc)
            show_all_charts()
            top.destroy()

        tk.Button(top, text="Apply", command=apply).grid(row=len(arr), columnspan=2, pady=5)

    # --- open saved wrapper (updates global + refresh all charts) ---
    def open_saved_wrapper():
        global horoscope
        h = load_ast()
        if h is not None:
            show_all_charts()

    # menu – Chart
    cm = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Charts", menu=cm)
    cm.add_command(label="Show All Charts", command=show_all_charts)
    cm.add_command(label="D1 (only)", command=lambda: show_one(horoscope))
    cm.add_command(label="D9 (only)", command=lambda: show_one(make_navamsa_horoscope(horoscope)))
    cm.add_command(label="D3 (only)", command=lambda: show_one(make_drekkana_horoscope(horoscope)))
    cm.add_command(label="D81 (only)", command=lambda: show_one(make_d81_horoscope(horoscope)))

    # file section
    fm = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=fm)
    fm.add_command(label="Save as .ast", command=lambda: save_ast(horoscope))
    fm.add_command(label="Open saved", command=open_saved_wrapper)
    fm.add_command(label="Edit chart", command=edit_chart)
    fm.add_separator()
    fm.add_command(label="Exit", command=root.quit)

    # dasha
    dm = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Dasha", menu=dm)
    dm.add_command(label="Vimshottari Explorer", command=lambda: create_vimshottari_window(root))
    dm.add_command(label="Vimshottari Rajan dasa Explorer", command=lambda: create_custom_dasha_window(root))

    # transit
    tm = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Transit", menu=tm)
    tm.add_command(label="Open Transit", command=lambda: open_transit_tab(root, horoscope))

    # start with all charts
    show_all_charts()
    root.mainloop()


# ------------------------------------------------
# DEMO ENTRY
# ------------------------------------------------
if __name__ == "__main__":
    cd = chart_details("a", 18, 3, 2004, 22, 4, 44, 88.36666, 22.56666, -5.5, 0.0)
    H = make_horoscope(cd)
    horoscope = H
    start_chart_menu()

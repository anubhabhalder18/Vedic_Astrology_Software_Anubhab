import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from Data_Types import Horror_scope, Planet

# ----------------- CONSTANTS -----------------

VIMSHOTTARI_STD_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars",
                         "Rahu", "Jupiter", "Saturn", "Mercury"]

VIMSHOTTARI_STD_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

# 27 nakshatra lords in order (Ashwini .. Revati)
NAK_LORDS = (VIMSHOTTARI_STD_ORDER * 3)[:27]
NAK_LEN = 360.0 / 27.0  # 13°20'

# -------------- GENERIC HELPERS --------------


def compute_progression(start, end, deg0=0.0, parts=12):
    """Same progression helper you used earlier (kept as requested)."""
    total_days = (end - start).total_seconds() / (24 * 3600)
    first = total_days * ((30.0 - deg0) / 30.0) / parts
    remaining = total_days - first
    later = remaining / (parts - 1) if parts > 1 else remaining
    periods = []
    current = start
    for i in range(parts):
        span = first if i == 0 else later
        e = current + timedelta(days=span)
        periods.append((f"Part {i + 1}", current, e))
        current = e
    return periods


def moon_nak_and_fraction(parent,h: Horror_scope):
    """Return (nak_lord, nak_index0_26, fraction_traversed_in_nak) from horoscope."""
    lon = h.Moon.planet_position.longitude % 360.0
    nak_index = int(lon // NAK_LEN)  # 0..26
    start_deg = nak_index * NAK_LEN
    deg_in_nak = lon - start_deg
    frac = deg_in_nak / NAK_LEN  # 0..1
    lord = NAK_LORDS[nak_index]
    return lord, nak_index, frac


# -------------- MAHADASHA / ANTARDASHA LOGIC --------------


def build_mahadasha_sequence(h: Horror_scope,
                             custom_order,
                             custom_years):
    """
    Build mahadasha list based on:
    - custom_order: list of 9 lords in sequence
    - custom_years: dict lord->years (custom)
    Dasha balance from Moon nakshatra traversed.
    Returns list of (lord, start_dt, end_dt).
    """
    # Birth datetime from natal chart
    nc = h.natal_chart
    birth = datetime(nc.year, nc.month, nc.date,
                     nc.hour, nc.minute, int(nc.second))

    start_lord, _, frac_traversed = moon_nak_and_fraction(h)

    # rotate custom order to start from Moon's nakshatra lord
    if start_lord in custom_order:
        idx = custom_order.index(start_lord)
    else:
        idx = 0
        start_lord = custom_order[0]
    order_rot = custom_order[idx:] + custom_order[:idx]

    # dasa balance: first mahadasha started earlier
    first_years = custom_years.get(start_lord, VIMSHOTTARI_STD_YEARS[start_lord])
    elapsed_years = first_years * frac_traversed
    first_start = birth - timedelta(days=elapsed_years * 365.25)

    periods = []
    current = first_start
    for lord in order_rot:
        yrs = custom_years.get(lord, VIMSHOTTARI_STD_YEARS[lord])
        end = current + timedelta(days=yrs * 365.25)
        periods.append((lord, current, end))
        current = end
    return periods, birth, start_lord, frac_traversed


def build_antardasha_sequence(maha_lord, start, end):
    """
    Antar dashas:
    - Start from running mahadasha lord
    - Follow *standard* Vimshottari order
    - Duration ratios use *standard* Vimshottari years (not custom),
      but scaled to actual mahadasha length.
    """
    # standard order rotated so it begins from maha_lord
    std = VIMSHOTTARI_STD_ORDER
    idx = std.index(maha_lord)
    seq = std[idx:] + std[:idx]

    # actual mahadasha length in days
    total_days = (end - start).total_seconds() / (24 * 3600)
    # compute total std years (should be 120)
    total_std = sum(VIMSHOTTARI_STD_YEARS[l] for l in std)

    periods = []
    current = start
    for lord in seq:
        fraction = VIMSHOTTARI_STD_YEARS[lord] / total_std
        span_days = total_days * fraction
        e = current + timedelta(days=span_days)
        periods.append((lord, current, e))
        current = e
    return periods


# -------------- TKINTER WINDOW --------------


def open_custom_dasha_window(h: Horror_scope):
    """
    Tkinter window:
    - Edit custom dasha order & years
    - Build Mahadasha tree with Antardashas
    - Dasha balance from Moon nakshatra traversed
    """

    root = tk.Toplevel()
    root.title("Custom Dasha Explorer")
    root.geometry("1100x720")

    # -------- top: config for order/durations --------
    config_frame = ttk.LabelFrame(root, text="Dasha Configuration")
    config_frame.pack(fill="x", padx=6, pady=4)

    ttk.Label(config_frame, text="Order").grid(row=0, column=0, padx=4)
    ttk.Label(config_frame, text="Lord").grid(row=0, column=1, padx=4)
    ttk.Label(config_frame, text="Years").grid(row=0, column=2, padx=4)

    lord_choices = VIMSHOTTARI_STD_ORDER[:]  # allowed lords
    order_widgets = []
    year_widgets = []

    for i in range(9):
        ttk.Label(config_frame, text=str(i + 1)).grid(row=i + 1, column=0, padx=4, pady=1, sticky="e")
        cb = ttk.Combobox(config_frame, values=lord_choices, state="readonly", width=8)
        cb.set(VIMSHOTTARI_STD_ORDER[i])
        cb.grid(row=i + 1, column=1, padx=4, pady=1)
        order_widgets.append(cb)

        e = ttk.Entry(config_frame, width=6)
        lord = VIMSHOTTARI_STD_ORDER[i]
        e.insert(0, str(VIMSHOTTARI_STD_YEARS[lord]))
        e.grid(row=i + 1, column=2, padx=4, pady=1)
        year_widgets.append(e)

    def get_config():
        order = [cb.get() for cb in order_widgets]
        years = {}
        for cb, ent in zip(order_widgets, year_widgets):
            lord = cb.get()
            try:
                yrs = float(ent.get())
            except ValueError:
                yrs = VIMSHOTTARI_STD_YEARS[lord]
            years[lord] = yrs
        return order, years

    # -------- left: treeview --------
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=6, pady=4)

    left_frame = ttk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=False)

    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True)

    tree_scroll = ttk.Scrollbar(left_frame, orient="vertical")
    tree = ttk.Treeview(left_frame, yscrollcommand=tree_scroll.set)
    tree.heading("#0", text="Mahadasha / Antardasha", anchor="w")
    tree.pack(side="left", fill="both", expand=True)
    tree_scroll.config(command=tree.yview)
    tree_scroll.pack(side="right", fill="y")

    # -------- right: details & buttons --------
    info_frame = ttk.LabelFrame(right_frame, text="Details")
    info_frame.pack(fill="both", expand=True, padx=4, pady=4)

    detail_text = tk.Text(info_frame, wrap="word")
    detail_scroll = ttk.Scrollbar(info_frame, orient="vertical", command=detail_text.yview)
    detail_text.configure(yscrollcommand=detail_scroll.set)
    detail_text.pack(side="left", fill="both", expand=True)
    detail_scroll.pack(side="right", fill="y")

    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", padx=6, pady=4)

    btn_build = ttk.Button(button_frame, text="Build Dasha")
    btn_build.pack(side="left", padx=4)

    node_data = {}  # tree_id -> dict(type,lord,start,end)

    # -------- building and callbacks --------

    def build_tree():
        order, years = get_config()

        md_list, birth, start_lord, frac = build_mahadasha_sequence(h, order, years)

        # clear tree & detail
        for item in tree.get_children():
            tree.delete(item)
        node_data.clear()
        detail_text.delete("1.0", "end")

        detail_text.insert(
            "end",
            f"Birth: {birth}\n"
            f"Moon Nakshatra Lord: {start_lord}\n"
            f"Moon traversed: {frac * 100:.2f}% of nakshatra\n"
            f"Custom Order: {order}\n\n"
            f"Mahadashas:\n"
        )

        for lord, s, e in md_list:
            txt = f"{lord}: {s:%Y-%m-%d} → {e:%Y-%m-%d}"
            nid = tree.insert("", "end", text=txt, open=False)
            node_data[nid] = {"type": "maha", "lord": lord, "start": s, "end": e}
            # placeholder child for lazy antardasha loading
            tree.insert(nid, "end", text="(double-click to load antardashas)")

    def on_open(event):
        item = tree.focus()
        data = node_data.get(item)
        if not data or data["type"] != "maha":
            return

        # if already expanded and children are real antardashas, do nothing
        children = tree.get_children(item)
        if children and "(double-click" not in tree.item(children[0], "text"):
            return

        # remove placeholder
        for c in children:
            tree.delete(c)

        lord = data["lord"]
        s = data["start"]
        e = data["end"]
        antars = build_antardasha_sequence(lord, s, e)

        for alord, as_, ae_ in antars:
            txt = f"   {alord}: {as_:%Y-%m-%d} → {ae_:%Y-%m-%d}"
            cid = tree.insert(item, "end", text=txt, open=False)
            node_data[cid] = {"type": "antar", "lord": alord, "start": as_, "end": ae_}

    def on_select(event):
        item = tree.focus()
        data = node_data.get(item)
        detail_text.delete("1.0", "end")
        if not data:
            return
        typ = data["type"]
        lord = data["lord"]
        s = data["start"]
        e = data["end"]

        detail_text.insert(
            "end",
            f"Type: {typ}\nLord: {lord}\nStart: {s}\nEnd:   {e}\n\n"
        )
        if typ == "maha":
            detail_text.insert("end", "Double-click this node to generate Antardashas.\n")

    btn_build.config(command=build_tree)
    tree.bind("<Double-1>", on_open)
    tree.bind("<<TreeviewSelect>>", on_select)

    build_tree()  # initial build with defaults


# -------------- DEMO (remove if importing) --------------

if __name__ == "__main__":
    # This demo assumes you already have a Horror_scope instance `H`.
    # Replace this import/creation with your actual horoscope creation.
    from Data_Types import chart_details, position

    # Dummy chart just so the window can open if you run this file directly.
    cd = chart_details(
        name="Demo",
        date=18,
        month=3,
        year=2004,
        hour=22,
        minute=4,
        second=44,
        longitude=88.3667,
        latitude=22.5667,
        timezone=-5.5,
    )

    # Here you should call your real `make_horoscope(cd)` instead
    # For a stand-alone dummy: create planets with arbitrary positions.
    def dummy_planet(name, lon):
        return Planet.make(name, lon, 1.0)

    asc_pos = position.make(100.0)
    asc_pl = Planet.make("Ascendant", asc_pos.longitude, 0.0)

    H = Horror_scope(
        ascendant=asc_pl,
        natal_chart=cd,
        Sun=dummy_planet("Sun", 10.0),
        Moon=dummy_planet("Moon", 40.0),
        Mercury=dummy_planet("Mercury", 70.0),
        Venus=dummy_planet("Venus", 100.0),
        Mars=dummy_planet("Mars", 130.0),
        Jupiter=dummy_planet("Jupiter", 160.0),
        Saturn=dummy_planet("Saturn", 190.0),
        Rahu=dummy_planet("Rahu", 220.0),
        Ketu=dummy_planet("Ketu", 40.0),  # opposite of Rahu just as placeholder
        weekday="Thursday",
    )

    root = tk.Tk()
    root.withdraw()
    open_custom_dasha_window(H)
    root.mainloop()

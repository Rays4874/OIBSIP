import tkinter as tk
from tkinter import font as tkfont
import requests
import threading
from dotenv import load_dotenv
import os
from PIL import Image, ImageTk
from datetime import datetime, timezone, timedelta

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
IP_GEO_URL = "https://ipinfo.io/json"
PLACEHOLDER = "Enter city name..."

THEMES = {
    "dark": {
        "bg": "#1e2a3a",
        "panel": "#263545",
        "header": "#16213e",
        "fg": "#e0e8f0",
        "fg_muted": "#a8c0d6",
        "desc_fg": "#7a9ab5",
        "divider": "#3a5068",
        "entry_bg": "#263545",
        "success": "#4a8a5e",
        "btn_toggle": "#263545",
        "btn_toggle_fg": "#e0e8f0"
    },
    "light": {
        "bg": "#f0f4f8",
        "panel": "#ffffff",
        "header": "#d9e2ec",
        "fg": "#102a43",
        "fg_muted": "#486581",
        "desc_fg": "#627d98",
        "divider": "#bcccdc",
        "entry_bg": "#e2e8f0",
        "success": "#22543d",
        "btn_toggle": "#ffffff",
        "btn_toggle_fg": "#102a43"
    }
}

current_theme = "dark"
# We removed "forecast" from the cache since Open-Meteo handles both now!
weather_cache = {"current": None, "aqi": None, "daily": None, "source": ""}

CONDITION_ICONS = {
    "Clear": "icons/sun.png",
    "Clouds": "icons/clouds.png",
    "Rain": "icons/rain.png",
    "Drizzle": "icons/drizzle.png",
    "Thunderstorm": "icons/thunderstorm.png",
    "Snow": "icons/snow.png",
    "Mist": "icons/mist.png",
    "Fog": "icons/fog.png",
    "Haze": "icons/haze.png",
    "Smoke": "icons/smoke.png",
    "Dust": "icons/dust.png",
    "Sand": "icons/sand.png",
    "Ash": "icons/ash.png",
    "Squall": "icons/squall.png",
    "Tornado": "icons/tornado.png",
}

_image_cache = {}


def get_weather_image(condition_main: str, size: tuple = (64, 64)):
    image_path = CONDITION_ICONS.get(condition_main, "icons/clouds.png")
    cache_key = (image_path, size)
    if cache_key in _image_cache: return _image_cache[cache_key]
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        _image_cache[cache_key] = photo
        return photo
    except Exception:
        return None


def get_condition_from_wmo(code: int) -> str:
    if code == 0:
        return "Clear"
    elif code in [1, 2, 3]:
        return "Clouds"
    elif code in [45, 48]:
        return "Fog"
    elif code in [51, 53, 55, 56, 57]:
        return "Drizzle"
    elif code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "Rain"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "Snow"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    return "Clouds"


def calculate_standard_aqi(pm25: float) -> tuple:
    if pm25 <= 12.0:
        c_low, c_high, i_low, i_high, cat = 0.0, 12.0, 0, 50, "Good"
    elif pm25 <= 35.4:
        c_low, c_high, i_low, i_high, cat = 12.1, 35.4, 51, 100, "Moderate"
    elif pm25 <= 55.4:
        c_low, c_high, i_low, i_high, cat = 35.5, 55.4, 101, 150, "Unhealthy"
    elif pm25 <= 150.4:
        c_low, c_high, i_low, i_high, cat = 55.5, 150.4, 151, 200, "Unhealthy"
    elif pm25 <= 250.4:
        c_low, c_high, i_low, i_high, cat = 150.5, 250.4, 201, 300, "Very Unhealthy"
    else:
        c_low, c_high, i_low, i_high, cat = 250.5, 500.4, 301, 500, "Hazardous"
    aqi = ((i_high - i_low) / (c_high - c_low)) * (pm25 - c_low) + i_low
    return round(aqi), cat


def detect_city_from_ip() -> str:
    try:
        response = requests.get(IP_GEO_URL, timeout=8)
        if response.status_code != 200: raise RuntimeError(f"HTTP {response.status_code}")
        city = response.json().get("city", "").strip()
        if not city: raise RuntimeError("Could not determine city.")
        return city
    except Exception as e:
        raise RuntimeError(f"Detection failed: {e}")


def create_weather_app():
    global current_theme
    t = THEMES[current_theme]

    root = tk.Tk()
    root.title("Weather Forecast App")
    root.geometry("920x800")
    root.resizable(False, False)
    root.configure(bg=t["bg"])

    title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
    label_font = tkfont.Font(family="Helvetica", size=12)
    button_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
    small_btn_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
    city_big_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
    stat_font = tkfont.Font(family="Helvetica", size=13)
    desc_font = tkfont.Font(family="Helvetica", size=14, slant="italic")
    error_font = tkfont.Font(family="Helvetica", size=12)
    forecast_time_font = tkfont.Font(family="Helvetica", size=10)
    forecast_temp_font = tkfont.Font(family="Helvetica", size=11, weight="bold")

    themed_bgs = []
    themed_panels = []
    themed_headers = []
    themed_text = []
    themed_text_muted = []
    themed_desc = []
    themed_dividers = []

    header_frame = tk.Frame(root, bg=t["header"], pady=12)
    header_frame.pack(fill="x")
    themed_headers.append(header_frame)

    try:
        logo_raw = Image.open("icons/logo.png")
        logo_raw = logo_raw.resize((36, 36), Image.Resampling.LANCZOS)
        app_logo_img = ImageTk.PhotoImage(logo_raw)
        _image_cache["main_logo"] = app_logo_img
        header_title = tk.Label(header_frame, text="  Weather Forecast Application", image=app_logo_img,
                                compound="left", font=title_font, bg=t["header"], fg=t["fg"])
    except Exception:
        header_title = tk.Label(header_frame, text="🌤  Weather Forecast Application", font=title_font, bg=t["header"],
                                fg=t["fg"])

    header_title.pack(side="left", padx=40)
    themed_headers.append(header_title)
    themed_text.append(header_title)

    def toggle_theme():
        global current_theme
        current_theme = "light" if current_theme == "dark" else "dark"
        apply_theme()

    theme_btn = tk.Button(header_frame, text="☀️ Light Mode", font=small_btn_font, bg=t["btn_toggle"],
                          fg=t["btn_toggle_fg"], relief="flat", cursor="hand2", command=toggle_theme)
    theme_btn.pack(side="right", padx=40)

    header_div = tk.Frame(root, height=2, bg=t["divider"])
    header_div.pack(fill="x")
    themed_dividers.append(header_div)

    search_frame = tk.Frame(root, bg=t["bg"], pady=16)
    search_frame.pack(fill="x", padx=40)
    themed_bgs.append(search_frame)

    search_label = tk.Label(search_frame, text="City :", font=label_font, bg=t["bg"], fg=t["fg_muted"])
    search_label.grid(row=0, column=0, padx=(0, 8))
    themed_bgs.append(search_label)
    themed_text_muted.append(search_label)

    city_entry = tk.Entry(search_frame, width=30, font=label_font, bg=t["entry_bg"], fg=t["fg"],
                          insertbackground=t["fg"], relief="flat", bd=6)
    city_entry.grid(row=0, column=1, padx=(0, 10), ipady=4)
    city_entry.insert(0, PLACEHOLDER)
    city_entry.config(fg=t["desc_fg"])

    def clear_placeholder(event):
        if city_entry.get() == PLACEHOLDER:
            city_entry.delete(0, tk.END)
            city_entry.config(fg=THEMES[current_theme]["fg"])

    def restore_placeholder(event):
        if city_entry.get() == "":
            city_entry.insert(0, PLACEHOLDER)
            city_entry.config(fg=THEMES[current_theme]["desc_fg"])

    city_entry.bind("<FocusIn>", clear_placeholder)
    city_entry.bind("<FocusOut>", restore_placeholder)

    search_btn = tk.Button(search_frame, text="🔍  Search", font=button_font, bg="#0078d7", fg="#ffffff",
                           activebackground="#005fa3", activeforeground="#ffffff", relief="flat", padx=12, pady=6,
                           cursor="hand2")
    search_btn.grid(row=0, column=2, padx=(0, 8))

    location_btn = tk.Button(search_frame, text="📍  Use Current Location", font=small_btn_font, bg="#1a6b3c",
                             fg="#ffffff", activebackground="#145530", activeforeground="#ffffff", relief="flat",
                             padx=12, pady=6, cursor="hand2")
    location_btn.grid(row=0, column=3)

    main_container = tk.Frame(root, bg=t["panel"], bd=0)
    main_container.pack(fill="both", expand=True, padx=40, pady=(0, 16))
    themed_panels.append(main_container)

    main_canvas = tk.Canvas(main_container, bg=t["panel"], highlightthickness=0)
    main_canvas.pack(side="left", fill="both", expand=True)
    themed_panels.append(main_canvas)

    main_scrollbar = tk.Scrollbar(main_container, orient="vertical", command=main_canvas.yview)
    main_scrollbar.pack(side="right", fill="y")
    main_canvas.configure(yscrollcommand=main_scrollbar.set)

    display_inner = tk.Frame(main_canvas, bg=t["panel"])
    themed_panels.append(display_inner)

    canvas_window = main_canvas.create_window((0, 0), window=display_inner, anchor="nw")

    def configure_scroll_region(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))

    display_inner.bind("<Configure>", configure_scroll_region)

    def configure_canvas_width(event):
        if main_canvas.winfo_width() > display_inner.winfo_width():
            main_canvas.itemconfig(canvas_window, width=main_canvas.winfo_width())

    main_canvas.bind("<Configure>", configure_canvas_width)

    def _on_mousewheel(event):
        main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    city_row = tk.Frame(display_inner, bg=t["panel"])
    city_row.pack(pady=(10, 4))
    themed_panels.append(city_row)

    icon_label = tk.Label(city_row, text="", font=tkfont.Font(size=28), bg=t["panel"], fg=t["fg"])
    icon_label.pack(side="left", padx=(0, 8))
    themed_panels.append(icon_label)

    city_name_label = tk.Label(city_row, text="— City —", font=city_big_font, bg=t["panel"], fg=t["fg"])
    city_name_label.pack(side="left")
    themed_panels.append(city_name_label)
    themed_text.append(city_name_label)

    source_var = tk.StringVar(value="")
    source_label = tk.Label(display_inner, textvariable=source_var, font=tkfont.Font(family="Helvetica", size=9),
                            bg=t["panel"], fg=t["success"])
    source_label.pack(pady=(0, 2))
    themed_panels.append(source_label)

    desc_label = tk.Label(display_inner, text="Search a city or use your location", font=desc_font, bg=t["panel"],
                          fg=t["desc_fg"])
    desc_label.pack(pady=(0, 10))
    themed_panels.append(desc_label)
    themed_desc.append(desc_label)

    alerts_container = tk.Frame(display_inner, bg=t["panel"])
    alerts_container.pack(fill="x", pady=(0, 5))
    themed_panels.append(alerts_container)

    div1 = tk.Frame(display_inner, height=1, bg=t["divider"])
    div1.pack(fill="x", padx=30)
    themed_dividers.append(div1)

    stats_frame = tk.Frame(display_inner, bg=t["panel"])
    stats_frame.pack(pady=10)
    themed_panels.append(stats_frame)

    def make_stat(parent, icon_path, title, row, col):
        card = tk.Frame(parent, bg=t["bg"], padx=12, pady=8)
        card.grid(row=row, column=col, padx=8, pady=4, sticky="nsew")
        themed_bgs.append(card)

        size = (32, 32)
        cache_key = (icon_path, size)
        if cache_key not in _image_cache:
            try:
                img = Image.open(icon_path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                _image_cache[cache_key] = ImageTk.PhotoImage(img)
            except Exception:
                _image_cache[cache_key] = None

        photo = _image_cache[cache_key]
        img_lbl = tk.Label(card, image=photo, bg=t["bg"]) if photo else tk.Label(card, text="❓",
                                                                                 font=tkfont.Font(size=20), bg=t["bg"],
                                                                                 fg=t["fg"])
        img_lbl.pack(pady=(0, 4))
        themed_bgs.append(img_lbl)

        var = tk.StringVar(value="—")
        val_lbl = tk.Label(card, textvariable=var, font=stat_font, bg=t["bg"], fg=t["fg"])
        val_lbl.pack()
        themed_bgs.append(val_lbl)
        themed_text.append(val_lbl)

        title_lbl = tk.Label(card, text=title, font=tkfont.Font(family="Helvetica", size=9), bg=t["bg"],
                             fg=t["fg_muted"])
        title_lbl.pack()
        themed_bgs.append(title_lbl)
        themed_text_muted.append(title_lbl)

        return var

    temp_var = make_stat(stats_frame, "icons/temp.png", "Temperature", 0, 0)
    hum_var = make_stat(stats_frame, "icons/humidity.png", "Humidity", 0, 1)
    wind_var = make_stat(stats_frame, "icons/wind.png", "Wind Speed", 0, 2)
    feels_var = make_stat(stats_frame, "icons/feels_like.png", "Feels Like", 0, 3)
    aqi_var = make_stat(stats_frame, "icons/aqi.png", "Air Quality", 0, 4)

    div2 = tk.Frame(display_inner, height=1, bg=t["divider"])
    div2.pack(fill="x", padx=30, pady=(10, 5))
    themed_dividers.append(div2)

    f24_label = tk.Label(display_inner, text="24-Hour Forecast (Hourly)",
                         font=tkfont.Font(family="Helvetica", size=11, weight="bold"), bg=t["panel"], fg=t["fg_muted"])
    f24_label.pack()
    themed_panels.append(f24_label)
    themed_text_muted.append(f24_label)

    forecast_container = tk.Frame(display_inner, bg=t["panel"])
    forecast_container.pack(fill="x", padx=30, pady=(5, 5))
    themed_panels.append(forecast_container)

    canvas24 = tk.Canvas(forecast_container, bg=t["panel"], highlightthickness=0, height=115)
    scrollbar24 = tk.Scrollbar(forecast_container, orient="horizontal", command=canvas24.xview)
    scrollable_frame_24 = tk.Frame(canvas24, bg=t["panel"])
    themed_panels.extend([canvas24, scrollable_frame_24])

    scrollable_frame_24.bind("<Configure>", lambda e: canvas24.configure(scrollregion=canvas24.bbox("all")))
    canvas24.create_window((0, 0), window=scrollable_frame_24, anchor="nw")
    canvas24.configure(xscrollcommand=scrollbar24.set)
    canvas24.pack(side="top", fill="both", expand=True)
    scrollbar24.pack(side="bottom", fill="x")

    div3 = tk.Frame(display_inner, height=1, bg=t["divider"])
    div3.pack(fill="x", padx=30, pady=(10, 5))
    themed_dividers.append(div3)

    f7_label = tk.Label(display_inner, text="7-Day Forecast",
                        font=tkfont.Font(family="Helvetica", size=11, weight="bold"), bg=t["panel"], fg=t["fg_muted"])
    f7_label.pack()
    themed_panels.append(f7_label)
    themed_text_muted.append(f7_label)

    daily_container = tk.Frame(display_inner, bg=t["panel"])
    daily_container.pack(fill="x", padx=30, pady=(5, 10))
    themed_panels.append(daily_container)

    status_var = tk.StringVar(value="")
    status_label = tk.Label(display_inner, textvariable=status_var, font=error_font, bg=t["panel"], fg="#e05555")
    status_label.pack(pady=(0, 5))
    themed_panels.append(status_label)

    footer_label = tk.Label(root, text="Weather Forecast App  •  Task 10 – Hourly Forecast Data",
                            font=tkfont.Font(family="Helvetica", size=9), bg=t["header"], fg=t["divider"], pady=5)
    footer_label.pack(fill="x", side="bottom")
    themed_headers.append(footer_label)

    def apply_theme():
        th = THEMES[current_theme]
        root.config(bg=th["bg"])
        city_entry.config(bg=th["entry_bg"], fg=th["fg"], insertbackground=th["fg"])

        if current_theme == "dark":
            theme_btn.config(text="☀️ Light Mode", bg=th["btn_toggle"], fg=th["btn_toggle_fg"])
        else:
            theme_btn.config(text="🌙 Dark Mode", bg=th["btn_toggle"], fg=th["btn_toggle_fg"])

        for w in themed_bgs: w.config(bg=th["bg"])
        for w in themed_panels: w.config(bg=th["panel"])
        for w in themed_headers: w.config(bg=th["header"])
        for w in themed_text: w.config(fg=th["fg"])
        for w in themed_text_muted: w.config(fg=th["fg_muted"])
        for w in themed_desc: w.config(fg=th["desc_fg"])
        for w in themed_dividers: w.config(bg=th["divider"])

        footer_label.config(fg=th["divider"])

        if weather_cache["current"] is not None:
            show_data(weather_cache["current"], weather_cache["aqi"], weather_cache["daily"], weather_cache["source"])

    def set_buttons_state(state: str):
        search_btn.config(state=state)
        location_btn.config(state=state)

    def clear_forecasts():
        for widget in scrollable_frame_24.winfo_children(): widget.destroy()
        for widget in daily_container.winfo_children(): widget.destroy()
        for widget in alerts_container.winfo_children(): widget.destroy()

    def show_loading(message="Fetching…"):
        city_name_label.config(text=message)
        blank = tk.PhotoImage()
        icon_label.config(image=blank, text="⏳")
        icon_label.image = blank
        desc_label.config(text="Please wait…")
        source_var.set("")
        for var in (temp_var, hum_var, wind_var, feels_var, aqi_var): var.set("…")
        status_var.set("")
        clear_forecasts()
        main_canvas.yview_moveto(0)

    def show_error(message: str):
        city_name_label.config(text="Not Found", fg="#e05555")
        blank = tk.PhotoImage()
        icon_label.config(image=blank, text="❌")
        icon_label.image = blank
        desc_label.config(text="")
        source_var.set("")
        for var in (temp_var, hum_var, wind_var, feels_var, aqi_var): var.set("—")
        status_var.set(message)
        clear_forecasts()
        search_btn.config(state="normal", text="🔍  Search")
        location_btn.config(state="normal", text="📍  Use Current Location")

    # NOTE: forecast_data (OWM) parameter removed since we use daily_data for both now!
    def show_data(current_data: dict, aqi_data: dict, daily_data: dict, source: str = "searched"):
        th = THEMES[current_theme]

        weather_cache["current"] = current_data
        weather_cache["aqi"] = aqi_data
        weather_cache["daily"] = daily_data
        weather_cache["source"] = source

        main = current_data["main"]
        wind = current_data["wind"]
        weather_info = current_data["weather"][0]
        city = current_data.get("name", "Unknown")
        country = current_data.get("sys", {}).get("country", "")

        city_name_label.config(text=f"{city}, {country}", fg=th["fg"])

        weather_img = get_weather_image(weather_info["main"], size=(80, 80))
        if weather_img:
            icon_label.config(image=weather_img, text="")
        else:
            blank = tk.PhotoImage()
            icon_label.config(image=blank, text="❓")
            icon_label.image = blank

        desc_label.config(text=weather_info["description"].title(), fg=th["desc_fg"])

        temp_val = main['temp']
        wind_speed_kmh = wind['speed'] * 3.6
        condition = weather_info["main"]

        temp_var.set(f"{temp_val:.1f} °C")
        feels_var.set(f"{main['feels_like']:.1f} °C")
        hum_var.set(f"{main['humidity']} %")
        wind_var.set(f"{wind_speed_kmh:.1f} km/h")

        if aqi_data and "list" in aqi_data:
            pm25_val = aqi_data["list"][0]["components"]["pm2_5"]
            calculated_aqi, aqi_category = calculate_standard_aqi(pm25_val)
            aqi_var.set(f"{calculated_aqi} ({aqi_category})")
        else:
            aqi_var.set("—")

        status_var.set("")
        source_label.config(fg=th["success"])
        source_var.set("📍 Auto-detected via IP" if source == "auto" else "🔍 Searched manually")

        clear_forecasts()

        alerts = []
        if temp_val >= 35: alerts.append(("⚠️ High Temperature Alert", "#c0392b"))
        if temp_val <= 0: alerts.append(("❄️ Freezing Conditions Expected", "#2980b9"))
        if wind_speed_kmh >= 50: alerts.append(("💨 Strong Winds Warning", "#d35400"))
        if condition in ["Thunderstorm", "Tornado", "Squall"]:
            alerts.append((f"⚠️ {condition} Warning", "#c0392b"))
        elif condition in ["Rain"]:
            alerts.append(("🌧️ Rain Expected", "#f39c12"))
        elif condition in ["Snow"]:
            alerts.append(("❄️ Snow Expected", "#2980b9"))

        for msg, color in alerts:
            alert_lbl = tk.Label(alerts_container, text=msg, bg=color, fg="#ffffff",
                                 font=tkfont.Font(family="Helvetica", size=10, weight="bold"), pady=4)
            alert_lbl.pack(fill="x", pady=(0, 4), padx=30)

        # ── NEW: True Hourly 24-Hour Forecast (Open-Meteo) ──
        if daily_data and "hourly" in daily_data:
            hourly = daily_data["hourly"]

            # 1. Calculate the exact local time of the city searched
            city_time = datetime.now(timezone.utc) + timedelta(seconds=current_data["timezone"])
            current_hour_str = city_time.strftime("%Y-%m-%dT%H:00")

            # 2. Find where that hour is in the API array
            start_idx = 0
            for idx, t_str in enumerate(hourly["time"]):
                if t_str >= current_hour_str:
                    start_idx = idx
                    break

            # 3. Build exactly 24 hourly cards
            for i in range(start_idx, start_idx + 24):
                if i >= len(hourly["time"]): break  # Failsafe

                time_str = hourly["time"][i][11:16]  # Gets just the HH:MM
                temp = hourly["temperature_2m"][i]
                wmo_code = hourly["weathercode"][i]
                cond = get_condition_from_wmo(wmo_code)

                f_card = tk.Frame(scrollable_frame_24, bg=th["bg"], padx=15, pady=8, bd=1, relief="ridge")
                f_card.pack(side="left", padx=5, fill="y")

                # Make the very first card say "Now" instead of the time
                display_time = "Now" if i == start_idx else time_str
                tk.Label(f_card, text=display_time, font=forecast_time_font, bg=th["bg"], fg=th["fg_muted"]).pack()

                forecast_img = get_weather_image(cond, size=(40, 40))
                img_label = tk.Label(f_card, bg=th["bg"])
                if forecast_img:
                    img_label.config(image=forecast_img)
                else:
                    img_label.config(text="❓", font=tkfont.Font(size=16), fg=th["fg"])
                img_label.pack(pady=4)

                tk.Label(f_card, text=f"{temp:.1f}°C", font=forecast_temp_font, bg=th["bg"], fg=th["fg"]).pack()

        # 7-Day Forecast
        if daily_data and "daily" in daily_data:
            daily = daily_data["daily"]
            for i in range(7):
                date_str = daily["time"][i]
                max_t = daily["temperature_2m_max"][i]
                min_t = daily["temperature_2m_min"][i]
                wmo_code = daily["weathercode"][i]
                day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a")
                cond = get_condition_from_wmo(wmo_code)

                # Highlight "Today"
                if i == 0: day_name = "Today"

                d_card = tk.Frame(daily_container, bg=th["bg"], padx=8, pady=8, bd=1, relief="ridge")
                d_card.pack(side="left", padx=6, fill="y", expand=True)
                tk.Label(d_card, text=day_name, font=forecast_time_font, bg=th["bg"], fg=th["fg_muted"]).pack()

                daily_img = get_weather_image(cond, size=(40, 40))
                img_label = tk.Label(d_card, bg=th["bg"])
                if daily_img:
                    img_label.config(image=daily_img)
                else:
                    img_label.config(text="❓", font=tkfont.Font(size=16), fg=th["fg"])
                img_label.pack(pady=4)

                tk.Label(d_card, text=f"{min_t:.0f}° / {max_t:.0f}°", font=forecast_temp_font, bg=th["bg"],
                         fg=th["fg"]).pack()

        search_btn.config(state="normal", text="🔍  Search")
        location_btn.config(state="normal", text="📍  Use Current Location")

    def fetch_weather_for_city(city: str, source: str):
        if not API_KEY:
            root.after(0, show_error, "❌ OpenWeatherMap API key not found in .env file.")
            return
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        try:
            curr_resp = requests.get(BASE_URL, params=params, timeout=8)
            if curr_resp.status_code == 401: return root.after(0, show_error, "❌ Invalid API key.")
            if curr_resp.status_code == 404: return root.after(0, show_error, f"❌ City \"{city}\" not found.")
            if curr_resp.status_code != 200: return root.after(0, show_error, f"❌ API error {curr_resp.status_code}.")

            current_data = curr_resp.json()
            lat = current_data["coord"]["lat"]
            lon = current_data["coord"]["lon"]

            aqi_data = None
            aqi_params = {"lat": lat, "lon": lon, "appid": API_KEY}
            aqi_resp = requests.get(AIR_POLLUTION_URL, params=aqi_params, timeout=8)
            if aqi_resp.status_code == 200: aqi_data = aqi_resp.json()

            # ── NEW: Request "hourly" along with daily data ──
            daily_data = None
            om_params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m,weathercode",
                "daily": "weathercode,temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
                "forecast_days": 7  # Fetch 3 days to ensure we have a full 24h ahead
            }
            om_resp = requests.get(OPEN_METEO_URL, params=om_params, timeout=8)
            if om_resp.status_code == 200: daily_data = om_resp.json()

            # Passed to GUI
            root.after(0, show_data, current_data, aqi_data, daily_data, source)

        except requests.exceptions.ConnectionError:
            root.after(0, show_error, "❌ No internet connection.")
        except requests.exceptions.Timeout:
            root.after(0, show_error, "❌ Request timed out.")
        except Exception as exc:
            root.after(0, show_error, f"❌ Unexpected error: {exc}")

    def on_search():
        city = city_entry.get().strip()
        if not city or city == PLACEHOLDER: return show_error("⚠️ Please enter a city name.")
        set_buttons_state("disabled")
        search_btn.config(text="Searching…")
        show_loading()
        threading.Thread(target=fetch_weather_for_city, args=(city, "searched"), daemon=True).start()

    def on_use_location():
        set_buttons_state("disabled")
        location_btn.config(text="Detecting…")
        show_loading("Detecting location…")

        def detect_then_fetch():
            try:
                city = detect_city_from_ip()
            except RuntimeError as err:
                return root.after(0, show_error, f"📍 {err}")
            root.after(0, city_entry.delete, 0, tk.END)
            root.after(0, city_entry.insert, 0, city)
            root.after(0, lambda: city_entry.config(fg=THEMES[current_theme]["fg"]))
            fetch_weather_for_city(city, source="auto")

        threading.Thread(target=detect_then_fetch, daemon=True).start()

    search_btn.config(command=on_search)
    location_btn.config(command=on_use_location)
    city_entry.bind("<Return>", lambda _: on_search())

    root.mainloop()


if __name__ == "__main__":
    create_weather_app()
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import time


def type_text(text, widget, delay=25):
    """Typing animation for output box."""
    widget.config(state="normal")
    widget.delete(1.0, tk.END)

    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        widget.after(delay)  # typing speed in ms

    widget.config(state="disabled")


def get_ip_info():
    api_url = "https://ipwhois.app/json/"

    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()

            ipv4 = data.get("ip", "Not available")
            ipv6 = data.get("ipv6", "Not available")
            hostname = data.get("hostname", "Not available")
            city = data.get("city", "Not available")
            region = data.get("region", "Not available")
            country = data.get("country", "Not available")
            loc = data.get("loc", "Not available")
            org = data.get("org", "Not available")
            postal = data.get("postal", "Not available")
            timezone = data.get("timezone", "Not available")

            # Second API
            ipwhois_url = f"{api_url}{ipv4}"
            ipwhois_response = requests.get(ipwhois_url)

            if ipwhois_response.status_code == 200:
                details = ipwhois_response.json()
                asn = details.get("asn", "Not available")
                isp = details.get("isp", "Not available")
                country_code = details.get("country_code", "Not available")

                output = (
                    f"IPv4 Address: {ipv4}\n"
                    f"IPv6 Address: {ipv6}\n"
                    f"Hostname: {hostname}\n"
                    f"Location: {city}, {region}, {country}\n"
                    f"Coordinates: {loc}\n"
                    f"Organization: {org}\n"
                    f"Postal Code: {postal}\n"
                    f"Timezone: {timezone}\n"
                    f"ASN: {asn}\n"
                    f"ISP: {isp}\n"
                    f"Country Code: {country_code}\n"
                )

                # CALL TYPING EFFECT HERE
                type_text(output, result_box)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------------------
#    DARK UI SETUP
# -------------------------------
window = tk.Tk()
window.title("IP Information Tool")
window.geometry("700x540")
window.configure(bg="#000000")
window.resizable(False, False)

dark_bg = "#000000"
card_bg = "#0F0F0F"
text_color = "#E0E0E0"
blue = "#1E4BD8"
blue_hover = "#163A9F"
box_bg = "#1A1A1A"
border_color = "#2A2A2A"

style = ttk.Style()
style.theme_use("clam")

style.configure("Dark.TFrame", background=card_bg)

style.configure(
    "Dark.TLabel",
    background=card_bg,
    foreground=text_color,
    font=("Segoe UI", 11)
)

style.configure(
    "HeaderDark.TLabel",
    background=card_bg,
    foreground=text_color,
    font=("Segoe UI Semibold", 16)
)

style.configure(
    "Blue.TButton",
    background=blue,
    foreground="white",
    font=("Segoe UI", 12, "bold"),
    padding=8,
    relief="flat"
)
style.map("Blue.TButton", background=[("active", blue_hover)])

card = ttk.Frame(window, padding=20, style="Dark.TFrame")
card.place(relx=0.5, rely=0.5, anchor="center", width=640, height=470)

title_label = ttk.Label(card, text="IP Information Tool", style="HeaderDark.TLabel")
title_label.pack(anchor="w", pady=(0, 12))

fetch_button = ttk.Button(card, text="Get My IP Information", style="Blue.TButton", command=get_ip_info)
fetch_button.pack(anchor="w", pady=5)

sep = ttk.Separator(card)
sep.pack(fill="x", pady=15)

result_label = ttk.Label(card, text="Details:", style="HeaderDark.TLabel")
result_label.pack(anchor="w")

result_box = scrolledtext.ScrolledText(
    card,
    wrap=tk.WORD,
    width=70,
    height=18,
    font=("Consolas", 11),
    state="disabled",
    background=box_bg,
    foreground=text_color,
    insertbackground=text_color,
    border=1,
    relief="solid"
)
result_box.pack(pady=10)

window.mainloop()

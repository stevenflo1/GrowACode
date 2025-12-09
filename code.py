import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests


# -------------------------------
# Typing effect with blue details
# -------------------------------
def type_text_blue_details(text, widget, delay=20):
    widget.config(state="normal")
    widget.delete(1.0, tk.END)

    for line in text.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            widget.insert(tk.END, key + ": ")
            widget.insert(tk.END, value + "\n", "blue_text")  # all details in blue
        else:
            widget.insert(tk.END, line + "\n")
        widget.update()
        widget.after(delay)

    widget.config(state="disabled")


# -------------------------------
# Fetch IP info
# -------------------------------
def get_ip_info():
    api_url = "https://ipwhois.app/json/"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("success", True) is False:
            messagebox.showerror("Error", data.get("message", "Failed to fetch IP info"))
            return

        ipv4 = data.get("ip", "Not available")
        country = data.get("country", "Not available")
        country_code = data.get("country_code", "Not available")
        region = data.get("region", "Not available")
        city = data.get("city", "Not available")
        postal = data.get("postal", "Not available")
        timezone = data.get("timezone", "Not available")

        output = (
            f"IP Address: {ipv4}\n"
            f"Country: {country}\n"
            f"Region: {region}\n"
            f"City: {city}\n"
            f"Postal: {postal}\n"
            f"Timezone: {timezone}\n"
            f"Country Code: {country_code}\n"
        )

        # Call typing animation with blue details
        type_text_blue_details(output, result_box)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------------------
# DARK UI SETUP
# -------------------------------
window = tk.Tk()
window.title("IP Information Tool")
window.geometry("700x540")
window.configure(bg="#000000")
window.resizable(False, False)

# Colors
card_bg = "#0F0F0F"
text_color = "#E0E0E0"
blue_color = "#1E90FF"  # blue for details
blue = "#1E4BD8"
blue_hover = "#163A9F"
box_bg = "#1A1A1A"

# Style
style = ttk.Style()
style.theme_use("clam")

style.configure("Dark.TFrame", background=card_bg)
style.configure("Dark.TLabel", background=card_bg, foreground=text_color, font=("Segoe UI", 11))
style.configure("HeaderDark.TLabel", background=card_bg, foreground=text_color, font=("Segoe UI Semibold", 16))
style.configure("Blue.TButton", background=blue, foreground="white", font=("Segoe UI", 12, "bold"), padding=8)
style.map("Blue.TButton", background=[("active", blue_hover)])

# Card container
card = ttk.Frame(window, padding=20, style="Dark.TFrame")
card.place(relx=0.5, rely=0.5, anchor="center", width=640, height=470)

# Title
title_label = ttk.Label(card, text="IP Information Tool", style="HeaderDark.TLabel")
title_label.pack(anchor="w", pady=(0, 12))

# Button
fetch_button = ttk.Button(card, text="Get My IP Information", style="Blue.TButton", command=get_ip_info)
fetch_button.pack(anchor="w", pady=5)

# Separator
sep = ttk.Separator(card)
sep.pack(fill="x", pady=15)

# Subtitle
result_label = ttk.Label(card, text="Details:", style="HeaderDark.TLabel")
result_label.pack(anchor="w")

# Results box
result_box = tk.Text(
    card,
    wrap=tk.WORD,
    width=70,
    height=18,
    background=box_bg,
    foreground=text_color,
    insertbackground=text_color,
    borderwidth=2,
    relief="solid",
    highlightbackground=blue_color,
    highlightcolor=blue_color
)
result_box.pack(pady=10)

# Tag configuration for blue details
result_box.tag_configure("blue_text", foreground=blue_color)

# Cross-platform mouse wheel scrolling
def _on_mousewheel(event):
    if event.num == 4:  # Linux scroll up
        result_box.yview_scroll(-1, "units")
    elif event.num == 5:  # Linux scroll down
        result_box.yview_scroll(1, "units")
    else:  # Windows/macOS
        result_box.yview_scroll(int(-1*(event.delta/120)), "units")


# Bindings
result_box.bind("<MouseWheel>", _on_mousewheel)   # Windows/macOS
result_box.bind("<Button-4>", _on_mousewheel)     # Linux scroll up
result_box.bind("<Button-5>", _on_mousewheel)     # Linux scroll down

window.mainloop()

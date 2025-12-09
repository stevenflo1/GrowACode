import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os

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
            widget.insert(tk.END, value + "\n", "blue_text")
        else:
            widget.insert(tk.END, line + "\n")
        widget.update()
        widget.after(delay)

    widget.config(state="disabled")

# -------------------------------
# Fetch IP info
# -------------------------------
def get_ip_info(widget=None):
    """
    If widget is provided, display output in the Text widget.
    Otherwise, return the output string (for testing).
    """
    api_url = "https://ipwhois.app/json/"

    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
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

        ipwhois_response = requests.get(f"{api_url}{ipv4}")
        ipwhois_response.raise_for_status()
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

        if widget is not None:
            type_text_blue_details(output, widget)

        return output

    except Exception as e:
        if widget is not None:
            messagebox.showerror("Error", str(e))
        else:
            raise

# -------------------------------
# GUI setup (only if main and display available)
# -------------------------------
if __name__ == "__main__":
    if os.environ.get("DISPLAY") or os.name == "nt":  # Windows always allowed
        window = tk.Tk()
        window.title("IP Information Tool")
        window.geometry("700x540")
        window.configure(bg="#000000")
        window.resizable(False, False)

        # Colors
        card_bg = "#0F0F0F"
        text_color = "#E0E0E0"
        blue_color = "#1E90FF"
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

        # Results box
        result_box = tk.Text(
            card,
            wrap=tk.WORD,
            width=70,
            height=18,
            font=("Consolas", 11),
            state="disabled",
            background=box_bg,
            foreground=text_color,
            insertbackground=text_color,
            borderwidth=2,
            relief="solid",
            highlightbackground=blue_color,
            highlightcolor=blue_color
        )
        result_box.pack(pady=10)
        result_box.tag_configure("blue_text", foreground=blue_color)

        # Button
        fetch_button = ttk.Button(card, text="Get My IP Information", style="Blue.TButton",
                                  command=lambda: get_ip_info(result_box))
        fetch_button.pack(anchor="w", pady=5)

        # Separator
        sep = ttk.Separator(card)
        sep.pack(fill="x", pady=15)

        # Subtitle
        result_label = ttk.Label(card, text="Details:", style="HeaderDark.TLabel")
        result_label.pack(anchor="w")

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            if event.num == 4:
                result_box.yview_scroll(-1, "units")
            elif event.num == 5:
                result_box.yview_scroll(1, "units")
            else:
                result_box.yview_scroll(int(-1*(event.delta/120)), "units")

        result_box.bind("<MouseWheel>", _on_mousewheel)
        result_box.bind("<Button-4>", _on_mousewheel)
        result_box.bind("<Button-5>", _on_mousewheel)

        window.mainloop()
    else:
        print("No display available. Skipping GUI.")

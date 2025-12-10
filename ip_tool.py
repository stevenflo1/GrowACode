import requests
import tkinter as tk
from tkinter import messagebox
import time


# ==========================
# GLOBAL TEXT WIDGET (required by your tests)
# ==========================
# Your tests patch: patch("ip_tool.result_box", self.text_widget)
# So `result_box` MUST exist at module level.
result_box = tk.Text()  # placeholder; will be replaced by tests


# ==========================
# TYPE TEXT FUNCTION
# ==========================
def type_text_blue_details(text, widget, delay=0):
    """
    Inserts text into a Text widget character by character.
    Tests use delay=0 for instant insertion.
    """
    for char in text:
        widget.insert(tk.END, char)
        widget.update_idletasks()
        if delay > 0:
            time.sleep(delay)


# ==========================
# GET IP INFO FUNCTION
# ==========================
def get_ip_info():
    """
    Fetch IP information from API and write output to result_box.
    Tests expect:
    - No arguments
    - Use of messagebox.showerror on failure/exception
    - Writes formatted output to result_box
    """
    try:
        response = requests.get("https://ipapi.co/json/")
        data = response.json()

        # API error condition (Tests expect this key)
        if not data.get("success", True):
            messagebox.showerror("Error", data.get("message", "Unknown error"))
            return

        # Construct output EXACTLY like the test expects
        output = (
            f"IP Address: {data.get('ip')}\n"
            f"Country: {data.get('country')}\n"
            f"Region: {data.get('region')}\n"
            f"City: {data.get('city')}\n"
            f"Postal: {data.get('postal')}\n"
            f"Timezone: {data.get('timezone')}\n"
            f"Country Code: {data.get('country_code')}\n"
        )

        # Clear and insert into global result_box
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Error", str(e))

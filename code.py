import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

def get_ip_info():
    api_url = "https://ipwhois.app/json/"
    
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            
            ipv4_address = data.get("ip", "Not available")
            ipv6_address = data.get("ipv6", "Not available")
            hostname = data.get("hostname", "Not available")
            city = data.get("city", "Not available")
            region = data.get("region", "Not available")
            country = data.get("country", "Not available")
            loc = data.get("loc", "Not available")
            org = data.get("org", "Not available")
            postal = data.get("postal", "Not available")
            timezone = data.get("timezone", "Not available")
            
            ipwhois_api_url = f"{api_url}{ipv4_address}"
            ipwhois_response = requests.get(ipwhois_api_url)
            
            if ipwhois_response.status_code == 200:
                ipwhois_data = ipwhois_response.json()
                asn = ipwhois_data.get("asn", "Not available")
                isp = ipwhois_data.get("isp", "Not available")
                country_code = ipwhois_data.get("country_code", "Not available")
                
                # Format output
                output = (
                    "=== IP Address Information ===\n"
                    f"IPv4 Address: {ipv4_address}\n"
                    f"IPv6 Address: {ipv6_address}\n"
                    f"Hostname: {hostname}\n"
                    f"Location: {city}, {region}, {country}\n"
                    f"Geolocation: {loc}\n"
                    f"Organization: {org}\n"
                    f"Postal Code: {postal}\n"
                    f"Timezone: {timezone}\n"
                    f"ASN: {asn}\n"
                    f"ISP: {isp}\n"
                    f"Country Code: {country_code}\n"
                )
                
                result_box.config(state='normal')
                result_box.delete(1.0, tk.END)
                result_box.insert(tk.END, output)
                result_box.config(state='disabled')
            else:
                messagebox.showerror("Error", "Failed to retrieve data from IPWhois API.")
        else:
            messagebox.showerror("Error", f"IPinfo.io returned status code: {response.status_code}")
    
    except Exception as e:
        messagebox.showerror("Exception", f"An error occurred: {e}")


# -------------------------------
# GUI SETUP
# -------------------------------

window = tk.Tk()
window.title("IP Information Lookup")
window.geometry("600x500")

title_label = tk.Label(window, text="IP Information Viewer", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

fetch_button = tk.Button(window, text="Get My IP Information", font=("Arial", 14), command=get_ip_info)
fetch_button.pack(pady=10)

result_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20, state='disabled')
result_box.pack(pady=10)

window.mainloop()

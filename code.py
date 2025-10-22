import requests
def get_ip_info():
    api_url = "https://ipwhois.app/json/"
    
    try:
        # Get public IP address information from ipinfo.io
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
            
            # Now use IPWhois API to fetch detailed information for the retrieved IPv4 address
            ipwhois_api_url = f"{api_url}{ipv4_address}"
            ipwhois_response = requests.get(ipwhois_api_url)
            
            if ipwhois_response.status_code == 200:
                ipwhois_data = ipwhois_response.json()
                asn = ipwhois_data.get("asn", "Not available")
                isp = ipwhois_data.get("isp", "Not available")
                country_code = ipwhois_data.get("country_code", "Not available")
                
                print("\n=== IP Address Information ===")
                print(f"IPv4 Address: {ipv4_address}")
                print(f"IPv6 Address: {ipv6_address}")
                print(f"Hostname: {hostname}")
                print(f"Location: {city}, {region}, {country}")
                print(f"Geolocation (Latitude, Longitude): {loc}")
                print(f"Organization: {org}")
                print(f"Postal Code: {postal}")
                print(f"Timezone: {timezone}")
                print(f"ASN: {asn}")
                print(f"ISP: {isp}")
                print(f"Country Code: {country_code}")
            else:
                print("Failed to retrieve information from IPWhois API.")
        else:
            print(f"Failed to retrieve IP information. HTTP Status Code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred while retrieving IP information: {e}")

get_ip_info()

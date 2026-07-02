import urllib.request
import json
import webbrowser
import sys

# ANSI Colors
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"

def fetch_ip():
    """Tries multiple public IP echo APIs to retrieve the public IP."""
    apis = [
        "https://api.ipify.org?format=json",
        "https://ipinfo.io/json",
        "https://ifconfig.me/all.json"
    ]
    
    for api in apis:
        try:
            req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                # Return the IP key (usually 'ip' or 'ip_addr' or 'query')
                if 'ip' in data:
                    return data['ip']
                elif 'query' in data:
                    return data['query']
        except Exception:
            continue
    return None

def geolocate(ip=None):
    """Fetches geolocation details for a given IP (or self if None) using ip-api.com."""
    url = "http://ip-api.com/json/"
    if ip:
        url += ip
        
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                return data
            else:
                print(f"{C_RED}[✗] API Error: {data.get('message', 'Unknown error')}{C_RESET}")
                return None
    except Exception as e:
        print(f"{C_RED}[✗] Connection failed: {e}{C_RESET}")
        return None

def main():
    print(f"{C_BOLD}{C_CYAN}📡 IP GEOLOCATOR & TELEMETRY TOOL 📡{C_RESET}")
    print("Queries public mapping APIs to extract network geolocation details.\n")
    
    # 1. Ask for IP or automatic detection
    ip_input = input("Enter an IP Address to locate (or press Enter for your public IP): ").strip()
    
    if not ip_input:
        print("Detecting your public IP address...")
        ip = fetch_ip()
        if not ip:
            print(f"{C_RED}[✗] Failed to resolve public IP. Please check your internet connection.{C_RESET}")
            sys.exit(1)
        print(f"Found IP: {C_GREEN}{ip}{C_RESET}\n")
    else:
        ip = ip_input

    # 2. Fetch geolocation
    print(f"Resolving coordinates and ISP details for {C_BOLD}{ip}{C_RESET}...")
    geo_data = geolocate(ip)
    
    if not geo_data:
        print(f"{C_RED}[✗] Failed to retrieve geolocation telemetry.{C_RESET}")
        sys.exit(1)
        
    # 3. Print report
    print(f"\n{C_BOLD}{C_CYAN}================ GEOLOCATION TELEMETRY ================{C_RESET}")
    print(f"{C_BOLD}IP Address:{C_RESET}     {geo_data.get('query')}")
    print(f"{C_BOLD}Country:{C_RESET}        {geo_data.get('country')} ({geo_data.get('countryCode')})")
    print(f"{C_BOLD}Region/State:{C_RESET}   {geo_data.get('regionName')}")
    print(f"{C_BOLD}City/Location:{C_RESET}  {geo_data.get('city')}")
    print(f"{C_BOLD}Zip Code:{C_RESET}       {geo_data.get('zip')}")
    print(f"{C_BOLD}Timezone:{C_RESET}       {geo_data.get('timezone')}")
    print(f"{C_BOLD}Coordinates:{C_RESET}    Lat: {geo_data.get('lat')}, Lon: {geo_data.get('lon')}")
    print(f"{C_BOLD}ISP/Network:{C_RESET}    {geo_data.get('isp')}")
    print(f"{C_BOLD}Organization:{C_RESET}   {geo_data.get('org') or 'N/A'} ({geo_data.get('as')})")
    print(f"{C_CYAN}======================================================={C_RESET}\n")

    # 4. Generate map link and ask to open
    lat = geo_data.get('lat')
    lon = geo_data.get('lon')
    
    if lat is not None and lon is not None:
        gmaps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        print(f"Google Maps Location Link:")
        print(f"{C_YELLOW}{gmaps_link}{C_RESET}\n")
        
        open_browser = input("Would you like to open this location in your web browser? (y/n): ").strip().lower()
        if open_browser == 'y':
            print("Launching web browser...")
            webbrowser.open(gmaps_link)
            print(f"{C_GREEN}[✓] Browser opened.{C_RESET}")
    else:
        print(f"{C_RED}[!] Geographic coordinates were not provided by the API.{C_RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Locator cancelled.")

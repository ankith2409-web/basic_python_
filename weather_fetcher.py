import urllib.request
import json

def fetch_weather(latitude, longitude):
    """
    Fetches current weather data for given coordinates using the Open-Meteo API.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if 'current_weather' in data:
                current = data['current_weather']
                temperature = current.get('temperature')
                windspeed = current.get('windspeed')
                time = current.get('time')
                
                print(f"--- Current Weather at ({latitude}, {longitude}) ---")
                print(f"Time: {time}")
                print(f"Temperature: {temperature}°C")
                print(f"Wind Speed: {windspeed} km/h")
            else:
                print("Could not retrieve current weather data.")
    except Exception as e:
        print(f"An error occurred while fetching the weather: {e}")

if __name__ == "__main__":
    print("Weather Fetcher (powered by Open-Meteo)")
    try:
        lat_input = input("Enter latitude (e.g., 52.52) [Press Enter for default]: ")
        lon_input = input("Enter longitude (e.g., 13.41) [Press Enter for default]: ")
        
        lat = float(lat_input) if lat_input.strip() else 52.52
        lon = float(lon_input) if lon_input.strip() else 13.41
        
        fetch_weather(lat, lon)
    except ValueError:
        print("Invalid input. Please enter numerical coordinates.")

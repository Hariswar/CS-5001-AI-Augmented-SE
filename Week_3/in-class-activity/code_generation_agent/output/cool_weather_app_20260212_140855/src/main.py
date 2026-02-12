import streamlit as st
import requests
from datetime import datetime

# Set page config
st.set_page_config(page_title="Cool Weather App", layout="wide")

# Title and description
st.title("🌤️ Cool Weather App")
st.write("Check the current weather for any location around the world")

# Location input
location = st.text_input("Enter a location (city, country):", "London, UK")

# Weather data fetching function
def get_weather_data(location):
    try:
        # Using OpenWeatherMap API (you'll need an API key)
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# Get weather data
if st.button("Get Weather"):
    weather_data = get_weather_data(location)

    if weather_data:
        # Display weather information
        st.subheader(f"Current Weather in {weather_data['name']}, {weather_data['sys']['country']}")

        # Main weather info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{weather_data['main']['temp']}°C")
            st.metric("Feels Like", f"{weather_data['main']['feels_like']}°C")
        with col2:
            st.metric("Humidity", f"{weather_data['main']['humidity']}%")
            st.metric("Pressure", f"{weather_data['main']['pressure']} hPa")
        with col3:
            st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")
            st.metric("Visibility", "N/A")  # Not always available in API

        # Additional details
        st.write(f"**Weather Conditions:** {weather_data['weather'][0]['description'].title()}")
        st.write(f"**Sunrise:** {datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')}")
        st.write(f"**Sunset:** {datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')}")

        # Weather icon (using emoji)
        weather_main = weather_data['weather'][0]['main'].lower()
        if 'clear' in weather_main:
            st.write("☀️ Clear skies")
        elif 'rain' in weather_main:
            st.write("🌧️ Rainy")
        elif 'cloud' in weather_main:
            st.write("☁️ Cloudy")
        elif 'snow' in weather_main:
            st.write("❄️ Snowy")
        elif 'thunder' in weather_main:
            st.write("⛈️ Thunderstorm")
        else:
            st.write("🌤️ Partly cloudy")
    else:
        st.error("Could not retrieve weather data. Please check the location and try again.")

# Footer
st.markdown("---")
st.write("Built with Streamlit | Data from OpenWeatherMap API")

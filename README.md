# WeatherCLI
Python CLI app that fetches live weather data and logs it to CSV with pandas

### <img width="1920" height="1011" alt="Screenshot 2026-08-17 123322" src="https://github.com/user-attachments/assets/6d70b1df-ac99-40b8-bac4-e32df4e90e5d" />
<img width="1920" height="1011" alt="Screenshot 2026-08-17 123322" src="https://github.com/user-attachments/assets/ccbc042b-d91a-415e-94af-becd449cd9a2" />
Features:
- Get real-time weather for any city using OpenWeather API
- Automatically logs timestamp, temp, humidity, wind, min/max to `weather_log.csv`
- Clean virtual environment setup with `requirements.txt`
- Built with `requests`, `pandas`

### How to Run
```bash
git clone <your-repo-link>
cd WeatherCLI
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python Weatherapp.py

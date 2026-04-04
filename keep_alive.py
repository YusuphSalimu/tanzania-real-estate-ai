import requests
import time
import schedule
from datetime import datetime

def ping_backend():
    try:
        response = requests.get('https://tanzania-real-estate-ai.onrender.com/health', timeout=10)
        print(f"[{datetime.now()}] Backend ping successful: {response.status_code}")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Backend ping failed: {e}")
        return False

def ping_multiple_times():
    print("Pinging backend multiple times to keep it warm...")
    for i in range(3):
        ping_backend()
        time.sleep(30)  # Wait 30 seconds between pings

# Schedule pings every 10 minutes
schedule.every(10).minutes.do(ping_multiple_times)

if __name__ == "__main__":
    print("Keep-alive service started...")
    ping_multiple_times()  # Initial ping
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

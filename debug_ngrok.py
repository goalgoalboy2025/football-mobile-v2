from pyngrok import ngrok
import sys

print("Testing ngrok...")
try:
    # Check if ngrok is installed
    print("Connecting to port 8080...")
    public_url = ngrok.connect(8080).public_url
    print(f"Ngrok URL: {public_url}")
    ngrok.kill()
except Exception as e:
    print(f"Error: {e}")

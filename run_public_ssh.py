import flet as ft
import subprocess
import threading
import time
import sys
import qrcode
import re
import os
from main import main as app_main

# Global variable to store the public URL
public_url = None

def print_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    qr.print_ascii(invert=True)

def start_ssh_tunnel():
    global public_url
    print("正在尝试通过 SSH 建立公共隧道 (Trying localhost.run)...")
    
    # Command to start SSH tunnel
    # -o StrictHostKeyChecking=no prevents the yes/no prompt
    # -R 80:localhost:8080 forwards port 80 on remote to 8080 on local
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8088", "nokey@localhost.run"]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            encoding='utf-8'
        )
        
        # Read output to find the URL
        while True:
            # localhost.run prints the URL to stdout or stderr? Usually stdout.
            line = process.stdout.readline()
            if not line:
                break
            
            # Check for URL in output
            # Example: "tunneled with tls change, https://something.lhr.life forwarding to ..."
            print(f"[SSH] {line.strip()}")
            
            match = re.search(r'(https://[a-zA-Z0-9.-]+\.lhr\.life)', line)
            if not match:
                 # Sometimes it's .localhost.run or other domains
                 match = re.search(r'(https://[a-zA-Z0-9.-]+\.localhost\.run)', line)
            
            if match:
                public_url = match.group(1)
                print(f"\n✅ 隧道建立成功！(Tunnel Established)")
                print(f"👉  {public_url}")
                print("\n扫描二维码 (Scan QR code):\n")
                print_qr(public_url)
                print("\n保持此窗口开启以维持访问 (Keep open)")
                break
                
        # Keep reading to prevent buffer filling
        for line in process.stdout:
            pass
            
    except Exception as e:
        print(f"SSH Tunnel Error: {e}")
        print("如果 SSH 方式失败，请尝试使用 ngrok (需配置 token)")

if __name__ == "__main__":
    port = 8088
    
    # Start SSH tunnel in background thread
    t = threading.Thread(target=start_ssh_tunnel, daemon=True)
    t.start()
    
    # Wait a bit for tunnel to initialize (optional)
    time.sleep(2)
    
    print("\n" + "="*50)
    print(f" 🌍 公网访问模式 (Public Access Mode)")
    print("="*50)
    print("正在启动应用... (Starting App)")
    
    # Run Flet App
    try:
        ft.app(target=app_main, view=ft.WEB_BROWSER, port=port, host="0.0.0.0")
    except KeyboardInterrupt:
        pass

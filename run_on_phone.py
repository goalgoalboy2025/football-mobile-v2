import flet as ft
import socket
import qrcode
import os
import sys

# Import the main app logic
from main import main as app_main

def get_local_ip():
    try:
        # Create a dummy socket to connect to an external IP (doesn't actually connect)
        # This helps to find the preferred local IP used for internet access
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def print_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    qr.print_ascii(invert=True)

if __name__ == "__main__":
    port = 8080
    ip = get_local_ip()
    url = f"http://{ip}:{port}"
    
    print("\n" + "="*50)
    print(f" 📱 手机访问模式 (Mobile Access Mode)")
    print("="*50)
    print(f"\n1. 确保您的手机和电脑连接的是【同一个Wi-Fi】")
    print(f"   (Make sure your phone and PC are on the same Wi-Fi)\n")
    print(f"2. 请使用手机浏览器访问以下地址：")
    print(f"   (Open this URL on your phone)\n")
    print(f"   👉  {url}")
    print("\n" + "-"*50 + "\n")
    
    try:
        print("或者直接扫描下方二维码 (Or scan QR code):\n")
        print_qr(url)
    except Exception:
        pass
        
    print("\n" + "="*50 + "\n")
    print("正在启动服务... (Starting server...)")
    print("提示：如果无法访问，请检查电脑防火墙是否允许 Python 通信")
    print("(Note: Check Windows Firewall if connection fails)\n")

    # Run the Flet app in web mode
    try:
        ft.app(target=app_main, view=ft.WEB_BROWSER, port=port, host="0.0.0.0")
    except KeyboardInterrupt:
        print("\n服务已停止 (Server stopped)")

import flet as ft
from pyngrok import ngrok, conf
import qrcode
import sys
import os

# Import the main app logic
from main import main as app_main

def print_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    qr.print_ascii(invert=True)

if __name__ == "__main__":
    port = 8080
    
    # Optional: Set auth token if provided in env or code
    # ngrok.set_auth_token("YOUR_AUTHTOKEN")
    
    print("\n" + "="*50)
    print(f" 🌍 公网访问模式 (Public Access Mode)")
    print("="*50)
    print("正在建立隧道... (Establishing tunnel...)")
    
    try:
        # Open a ngrok tunnel to the socket
        # bind_tls=True ensures https which is often better for mobile
        public_url = ngrok.connect(port, bind_tls=True).public_url
        
        print(f"\n✅ 成功！无需同一Wi-Fi，任何地方都可访问！")
        print(f"(Success! Access from anywhere)\n")
        print(f"👉  {public_url}")
        print("\n" + "-"*50 + "\n")
        
        try:
            print("扫描二维码 (Scan QR code):\n")
            print_qr(public_url)
        except Exception:
            pass
            
        print("\n⚠️ 重要提示 (Important Note):")
        print("1. 如果遇到 ngrok 警告页面，请点击 'Visit Site' 继续")
        print("   (Click 'Visit Site' if you see a warning page)")
        print("2. 免费版 ngrok 隧道可能会在几小时后过期，重新运行即可")
        print("   (Free tunnel expires after some time, restart to renew)\n")

        # Run the Flet app
        ft.app(target=app_main, view=ft.WEB_BROWSER, port=port, host="0.0.0.0")
        
    except Exception as e:
        print(f"\n❌ 错误 (Error): {e}")
        print("请检查网络连接，或者尝试配置 ngrok auth token。")
    except KeyboardInterrupt:
        print("\n正在关闭隧道... (Closing tunnel...)")
        ngrok.kill()

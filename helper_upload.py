import webbrowser
import os
import time

def main():
    print("正在为您准备上传环境...")
    
    # 1. 打开本地文件夹
    folder_path = r"d:\ai-study\trae-world\projects\kanqiu\football-mobile"
    print(f"1. 打开本地文件夹: {folder_path}")
    os.startfile(folder_path)
    
    # 2. 打开 GitHub 创建页面
    print("2. 打开 GitHub 网站...")
    webbrowser.open("https://github.com/new")
    
    print("\n" + "="*60)
    print("🚀 傻瓜式操作指南")
    print("="*60)
    print("步骤一：在刚刚打开的浏览器页面中")
    print("   1. 如果提示登录，请先注册或登录 GitHub")
    print("   2. 在 'Repository name' 输入框中填入: football-mobile")
    print("   3. 滚动到底部，点击绿色的 'Create repository' 按钮")
    print("\n步骤二：上传文件")
    print("   1. 创建成功后，点击页面中间蓝色的链接 'uploading an existing file'")
    print("   2. 切换到刚刚弹出的文件夹窗口")
    print("   3. 按 Ctrl+A 全选所有文件")
    print("   4. 将它们拖拽到浏览器的上传区域")
    print("   5. 等待上传进度条结束，点击底部的绿色按钮 'Commit changes'")
    print("\n步骤三：获取 APP")
    print("   1. 点击页面顶部的 'Actions' 标签")
    print("   2. 等待 'Build Android APK' 变成绿色对勾 (约3分钟)")
    print("   3. 点击它，下载 'football-fixtures-apk'")
    print("="*60)
    
    # Keep window open
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()

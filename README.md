# Football Fixtures Mobile App

这是一个基于 Python Flet 框架构建的移动端应用，用于查询足球赛事信息。

## 1. 在电脑上运行 (开发预览)

确保已安装 Python 3.x，然后运行以下命令：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 2. 打包为 Android App (APK)

要将此项目打包为 Android APK 文件，你需要使用 `flet build` 命令。
注意：打包过程需要安装 Android SDK 和 Flutter 环境。建议在 Linux 或 macOS 上操作，或者使用 GitHub Actions。

### 本地打包 (如果你已配置好 Flutter/Android 环境)

```bash
flet build apk
```

### 使用 GitHub Actions 打包 (推荐)

如果你没有本地 Android 开发环境，可以将此项目上传到 GitHub，然后使用 GitHub Actions 自动构建。

1. 将 `football-mobile` 文件夹内容上传到新的 GitHub 仓库。
2. 在仓库中创建 `.github/workflows/build.yml` 文件，内容参考 Flet 官方文档的 CI 配置。
3. GitHub 会自动构建并生成 APK 文件供下载。

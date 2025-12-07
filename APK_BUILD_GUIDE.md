# 📱 如何获取 Android 安装包 (APK)

由于您的电脑上没有安装 Android 开发环境（通常需要下载 10GB+ 的文件并进行复杂配置），最简单、最专业的方法是利用 **GitHub Actions 云端构建**。

我已经为您配置好了一切，您只需要执行以下步骤：

## 准备工作 (已自动完成)

1.  **图标处理**：我已经将 `football_v2.ico` 转换为 `assets/icon.png`，App 将会自动使用此图标。
2.  **配置修正**：修复了 `.gitignore` 导致无法上传工作流配置的问题。

## 第一步：将代码上传到 GitHub

1.  登录 [GitHub](https://github.com/) 并创建一个新仓库（例如命名为 `football-mobile`）。
2.  在您的电脑终端中，进入 `football-mobile` 文件夹，依次运行以下命令：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <您的GitHub仓库地址>
git push -u origin main
```

*(如果您不熟悉 git 命令，也可以直接在 GitHub 网页上上传文件)*

## 第二步：等待自动构建

1.  代码上传后，点击 GitHub 仓库页面的 **"Actions"** 标签。
2.  您会看到一个名为 **"Build Android APK"** 的任务正在运行。
3.  等待约 3-5 分钟，任务变绿（成功）后点击进入。

## 第三步：下载安装

1.  在任务详情页的底部 **"Artifacts"** 区域。
2.  点击 **"football-fixtures-apk"** 下载压缩包。
3.  解压后得到 `.apk` 文件，发送到手机安装即可！

---

## 💡 为什么这样做？

*   **免配置**：无需在本地安装 Java, Android SDK, Flutter 等庞大工具。
*   **高性能**：使用 GitHub 的高性能服务器进行编译。
*   **自动化**：以后每次修改代码推送到 GitHub，都会自动生成新的安装包。

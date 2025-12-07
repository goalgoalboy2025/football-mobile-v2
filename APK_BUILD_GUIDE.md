# 📱 如何将程序转换为 Android APP (APK)

这个指南将帮助您利用 GitHub 的免费云端服务，将当前的足球赛程程序打包成安卓手机可以安装的 APK 文件。

**我已经为您完成了所有复杂的配置工作（包括图标转换、环境配置等），您只需要简单的上传操作。**

## 📋 准备工作 (已完成)

1.  ✅ **图标准备**：我已经将 `football_v2.ico` 转换为手机专用的 `assets/icon.png`。
2.  ✅ **配置修复**：修复了 `.gitignore` 以确保构建脚本能正确上传。
3.  ✅ **构建脚本**：优化了 GitHub Actions 脚本，增加了 Java 环境和自动依赖安装。

---

## 🚀 第一步：将代码上传到 GitHub

您需要将 `football-mobile` 文件夹中的内容上传到 GitHub。

### 方法 A：使用 Git 命令 (推荐)

如果您安装了 Git，请在终端中进入 `football-mobile` 文件夹并执行：

```bash
# 1. 初始化仓库
git init

# 2. 添加所有文件
git add .

# 3. 提交更改
git commit -m "准备构建 APK"

# 4. 创建主分支
git branch -M main

# 5. 关联远程仓库 (请替换为您自己的 GitHub 仓库地址)
git remote add origin https://github.com/您的用户名/仓库名.git

# 6. 推送代码
git push -u origin main
```

### 方法 B：网页上传 (如果您没有安装 Git)

1.  登录 [GitHub](https://github.com/) 并点击右上角的 **+** -> **New repository** 创建新仓库。
2.  在仓库页面，点击 **"uploading an existing file"** 链接。
3.  将本地 `football-mobile` 文件夹内的 **所有文件和文件夹** (包括 `.github` 文件夹) 拖入网页上传区域。
    *   *注意：请确保 `.github` 文件夹也被上传，这是自动构建的关键！*
4.  点击底部的 **Commit changes** 按钮。

---

## ⏳ 第二步：等待自动构建

1.  上传完成后，点击 GitHub 仓库页面顶部的 **"Actions"** 标签。
2.  您应该能看到一个名为 **"Build Android APK"** 的工作流正在运行 (黄色旋转图标)。
3.  点击该工作流，等待约 5-10 分钟。
4.  当图标变成绿色对号 ✅ 时，表示构建成功。

---

## 📥 第三步：下载并安装

1.  点击构建成功的任务名称 (例如 "Build Android APK")。
2.  向下滚动到页面底部的 **"Artifacts"** 区域。
3.  点击 **"football-fixtures-apk"** 下载压缩包。
4.  解压下载的文件，您将得到一个 `.apk` 安装包。
5.  将该文件发送到您的安卓手机并安装即可！

---

## ❓ 常见问题

*   **构建失败了怎么办？**
    请点击 Actions 页面中失败的任务，查看详细日志。通常是因为临时网络问题，您可以尝试点击右上角的 "Re-run jobs" 重试。
*   **安装时提示"未知的来源"？**
    这是安卓系统的安全机制，请在手机设置中允许安装来自此来源的应用，或选择"允许一次"。

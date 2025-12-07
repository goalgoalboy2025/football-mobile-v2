# 📤 如何将代码上传到 GitHub (无需 Git 命令行)

由于检测到您的电脑**没有安装 Git 工具**，最简单的方法是使用 **网页上传**。

请务必按照以下步骤操作，以确保自动化构建脚本 (`.github` 文件夹) 能被正确识别。

---

## 步骤 1：创建仓库
1.  登录 [GitHub.com](https://github.com/)。
2.  点击右上角的 **+** 号，选择 **New repository**。
3.  **Repository name** 输入 `football-mobile`。
4.  **Public/Private** 选 Public（公开）或 Private（私有）均可。
5.  **不要勾选** "Add a README file" 或其他初始化选项（保持仓库为空）。
6.  点击 **Create repository**。

## 步骤 2：准备文件
1.  打开您的电脑文件资源管理器。
2.  进入文件夹：`d:\ai-study\trae-world\projects\kanqiu\football-mobile`
    *   *(提示：这就是本项目所在的文件夹)*
3.  **关键步骤**：请确保您能看到一个名为 `.github` 的文件夹。
    *   如果看不到，请在资源管理器上方点击“查看” -> 勾选“隐藏的项目”。
    *   *(如果没有上传这个文件夹，GitHub 就不知道如何帮您打包 APP)*

## 步骤 3：上传文件
1.  在刚刚创建的 GitHub 仓库页面，点击蓝色的链接文字 **uploading an existing file**。
    *   或者直接点击页面上的 **Upload files** 按钮。
2.  **全选** 本地 `football-mobile` 文件夹内的**所有文件和文件夹**（包括 `.github`, `main.py`, `requirements.txt` 等）。
3.  将它们**拖拽**到 GitHub 的上传区域。
    *   *注意：请确保拖拽包含了 `.github` 文件夹。*
4.  等待文件上传进度条走完。
5.  在下方的 "Commit changes" 框中，直接点击绿色的 **Commit changes** 按钮。

## 步骤 4：开始构建
1.  上传完成后，点击仓库顶部的 **Actions** 标签页。
2.  您应该能看到一个名为 **Build Android APK** 的工作流自动开始了（黄色旋转图标）。
3.  等待约 3-5 分钟，图标变成绿色对勾 ✅。
4.  点击该工作流，在页面底部找到 **Artifacts**，点击 `football-fixtures-apk` 下载安装包。

---

**常见问题：**
*   **问：我看不到 `.github` 文件夹？**
    *   答：这是 Windows 默认隐藏了以点开头的文件。请务必开启“显示隐藏文件”功能，或者直接全选文件夹内容拖拽，通常也会包含它。

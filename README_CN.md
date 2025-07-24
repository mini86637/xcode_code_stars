# xcode-code-stats

## 项目简介
xcode-code-stats 是一个用于统计 Xcode 项目代码量的工具。它能够遍历指定的目录，计算代码行数，并提供代码行数占比的统计信息。

## 功能
- 统计指定目录下的代码行数
- 自动识别主项目 Target 和 Pod（三方库），并分别统计代码量及占比
- 计算主项目与三方库的代码行数占比
- 支持多种文件类型的统计

## 使用方法

1. 克隆或下载该项目。
2. 安装所需的依赖库：
   ```
   pip install -r requirements.txt
   ```
   
   依赖说明：
   - Flask：Web 服务框架，用于 webapp.py 提供网页界面
   - Werkzeug：WSGI 工具库，Flask 依赖
   - Bootstrap-Flask：集成 Bootstrap 前端样式
   - Jinja2：模板渲染引擎，Flask 依赖

### 脚本运行方式

1. 在 `src/main.py` 中指定要统计的 Xcode 项目目录。
2. 运行主程序：
   ```
   python src/main.py
   ```
3. 程序会自动识别主项目 Target 和 Pod（三方库）目录，并分别统计代码量及占比。

4. 支持命令行参数指定项目路径（可选）：
   ```
   python src/main.py /path/to/your/xcode/project
   ```
   如果未指定参数，则会使用代码中默认路径。

### Web 运行方式

1. 启动 Web 服务：
   ```
   python webapp.py
   ```
2. 在浏览器访问：
   ```
   http://127.0.0.1:5000
   ```
3. 按页面提示输入或粘贴 Xcode 项目路径，点击统计即可查看结果。




### Electron 桌面版运行与打包方式

1. 进入 electron-app 目录：
   ```
   cd electron-app
   ```
2. 安装依赖：
   ```
   npm install
   ```
3. 一键打包（自动下载 Xcode 图标并生成安装包）：
   ```
   ./build/download_xcode_icon_and_pack.sh
   ```
   如遇权限问题可先执行 `chmod +x ./build/download_xcode_icon_and_pack.sh`
4. 打包完成后，安装包文件位于 `electron-app/dist` 目录。
5. 双击安装包即可在桌面运行，界面与 Web 版一致。
6. 如需开发调试，可运行：
   ```
   npm run dev
   ```
   会自动启动 Flask 服务并加载本地网页。


   ## 贡献
欢迎提交问题和建议，或直接提交代码贡献。

## 许可证
该项目遵循 MIT 许可证。
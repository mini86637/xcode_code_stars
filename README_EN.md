# xcode-code-stats

## Project Introduction
xcode-code-stats is a tool for counting lines of code in Xcode projects. It can traverse the specified directory, calculate the number of code lines, and provide statistics on the proportion of code lines.

## Features
- Count lines of code in the specified directory
- Automatically identify main project Target and Pods (third-party libraries), and count code lines and proportions separately
- Calculate the proportion of code lines between the main project and third-party libraries
- Support statistics for multiple file types

## Usage

1. Clone or download this project.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Dependencies:
   - Flask: Web service framework, used for the web interface in webapp.py
   - Werkzeug: WSGI utility library, required by Flask
   - Bootstrap-Flask: Integrates Bootstrap frontend styles
   - Jinja2: Template rendering engine, required by Flask

### Script Usage

1. Specify the Xcode project directory to be counted in `src/main.py`.
2. Run the main program:
   ```
   python src/main.py
   ```
3. The program will automatically identify the main project Target and Pods (third-party libraries) directories, and count code lines and proportions separately.

4. You can specify the project path via command line arguments (optional):
   ```
   python src/main.py /path/to/your/xcode/project
   ```
   If no argument is specified, the default path in the code will be used.

### Web Usage

1. Start the web service:
   ```
   python webapp.py
   ```
2. Visit in your browser:
   ```
   http://127.0.0.1:5000
   ```
3. Enter or paste the Xcode project path as prompted on the page, click "Count" to view the results.

### Electron Desktop Version Usage and Packaging

1. Enter the electron-app directory:
   ```
   cd electron-app
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. One-click packaging (automatically downloads the Xcode icon and generates the installer):
   ```
   ./build/download_xcode_icon_and_pack.sh
   ```
   If you encounter permission issues, run `chmod +x ./build/download_xcode_icon_and_pack.sh` first.
4. After packaging, the installer file will be located in the `electron-app/dist` directory.
5. Double-click the installer to run the desktop version, which has the same interface as the web version.
6. For development and debugging, run:
   ```
   npm run dev
   ```
   This will automatically start the Flask service and load the local web page.

## Contribution
Feel free to submit issues and suggestions, or contribute code directly.

## License
This project is licensed under the
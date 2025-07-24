const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let flaskProcess = null;
let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });
  mainWindow.loadURL('http://127.0.0.1:5000');
  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

function startFlask() {
  // 兼容 macOS/Linux/Windows
  const python = process.platform === 'win32' ? 'python' : 'python3';
  const flaskScript = path.join(__dirname, '..', 'webapp.py');
  flaskProcess = spawn(python, [flaskScript], {
    cwd: path.join(__dirname, '..'),
    stdio: 'ignore',
    detached: true
  });
}

app.on('ready', () => {
  startFlask();
  // 等待 Flask 启动后再加载页面
  setTimeout(createWindow, 2000);
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    if (flaskProcess) flaskProcess.kill();
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

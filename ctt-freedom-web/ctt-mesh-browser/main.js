const { app, BrowserWindow, ipcMain, protocol } = require('electron');
const path = require('path');
const axios = require('axios');

const DAEMON_URL = 'http://localhost:8765';

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'icon.png'),
    title: 'CTT Mesh Browser',
    backgroundColor: '#0a0a0a'
  });

  mainWindow.loadFile('index.html');
  
  // Open DevTools in development
  // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers for mesh network operations
ipcMain.handle('mesh:status', async () => {
  try {
    const response = await axios.get(`${DAEMON_URL}/status`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('mesh:retrieve', async (event, contentHash) => {
  try {
    const response = await axios.get(`${DAEMON_URL}/retrieve/${contentHash}`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

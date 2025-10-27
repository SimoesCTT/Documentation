const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('meshAPI', {
  getStatus: () => ipcRenderer.invoke('mesh:status'),
  retrieveContent: (hash) => ipcRenderer.invoke('mesh:retrieve', hash)
});

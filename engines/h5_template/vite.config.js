import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import h5HotReload from './vite-plugin-h5-hot-reload.js'

export default defineConfig({
  plugins: [react(), h5HotReload()],
  resolve: {
    alias: [
      { find: '@', replacement: path.resolve(__dirname, 'src') },
    ]
  },
  server: {
    fs: {
      // 允许访问符号链接指向的外部目录
      allow: ['..', '../../', '../../../']
    }
  }
})

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
    // If you prefer proxying instead of hardcoding localhost:8000 in fetch:
    // proxy: {
    //   "/ask": {
    //     target: "http://localhost:8000",
    //     changeOrigin: true
    //   }
    // }
  }
});

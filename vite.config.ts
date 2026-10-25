import { defineConfig } from "vite-plus";

export default defineConfig({
  defaultPackage: "./app",
  fmt: {},
  lint: {
    plugins: ["typescript", "react"],
    options: {
      typeAware: true,
      typeCheck: true,
    },
  },
});

import { defineConfig } from "vite-plus";

export default defineConfig({
  defaultPackage: "./app",
  fmt: {},
  test: {
    include: ["app/src/**/*.test.ts"],
  },
  lint: {
    plugins: ["typescript", "react"],
    options: {
      typeAware: true,
      typeCheck: true,
    },
  },
});

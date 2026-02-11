const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: "/",
  outputDir: "../backend/app/static", // Optional: build directly to backend static
  assetsDir: "assets",
});

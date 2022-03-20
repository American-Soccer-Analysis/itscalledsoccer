module.exports = {
  env: {
    browser: true,
    es2021: true,
    "jest/globals": true,
    browser: true,
  },
  extends: ["eslint:recommended", "prettier"],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["jest"],
};

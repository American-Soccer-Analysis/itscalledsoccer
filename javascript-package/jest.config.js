module.exports = {
  setupFilesAfterEnv: ["./jest.setup.js"],
  coverageThreshold: {
    global: {
      branches: 90,
      statements: 90,
      functions: 90,
      lines: 90,
    },
  },
};

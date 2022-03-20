import pluralize from "../src/pluralize";

describe("pluralize", () => {
  test("stadium is stadia", () => {
    expect(pluralize("stadium")).toBe("stadia");
  });

  test("manager is managers", () => {
    expect(pluralize("manager")).toBe("managers");
  });

  test("team is teams", () => {
    expect(pluralize("team")).toBe("teams");
  });

  test("referee is referees", () => {
    expect(pluralize("referee")).toBe("referees");
  });
});

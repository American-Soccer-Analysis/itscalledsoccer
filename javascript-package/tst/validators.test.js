import {
  validateStringArray,
  validateUrlParameters,
  validateLeagues,
} from "../src/validators";

describe("validators", () => {
  beforeEach(() => {
    jest.spyOn(console, "assert").mockImplementation();
    jest.resetAllMocks();
  });
  it("asserts that numerical arrays are not string arrays", () => {
    const message = "foo";

    validateStringArray({ strings: [1234], message });

    expect(console.assert).toHaveBeenCalledWith(false, message);
  });

  it("asserts that strings are not string arrays", () => {
    const message = "bar";

    expect(() =>
      validateStringArray({ strings: "strings", message })
    ).toThrow();
    expect(console.assert).toHaveBeenCalledWith(false, message);
  });

  it("asserts that leagues is an array of leagues", () => {
    const leagues = ["la liga"];
    const message = `leagues must be an array of nwsl, mls, uslc, usl1, nasl, fetchEntity got ${leagues}`;

    validateLeagues({ leagues });

    expect(console.assert).toHaveBeenCalledWith(false, message);
  });

  it("asserts that url parameters are correct", () => {
    const providedArguments = { jordanMorris: 13, cristianRoldan: 7 };
    const validParameters = new Set(["jordanMorris"]);

    validateUrlParameters({ validParameters, providedArguments });

    expect(console.assert).toHaveBeenCalledWith(
      false,
      `Url parameters must be one of ${Array.from(
        validParameters.values()
      ).join(", ")}, got cristianRoldan`
    );
  });
});

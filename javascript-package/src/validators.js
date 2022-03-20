import { LEAGUES } from "./constants";

export const validateLeagues = ({ leagues }) => {
  console.assert(
    leagues.every((league) => Object.values(LEAGUES).includes(league)),
    `leagues must be an array of ${Object.values(LEAGUES).join(
      ", "
    )}, fetchEntity got ${leagues}`
  );
};

export const validateStringArray = ({ strings, message }) => {
  console.assert(Array.isArray(strings), message);
  console.assert(
    strings.every((string) => typeof string === "string"),
    message
  );
};

export const validateUrlParameters = ({
  validParameters,
  providedArguments,
}) => {
  Object.keys(providedArguments).forEach((arg) => {
    console.assert(
      validParameters.has(arg),
      `Url parameters must be one of ${Array.from(
        validParameters.values()
      ).join(", ")}, got ${arg}`
    );
  });
};

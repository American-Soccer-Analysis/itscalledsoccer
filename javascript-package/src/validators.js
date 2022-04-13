import { LEAGUES } from "./constants";
import { camelCase } from "change-case";

export const validateLeagues = ({ leagues }) => {
  console.assert(
    leagues.every((league) => Object.values(LEAGUES).includes(league)),
    `leagues must be an array of ${Object.values(LEAGUES).join(
      ", "
    )}, got ${leagues} instead`
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
        Array.from(validParameters.values()).map(camelCase)
      ).join(", ")}, got ${arg} instead`
    );
  });
};

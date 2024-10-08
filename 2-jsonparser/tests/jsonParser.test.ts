import { readFile } from "./utils";
import { test, expect, describe } from "@jest/globals";
import { JsonParser } from "../jsonParser";

describe("Test Cases for json parser", () => {
  let jsonParser: JsonParser;

  beforeEach(() => {
    jsonParser = new JsonParser();
  });

  describe("step1 tests", () => {
    const directory = "step1";

    test("parse empty json object", () => {
      const file = readFile(directory, "valid.json");
      expect(jsonParser.isJsonValid(file)).toBe(true);
    });

    test("parse invalid json object", () => {
      const file = readFile(directory, "invalid.json");
      expect(jsonParser.isJsonValid(file)).toBe(false);
    });

    test("parse a json object with empty strings behind and in front", () => {
      const jsonEmptyStrings = "         {}         ";

      expect(jsonParser.isJsonValid(jsonEmptyStrings)).toBe(true);
    });

    test("parse a json object with new lines in front and in behind and empty strings too", () => {
      const jsonEmptyStrings = " \n   \n   \n         {     \n \n   }         ";

      expect(jsonParser.isJsonValid(jsonEmptyStrings)).toBe(true);
    });

    test("parse a json object without a closing curly braces", () => {
      const jsonEmptyStrings =
        " \n   \n   \n         {     \n \n     **       ";

      expect(jsonParser.isJsonValid(jsonEmptyStrings)).toBe(false);
    });
  });

  describe("step 2 tests", () => {
    const directory = "step2";

    test("parse a json object with additional comma", () => {
      const file = readFile(directory, "invalid.json");
      expect(jsonParser.isJsonValid(file)).toBe(false);
    });

    test("parse a json object where the key has no quotes", () => {
      const file = readFile(directory, "invalid2.json");
      expect(jsonParser.isJsonValid(file)).toBe(false);
    });

    test("parse a json object with 2 key-value pair", () => {
      const file = readFile(directory, "valid2.json");
      expect(jsonParser.isJsonValid(file)).toBe(true);
    });

    test("parse a json object with a key-value pair", () => {
      const file = readFile(directory, "valid.json");
      expect(jsonParser.isJsonValid(file)).toBe(true);
    });

    test("parse a json object with key that has no quotes", () => {
      expect(jsonParser.isJsonValid(`{key: "value"}`)).toBe(false);
    });

    test("parse a json object with value that has no quotes", () => {
      expect(jsonParser.isJsonValid(`{"key": value}`)).toBe(false);
    });

    test("parse a json object with key that has 1 quote", () => {
      expect(jsonParser.isJsonValid(`{key: "value"}`)).toBe(false);
    });

    test("parse a json object with value that has 1 quote", () => {
      expect(jsonParser.isJsonValid(`{"key: "value"}`)).toBe(false);
    });

    test("parse a json object with no colon", () => {
      expect(jsonParser.isJsonValid(`{"key "value"}`)).toBe(false);
    });

    test("parse a json object with no comma", () => {
      expect(jsonParser.isJsonValid(`{"key: "value" "key2":"value"}`)).toBe(false);
    });
  });

  describe("step 3 tests", () => {
    const directory = "step3";

    test("parse a json object with correct boolean syntax", () => {
      const file = readFile(directory, "valid.json");
      expect(jsonParser.isJsonValid(file)).toBe(true);
    });

    test("parse a json object with incorrect boolean syntax", () => {
      const file = readFile(directory, "invalid.json");
      expect(jsonParser.isJsonValid(file)).toBe(false);
    });
  });

  describe("step 4 tests", () => {
    const directory = "step4";

    test("parse a json with objects, arrays, strings and numbers for the value", () => {
      const file = readFile(directory, "valid.json");
      expect(jsonParser.isJsonValid(file)).toBe(true);
    });

    test("parse a json object with an object with key-value pair inside and array also have values in it", () => {
      const file = readFile(directory, "valid2.json");
      expect(jsonParser.isJsonValid(file)).toBe(true);
    });

    test("parse a json object with incorrect string syntax in the array object", () => {
      const file = readFile(directory, "invalid.json");
      expect(jsonParser.isJsonValid(file)).toBe(false);
    });
  });
});

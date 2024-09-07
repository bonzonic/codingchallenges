import { parseJson } from "../jsonParser";
import { readFile } from "./utils";
import { test, expect, describe } from "@jest/globals";

describe("step 1 tests", () => {
  const directory = "step1";
  test("parse empty json object", () => {
    const file = readFile(directory, "valid.json");
    expect(parseJson(file)).toBe(0);
  });

  test("parse invalid json object", () => {
    const file = readFile(directory, "invalid.json");
    expect(parseJson(file)).toBe(1);
  });
});

// describe("step 2 tests", () => {
//   const directory = "step2";

//   test("parse a json object with additional comma", () => {
//     const file = readFile(directory, "invalid.json");
//     expect(parseJson(file)).toBe(1);
//   });

//   test("parse a json object where the key has no quotes", () => {
//     const file = readFile(directory, "invalid2.json");
//     expect(parseJson(file)).toBe(1);
//   });

//   test("parse a json object with 2 key-value pair", () => {
//     const file = readFile(directory, "valid2.json");
//     expect(parseJson(file)).toBe(0);
//   });

//   test("parse a json object with 1 key-value pair", () => {
//     const file = readFile(directory, "valid.json");
//     expect(parseJson(file)).toBe(0);
//   });
// });

// describe("step 3 tests", () => {
//   const directory = "step3";

//   test("parse a json object with correct boolean syntax", () => {
//     const file = readFile(directory, "valid.json");
//     expect(parseJson(file)).toBe(0);
//   });

//   test("parse a json object with incorrect boolean syntax", () => {
//     const file = readFile(directory, "invalid.json");
//     expect(parseJson(file)).toBe(1);
//   });
// });

// describe("step 4 tests", () => {
//   const directory = "step4";

//   test("parse a json with objects, arrays, strings and numbers for the value", () => {
//     const file = readFile(directory, "valid.json");
//     expect(parseJson(file)).toBe(0);
//   });

//   test("parse a json object with an object with key-value pair inside and array also have values in it", () => {
//     const file = readFile(directory, "valid2.json");
//     expect(parseJson(file)).toBe(0);
//   });

//   test("parse a json object with incorrect string syntax in the array object", () => {
//     const file = readFile(directory, "invalid.json");
//     expect(parseJson(file)).toBe(1);
//   });
// });

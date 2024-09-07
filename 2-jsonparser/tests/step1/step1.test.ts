import { parseJson } from "../../jsonParser";
import { readFile } from "../utils";
import { test, expect } from "@jest/globals";

test("parse empty json array", () => {
  const file = readFile("step1", "valid.json");
  expect(parseJson(file)).toBe(0);
});

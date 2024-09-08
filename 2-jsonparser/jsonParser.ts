import { readFile } from "./tests/utils";

/**
 * Checks if the json provided is valid or not valid
 * @param jsonString the json string
 * @returns true if the json is valid, else false
 */
export const isJsonValid = (jsonString: string): boolean => {
  if (jsonString.length === 0) return false;
  const stack = [];

  const splitJsonString = jsonString.split("\n");

  for (const line of splitJsonString) {
    const stripLine = line.trim();
    for (const character of stripLine) {
      if (character === "{") stack.push(character);
      else if (character === "}") stack.pop();
    }
  }
  return stack.length === 0;

  // // only 1 line
  // if (splitJsonString.length === 1) {
  //   const regexOneLiner = new RegExp('\\s*{\\s*(".*"\\s*:\\s*".*")?\\s*}\\s*');
  //   return regexOneLiner.test(jsonString);
  // }

  // const regex = new RegExp('{(".*":s?".*")?}');
  // return regex.test(jsonString);
};

const string = "\n\n\n{}";

console.log(isJsonValid(string));

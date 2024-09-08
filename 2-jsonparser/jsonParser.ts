import { readFile } from "./tests/utils";

/**
 * Parse the string and return the number of characters to skip
 * @param string parse the string in the json object
 */
const parseString = (jsonObject: string, index: number): number => {
  index = parseSpaceAndNewlines(jsonObject, index);
  let result = -1;
  for (let i = index; i < jsonObject.length; i++) {
    const character = jsonObject.charAt(i);
    if (character === '"') {
      result = i + 1;
      break;
    } else if (character === " ") {
    } else {
      break;
    }
  }
  const value = jsonObject.substring(result).search('"') + result;
  if (value === -1)
    throw new Error(`Something wrong in the string of key-value pair!`);

  return value + 1;
};

const parseSpaceAndNewlines = (jsonObject: string, index: number): number => {
  for (let i = index; i < jsonObject.length; i++) {
    const character = jsonObject.charAt(i);
    if (character === " " || character === "\n") {
    } else {
      return i;
    }
  }
};

const parseGeneralCharacters = (
  jsonObject: string,
  index: number,
  char: string
): number => {
  let result = -1;
  for (let i = index; i < jsonObject.length; i++) {
    const character = jsonObject.charAt(i);
    if (character === char) {
      result = i + 1;
      break;
    } else if (character === " " || character === "\n") {
    } else {
      console.log();
      throw new Error(
        `Found a weird character ${character} at index of ${index} while parsing ${char}`
      );
    }
  }
  if (result === -1) throw new Error(`Couldn't find the character ${char}`);
  return result;
};

const parseGeneralCharactersWithoutThrowingError = (
  jsonObject: string,
  index: number,
  char: string
): number => {
  let result = -1;
  for (let i = index; i < jsonObject.length; i++) {
    const character = jsonObject.charAt(i);
    if (character === char) {
      result = i + 1;
      break;
    } else if (character === " " || character === "\n") {
    } else {
      break;
    }
  }
  return result;
};

const parseLeftover = (jsonObject: string, index: number): boolean => {
  for (let i = index; i < jsonObject.length; i++) {
    const character = jsonObject.charAt(i);
    if (character !== " " && character !== "\n")
      throw new Error(
        `There's a leftover character ${character} with index ${i} after closing the curly brackets!`
      );
  }
  return true;
};

/**
 * Checks if the json provided is valid or not valid
 * @param jsonString the json string
 * @returns true if the json is valid, else false
 */
export const isJsonValid = (jsonString: string): boolean => {
  const stripLine = jsonString.trim();
  let result: number;

  try {
    result = parseGeneralCharacters(stripLine, 0, "{");
    // attempt to parse close curly bracket
    const parseCloseCurlyBracketResult =
      parseGeneralCharactersWithoutThrowingError(stripLine, result, "}");

    if (parseCloseCurlyBracketResult !== -1) {
      // have to check remaining leftover
      parseLeftover(stripLine, parseCloseCurlyBracketResult);
    } else {
      let commaResult = result;

      // parse key-value pairs
      while (commaResult !== -1) {
        result = commaResult;
        console.log(result);

        // parsing keys
        result = parseString(stripLine, result);

        // continue parsing for the colon
        result = parseGeneralCharacters(stripLine, result, ":");

        // parsing the value
        result = parseString(stripLine, result);

        // parsing the comma
        commaResult = parseGeneralCharactersWithoutThrowingError(
          stripLine,
          result,
          ","
        );
      }

      // parse closing curly bracket
      const finalClosingCurlyBracket =
        parseGeneralCharactersWithoutThrowingError(stripLine, result, "}");

      if (finalClosingCurlyBracket !== -1) {
        // have to check remaining leftover
        parseLeftover(stripLine, finalClosingCurlyBracket);
      } else {
        throw new Error("No curly bracket found!!");
      }
    }
    return true;
  } catch (e) {
    console.log(e.message);
    return false;
  }
};

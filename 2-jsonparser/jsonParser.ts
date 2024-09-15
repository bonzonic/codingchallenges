/**
 * Todo: add comments on functions
 */

export class JsonParser {
  private jsonString: string = "";
  private index: number = 0;
  private result: boolean = true;
  private line: number = 0; // for debugging purposes

  private getIndexAndLine = (): string => {
    return `at index ${this.index} at line ${this.line}`;
  };

  /**
   * Parse the string and return the number of characters to skip
   * @param string parse the string in the json object
   */
  private parseString = () => {
    const character = this.jsonString.charAt(this.index);
    if (character === '"') {
      this.index += 1;
    } else {
      throw new Error(
        `First " of the key cannot be found ${this.getIndexAndLine()}`
      );
    }

    const value =
      this.jsonString.substring(this.index).search('"') + this.index;
    if (value === -1)
      throw new Error(
        `Second " of the key cannot be found ${this.getIndexAndLine()}`
      );
    this.index = value + 1;
  };

  private parseSpaceAndNewlines = () => {
    for (let i = this.index; i < this.jsonString.length; i++) {
      const character = this.jsonString.charAt(i);
      if (character === "\n") this.line += 1;
      else if (character === " ") {
      } else {
        this.index = i;
        break;
      }
    }
  };

  // parse value
  private parseCharacters = (word: string, optional: boolean = false) => {
    let result = true;
    for (let i = 0; i < word.length; i++) {
      const character = word.charAt(i);
      if (this.jsonString.charAt(i + this.index) !== character) {
        if (optional) result = false;
        else throw new Error(`parsing ${word} error ${this.getIndexAndLine()}`);
      }
    }
    if (result) this.index += word.length;
    return result;
  };

  // parse number
  private parseNumber = () => {
    for (this.index; this.index < this.jsonString.length; this.index++) {
      const character = this.jsonString.charAt(this.index);
      if (character >= "0" && character <= "9") {
      } else {
        break;
      }
    }
  };

  private parseArray = () => {
    this.parseCharacters("[");
    let commaExists = true;

    // attempt to parse close square bracket
    this.parseSpaceAndNewlines();
    let closeSquareBracketExist = this.parseCharacters("]", true);

    if (!closeSquareBracketExist) {
      // parse elements inside the array

      while (commaExists) {
        // parsing the value
        this.parseValue();

        // parsing the comma
        commaExists = this.parseCharacters(",", true);
      }
      // parse closing square bracket
      closeSquareBracketExist = this.parseCharacters("]", true);

      if (!closeSquareBracketExist) {
        throw new Error(
          `No closing square bracket found ${this.getIndexAndLine()}`
        );
      }
    }
  };

  private parseValue = () => {
    this.parseSpaceAndNewlines();

    const nextCharacter = this.jsonString.charAt(this.index);
    const regexNumber = new RegExp("\\d");

    // if the value is a string
    if (nextCharacter === '"') {
      this.parseString();
    }

    // if the value is a null
    else if (nextCharacter === "n") {
      this.parseCharacters("null");
    }

    // if the value is a boolean true
    else if (nextCharacter === "t") {
      this.parseCharacters("true");
    }

    // if the value is a false
    else if (nextCharacter === "f") {
      this.parseCharacters("false");
    }

    // if the value is a number
    else if (regexNumber.test(nextCharacter)) {
      this.parseNumber();
    }

    // if the value is a json object
    else if (nextCharacter === "{") {
      this.result = this.parseJson(true) && this.result;
    }

    // if the value is a array object
    else if (nextCharacter === "[") {
      this.parseArray();
    }

    // other values that should not exist in a json value
    else {
      throw new Error(
        `The value ${nextCharacter} ${this.getIndexAndLine()} is not a valid format!`
      );
    }
  };

  private parseLeftover = () => {
    for (let i = this.index; i < this.jsonString.length; i++) {
      const character = this.jsonString.charAt(i);
      if (character !== " " && character !== "\n")
        throw new Error(
          `There's a leftover character ${character} ${this.getIndexAndLine()} after closing the curly brackets!`
        );
    }
  };

  private parseJson = (isJsonValue: boolean = false): boolean => {
    let commaExist = true;
    this.parseCharacters("{");

    // attempt to parse close curly bracket
    this.parseSpaceAndNewlines();
    let closeCurlyBracketExist = this.parseCharacters("}", true);

    if (closeCurlyBracketExist) {
      // have to check remaining leftover
      if (!isJsonValue) this.parseLeftover();
    } else {
      // parse key-value pairs
      while (commaExist) {
        // parsing keys
        this.parseSpaceAndNewlines();
        this.parseString();

        // continue parsing for the colon
        this.parseSpaceAndNewlines();
        this.parseCharacters(":");

        // parsing the value
        this.parseValue();

        // parsing the comma
        this.parseSpaceAndNewlines();
        commaExist = this.parseCharacters(",", true);
      }

      // parse closing curly bracket
      this.parseSpaceAndNewlines();
      closeCurlyBracketExist = this.parseCharacters("}", true);

      if (closeCurlyBracketExist) {
        // have to check remaining leftover
        if (!isJsonValue) this.parseLeftover();
      } else {
        throw new Error(
          `No closing curly bracket found ${this.getIndexAndLine()}`
        );
      }
    }
    return true;
  };

  /**
   * Checks if the json provided is valid or not valid
   * @param jsonString the json string
   * @returns true if the json is valid, else false
   */
  isJsonValid = (jsonString: string): boolean => {
    this.jsonString = jsonString.trim();

    try {
      this.parseSpaceAndNewlines();
      this.parseJson();
    } catch (e) {
      console.log(e.message);
      return false;
    }
    return this.result;
  };
}

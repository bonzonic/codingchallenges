export class JsonParser {
  private jsonString: string = "";
  private index: number = 0;

  /**
   * Parse the string and return the number of characters to skip
   * @param string parse the string in the json object
   */
  private parseString = () => {
    const character = this.jsonString.charAt(this.index);
    if (character === '"') {
      this.index += 1;
    } else {
      throw new Error(`First " of the key cannot be found!`);
    }

    const value =
      this.jsonString.substring(this.index).search('"') + this.index;
    if (value === -1) throw new Error(`Second " of the key cannot be found!`);
    this.index = value + 1;
  };

  private parseSpaceAndNewlines = () => {
    for (let i = this.index; i < this.jsonString.length; i++) {
      const character = this.jsonString.charAt(i);
      if (character === " " || character === "\n") {
      } else {
        this.index = i;
        break;
      }
    }
  };

  // parse value
  private parseCharacters = (word: string) => {
    for (let i = 0; i < word.length; i++) {
      const character = word.charAt(i);
      if (this.jsonString.charAt(i + this.index) !== character) {
        throw new Error("parsing null error!");
      }
    }
    this.index += word.length;
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

    // other values that should not exist in a json value
    else {
      throw new Error(
        `The value ${nextCharacter} at index of ${this.index} is not a valid format!`
      );
    }
  };

  private parseGeneralCharactersWithoutThrowingError = (
    char: string
  ): number => {
    let result = -1;
    for (let i = this.index; i < this.jsonString.length; i++) {
      const character = this.jsonString.charAt(i);
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

  private parseLeftover = () => {
    for (let i = this.index; i < this.jsonString.length; i++) {
      const character = this.jsonString.charAt(i);
      if (character !== " " && character !== "\n")
        throw new Error(
          `There's a leftover character ${character} with index ${i} after closing the curly brackets!`
        );
    }
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
      this.parseCharacters("{");

      // attempt to parse close curly bracket
      let result = this.parseGeneralCharactersWithoutThrowingError("}");

      if (result !== -1) {
        this.index = result;
        // have to check remaining leftover
        this.parseLeftover();
      } else {
        let commaResult = this.index;

        // parse key-value pairs
        while (commaResult !== -1) {
          this.index = commaResult;

          // parsing keys
          this.parseSpaceAndNewlines();
          this.parseString();

          // continue parsing for the colon
          this.parseSpaceAndNewlines();
          this.parseCharacters(":");

          // parsing the value
          this.parseValue();

          // parsing the comma
          commaResult = this.parseGeneralCharactersWithoutThrowingError(",");
        }
        // parse closing curly bracket
        this.index = this.parseGeneralCharactersWithoutThrowingError("}");

        if (this.index !== -1) {
          // have to check remaining leftover
          this.parseLeftover();
        } else {
          throw new Error("No closing curly bracket found!!");
        }
      }
      return true;
    } catch (e) {
      console.log(e.message);
      return false;
    }
  };
}

// const jsonParser = new JsonParser();

// console.log(jsonParser.isJsonValid(`{\n"key": "value",\n"key2": "value"\n}`));
// console.log(
//   jsonParser.isJsonValid(" \n   \n   \n         {     \n \n   }         ")
// );
// console.log(jsonParser.isJsonValid(`{"key": "value"}`))

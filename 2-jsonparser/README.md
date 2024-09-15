# Json Parser
Our version of JSON Parser  
Challenge: https://codingchallenges.fyi/challenges/challenge-json-parser 

# Functionalities
It returns true if the Json is valid, else false. If it returns false, it will also print out a useful message to indicate the error in the json string.

# How To Use
1. Clone the repo and go to the directory by executing the code below in the terminal.
```
cd 2-jsonparser
```
2. In the jsonParser.ts file, write the following command
```
const jsonParser = new JsonParser()
console.log(jsonParser.isJsonValid("<Your Json String here>"))
```
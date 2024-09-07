import * as fs from "fs";

export const readFile = (directory: string, fileName: string): string => {
  const file = fs.readFileSync(`tests/${directory}/${fileName}`, "utf8");
  return file;
};

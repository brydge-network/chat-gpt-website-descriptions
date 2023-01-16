
const { version } = require("../package.json");
const tokens = require("./data/tokens.json");
const gas = require("./data/gas.json");

module.exports = function buildList() {
  const parsed = version.split(".");
  return {
    name: "Brydge Network Website Data",
    timestamp: new Date().toISOString(),
    version: {
      major: +parsed[0],
      minor: +parsed[1],
      patch: +parsed[2],
    },
    tags: {},
    logoURI: "https://avatars.githubusercontent.com/u/91710361",
    keywords: ["brydge", "default"],
    data: {
      "tokens": [...tokens].sort((t1, t2) => {
      if (t1.token.toLowerCase() === t2.token.toLowerCase()) {
        return t1.chainId < t2.chainId ? -1 : 1;
      }
      return t1.token.toLowerCase() < t2.token.toLowerCase() ? -1 : 1;
    }),
      "gas": [...gas].sort((t1, t2) => {
      if (t1.token.toLowerCase() === t2.token.toLowerCase()) {
        return t1.chainId < t2.chainId ? -1 : 1;
      }
      return t1.token.toLowerCase() < t2.token.toLowerCase() ? -1 : 1;
    })}
  };
};

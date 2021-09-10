module.exports = function (eleventyConfig) {
  eleventyConfig.setTemplateFormats([
    "njk",
    "ts",
    "css"
  ]);

  return {
    dir: {
      input: "src",
      output: "_site"
    }
  };
};

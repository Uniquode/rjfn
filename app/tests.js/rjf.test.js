const rjf = require('../static/site/scripts/rjf.js');

describe('slugify', () => {
  it('should correctly slugify a string', () => {
    const string = 'This is   an "Example String" <>';
    const expected = 'this-is-an-example-string';
    let result = rjf.slugify(string);

    expect(result).toEqual(expected);
  })

  it('should correctly truncate the slugified string given a maxlength', () => {
    // maximum length
    const string = 'This is   an even longer "Example String" that must not exceed 62 characters';
    const expected = 'this-is-an-even-longer-example-string-that-must-not-exceed-62';
    const result = rjf.slugify(string, 62);

    expect(result).toEqual(expected);
  });
});

/**
 * slugify an input string
 * @param {string} str - string to transform
 * @param {number} maxlength - optional maximum string length
 * @returns {string}
 */
export const slugify = (str, maxlength=0) => {
  str = str.replace(/^\s+|\s+$/g, ''); // trim
  str = str.toLowerCase();

  // remove accents, swap ñ for n, etc
  const __fm = "àáãäâèéëêìíïîòóöôùúüûñç·/_,:;";
  const __to   = "aaaaaeeeeiiiioooouuuunc------";
  for (let i=0 ; i < __fm.length ; i++) {
      str = str.replace(new RegExp(__fm.charAt(i), 'g'), __to.charAt(i));
  }

  str = str.replace(/[^a-z0-9 -]/g, ''); // remove invalid chars
  str = str.replace(/\s+/g, '-'); // collapse whitespace and replace by -
  str = str.replace(/-+/g, '-');  // collapse dashes
  str = maxlength > 0 ? str.substr(0, maxlength) : str;
  str = str.replace(/^-|-$/g, ''); // trim leading/trailing dashes

  return str;
}

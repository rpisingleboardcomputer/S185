
// S185 - Introduction to Single-Board Computers
// Pi Day activity  :-)

// A .json script that will display the Raspberry Pi's logo
//   and the number pi together as ascii art.

//Execution:
// 1. Set the executable flag on the script: chmod u+x index.js
// 2. node index.js image_file_name.extension

// Sources:
// https://www.npmjs.com/package/pi-number
// https://www.npmjs.com/package/image-to-ascii
// https://www.npmjs.com/package/asciify-pixel-matrix

// Require the needed dependencies:
// (1) 'pi' will be used to return the first `n` decimals of pi.
const pi = require("pi")

      // (2) 'image-to-ascii' for displaying the images in the terminal.
    , img = require("image-to-ascii")

      // (3) 'asciify-pixel-matrix' to stringify the pixel matrix after
      // modifying the internal data (basically, the characters).
    , stringify = require("asciify-pixel-matrix")
    ;

// Take the image path from the command line argument(s).
img(process.argv[2], {
    // We turn off the stringify-ing, since we really want to do
    // some changes before displaying the images.
    stringify: false
  , concat: false
}, (err, converted) => {
    // Handle the errors.
    if (err) { return console.error(err); }

    // 'converted' is an array of arrays (in fact, a matrix of pixels).
    // We use the 'converted' matrix to know how many decimals we
    // need: width x height
    // 'piNumber' will be a string in this format: "3.141592...." (with a
    // lot of decimal places!).
    var piNumber = pi(converted.length * converted[0].length);

    // We will use this 'i' variable to get the current index.
    var i = -1;

    // For each row in the matrix.
    converted.forEach(cRow => {
        // ...and for each pixel in the row.
        cRow.forEach(px => {
            // ...update the character using a pi decimal, in order.
            px.char = piNumber[i = ++i % piNumber.length];
        });
    });

    // Finally, stringify everything and display the result! :-)!
    console.log(stringify.stringifyMatrix(converted));
});

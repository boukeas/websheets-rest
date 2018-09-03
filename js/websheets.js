'use strict';

// start processing when the readyState has been reached
document.addEventListener('readystatechange', function() {
    if (document.readyState == 'complete') process();
});

// high-level processing function: it is called when the readyState is reached
// and it delegates processing to functions that handle specific tasks
function process() {
  
}

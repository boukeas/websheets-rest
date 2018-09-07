'use strict';

// start processing when the readyState has been reached
document.addEventListener('readystatechange', function() {
    if (document.readyState == 'complete') process();
});

// high-level processing function: it is called when the readyState is reached
// and it delegates processing to functions that handle specific tasks
function process() {
    PR.prettyPrint();
}



/*

// add this to function process()
// addGroupButtons(document.querySelectorAll('div.explanation-group'), 'explanation');

function addGroupButtons(groups, name) {
  for (let group of groups) {
    hideAll(group.children);
    // create div for the buttons
    let buttons = document.createElement('div');
    buttons.classList.add(name + '-group-buttons');
    // add to generic 'group-buttons' class
    buttons.classList.add('group-buttons');
    buttons.active = null;
    let buttonCounters = {};
    let element = group.firstElementChild;
    while (element) {
        // create button
        let button = document.createElement('button');
        button.className = 'group-button ' + name + '-button';
        buttons.appendChild(button);
        // link to element
        button.element = element;
        element.button = button;
        // button content taken from element title
        button.innerHTML = element.firstElementChild.innerHTML;
        element.firstElementChild.remove();

        // if (element.classList.contains('active')) {
        //     element.classList.remove('active');
        //    buttonActivate(button);
        // }
        // button.counter = buttonCounters[buttonType];

        // click event
        button.onclick = buttonToggle;
        element = element.nextElementSibling;
    }
    // place the buttons before the group
    group.insertBefore(buttons, group.firstElementChild);
  }
}

////// simple generic functions for hiding or revealing elements

Node.prototype.hide = function() {
    // hide the element
    this.setAttribute('disabled','true');
}

Node.prototype.show = function() {
    // show the element
    this.removeAttribute('disabled');
}

function hideAll(elements) {
    // hide all elements
    for (let element of elements) element.hide();
}

function showSingle(elements, index) {
    // show only a single element, specified by index
    hideAll(elements);
    elements[index].show();
}

//// event handling for group buttons

// generic element activation and deactivation functions
// using the 'active' attribute (not the 'active' class)

function isActive(element) {
  // return element.classList.contains('active')
  return element.hasAttribute('active');
}

function activate(element) {
  // element.classList.add('active');
  element.setAttribute('active', 'true');
}

function deactivate(element) {
  // element.classList.remove('active');
  element.removeAttribute('active');
}

// group button activation and deactivation

function deactivateButton(btn) {
    deactivate(btn);
    btn.element.hide();
    btn.parentNode.active = null;
}

function activateButton(btn) {
    // check for other currently active element and deactivate
    if (btn.parentNode.active) deactivateButton(btn.parentNode.active);
    // activate button
    activate(btn);
    btn.element.show();
    btn.parentNode.active = btn;
}

function buttonToggle() {
    if (isActive(this)) {
        // clicked on active element » deactivate
        deactivateButton(this);
    } else {
        // clicked on inactive element » activate
        activateButton(this);
    }
}
*/

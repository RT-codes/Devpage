var consoleWindow = false;

jQuery(document).ready(function($) {
  //  little function to make the header collapse on scroll
  $(window).on("scroll", function() {
    if ($(window).scrollTop() < $("#top-spacer").offset().top) {
      $("#header").removeClass("header-glass");
    }
  });

  $(window).on("scroll", function() {
    if ($(window).scrollTop() > $("#top-spacer").offset().top) {
      $("#header").addClass("header-glass");
    }
  });

  // when spacebar is pressed run a console toggle function
  $(document).on("keypress", function(e) {
    if (e.keyCode == 32) {
      console.log("spacebar pressed");
      // start the console builder
      consoleToggle();
    }
  });

  // when the page is loaded look for an element with the id of "typewriter-effect"
  let typewriterHero = document.getElementById("typewriter-effect");
  let IntroWords = ["Designer.", "Creator.", "Problem Solver.", "Learner.", "blogger."];
  console.log(typewriterHero);
  if (typewriterHero) {
    typewriter(typewriterHero, "Developer.");
    // wait 1 second then run the typewriter manager function
    setTimeout(function() {
      typewriterManager(typewriterHero, IntroWords);
    }, 1000);
  }
});

// make a typewriter manager function that takes an element and a list of strings
// the function will then type out the strings in the list by looping through them and calling the typewriter function and passing it the element and the string

function typewriterManager(el, strings) {
  // set the counter to 0
  var counter = 0;
  // set the length of the strings array
  var stringsLength = strings.length;
  console.log(stringsLength);
  // set an interval variable so it can be adjusted, then run a loop that will run the typewriter function forever until the counter is equal to the length of the strings array then it will reset the counter to 0
  // the interval will be set to 5 seconds and use this to call the typewriter function and pass it the element and the string
  var intervalDelay = 3000;
  // every intervalDelay seconds run the typewriter function
  var wordLoop = setInterval(function() {
    // toggle a class on the element called "typewriter"
    // el.classList.removeClass("typewriter");

    // if the counter is less than the length of the strings array
    if (counter < stringsLength) {
      // run the typewriter function
      typewriter(el, strings[counter]);
      // increment the counter
      counter++;
    } else {
      // reset the counter to 0
      counter = 0;
      el.classList.toggle("typewriter");
      el.classList.toggle("typewriter-blink");
    }
  }, intervalDelay);
}

function typewriter(textEl, text) {
  // set the text in textEl to an empty string
  textEl.innerHTML = "";
  // set the length of the text
  var textLength = text.length;
  // set the counter to 0
  var counter = 0;
  // set the interval delay to 100ms
  var intervalDelay = 150;
  // set the interval variable
  // set the interval to run every intervalDelay ms
  var writer = setInterval(function() {
    // if the counter is less than the length of the text
    if (counter < textLength) {
      // add the next character to the textEl
      textEl.innerHTML += text.charAt(counter);
      // increment the counter
      counter++;
    } else {
      // clear the interval
      clearInterval(writer);
    }
  }, intervalDelay);
}

function consoleToggle() {
  if (consoleWindow) {
    consoleWindow = false;
    document.body.removeChild(document.getElementById("console-container"));
  } else {
    consoleWindow = true;
    var consoleContainer = document.createElement("div");
    consoleContainer.id = "console-container";
    consoleContainer.style.cssText = "display: flex; justify-content: center; align-items: center; position: fixed; bottom: 0; left: 0; width: 100%; height: 5rem; background-color: black; z-index: 9999;";
    consoleContainer.innerHTML = "Press spacebar to close";
    document.body.appendChild(consoleContainer);
  }
}

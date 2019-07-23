const arrEqual = (arr1, arr2) => { //returns true if arr1 and arr2 have the same elements.
  if (arr1.length != arr2.length) {
    return false;
  }
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] != arr2[i]) {
      return false;
    }
  }
  return true;
}

let subscribed = false;
let liked = false;
//easter eggs
const konami = ["ArrowUp", "ArrowUp", "ArrowDown", "ArrowDown", "ArrowLeft", "ArrowRight", "ArrowLeft", "ArrowRight", "KeyA", "KeyB"];
const konamiCheck = [];
const penguin = ["KeyP", "KeyE", "KeyN", "KeyG", "KeyU", "KeyI", "KeyN"];
const penguinCheck = [];

//activate correct header button
const topNavBtn = document.getElementById("index.html");
topNavBtn.className = "active";

const alertButton = document.querySelector("#alertButton");
alertButton.addEventListener("click", (event) => {
  alert("Get Alerted by the Event Listener!");
});

const pikachuMeme = document.querySelector("#pikachuMeme");
pikachuMeme.addEventListener("click", (event) => {
  alert("Don't click my pikachu");
  pikachuMeme.style.transform = "scale(2x)";
});

//like button event listeners
const likeButton = document.querySelector("#likeButton");
likeButton.addEventListener("click", (event) => {
  likeButton.innerHTML = "Liked!";
  likeButton.style.backgroundColor = "green";
  liked = true;
});

likeButton.addEventListener("mouseover", (e) => {
  if (liked) return;
  likeButton.style.backgroundColor = "lightgreen";
});

likeButton.addEventListener("mouseout", (e) => {
  if (liked) return;
  likeButton.style.backgroundColor = "white";

});
//subscribe button event listeners
//-------------------------
const subscribeButton = document.querySelector("#subscribeButton");
subscribeButton.addEventListener("click", (event) => {
  subscribeButton.innerHTML = "Subscribed!";
  subscribeButton.style.backgroundColor = "green";
  subscribed = true;
});

subscribeButton.addEventListener("mouseover", (e) => {
  if (subscribed) return;
  subscribeButton.style.backgroundColor = "lightgreen";
});

subscribeButton.addEventListener("mouseout", (e) => {
  if (subscribed) return;
  subscribeButton.style.backgroundColor = "white";

});
//END subscribe button event listeners

//make the title random color when clicked
const mainTitle = document.querySelector("#mainTitle");
mainTitle.addEventListener("click", (e) => {
  mainTitle.style.color = `rgb(${Math.random()*256},${Math.random()*256},${Math.random()*256})`;
  //make all the h2's change colors too
  const h2s = document.querySelectorAll("h2");
  h2s.forEach((h2Obj) => {
    h2Obj.style.color = mainTitle.style.color;
  })
});


//secret Konami Code ;o
const checkKonami = (e) => {
  konamiCheck.push(e.code);
  if (konamiCheck.length > 10) {
    konamiCheck.shift(); //removes the first elem of array
  }
  if (arrEqual(konami, konamiCheck)) { //KONAMI CODE ENTERED :OO
    //mainTitle.style.color = "red";
    const easterEggPikachu = document.querySelector("#easterEggPikachu");
    easterEggPikachu.style.height = "100%";
    easterEggPikachu.style.width = "100%";
    easterEggPikachu.style.display = "block"; //make it visible

    //frogger!
    setTimeout(() => {
      window.location.href = "frogger.html";
    }, 500);
  }
  //console.log(konamiCheck);
}; //end check Konami/
//penguin easter egg
const checkPenguin = (e) => {
  penguinCheck.push(e.code);
  if (penguinCheck.length > 7) {
    penguinCheck.shift();
  }
  if (arrEqual(penguin, penguinCheck)) {
    const easterEggPenguin = document.querySelector("#easterEggPenguin");
    easterEggPenguin.style.height = "100%";
    easterEggPenguin.style.width = "100%";
    easterEggPenguin.style.display = "block"; //make it visible
  }
};
const body = document.querySelector("body");
window.addEventListener("keydown", (e) => {
  checkKonami(e);
  checkPenguin(e);

});





//JS Includes from w3 schools
/* DOESNT WORK ON LOCAL FILES BC SECURITY ISSUES
function includeHTML() {
  var z, i, elmnt, file, xhttp;
  // Loop through a collection of all HTML elements:
  z = document.getElementsByTagName("*");
  for (i = 0; i < z.length; i++) {
    elmnt = z[i];
    //search for elements with a certain atrribute:
    file = elmnt.getAttribute("w3-include-html");
    if (file) {
      // Make an HTTP request using the attribute value as the file name:
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          if (this.status == 200) {elmnt.innerHTML = this.responseText;}
          if (this.status == 404) {elmnt.innerHTML = "Page not found.";}
          // Remove the attribute, and call this function once more:
          elmnt.removeAttribute("w3-include-html");
          includeHTML();
        }
      }
      xhttp.open("GET", file, true);
      xhttp.send();
      // Exit the function:
      return;
    }
  }
}
*/

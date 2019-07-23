// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

let currentlily = 1;
//bools that control direction of lilypad animation
let down2 = true;
let down3 = false;
let down4 = false;
let lost = false;

//
const frogger = document.querySelector("#frog"); /* Use a querySelector to grab your frog from your HTML */;
frog.style.left = "17%";//why does this happen

const lp2 = document.querySelector("#lilypad2");
const lp3 = document.querySelector("#lilypad3");
const lp4 = document.querySelector("#lilypad4");
const lp5 = document.querySelector("#lilypad5");

lp2.style.top = 20 + Math.random()*60 + "%";
lp3.style.top = 20 + Math.random()*60 + "%";
lp4.style.top = 20 + Math.random()*60 + "%";
lp5.style.top = "50%";

//DEBUG PLACE
console.log(document.querySelector("#lilypad2").offsetTop);

const vertMoveByPercent = (DOMobj, percent) => {
  let pos = parseFloat(DOMobj.style.top);
  DOMobj.style.top = pos + percent + "%";
};


const checkAndCorrectDirection = (bool, lilypadObj) =>{
  if(bool && parseFloat(lilypadObj.style.top) > 75){
    return false;
  }
  if(!bool && parseFloat(lilypadObj.style.top) <25){
    return true;
  }
  return bool;
};


const animate = () =>{

  vertMoveByPercent(lp2,(down2 ? 4*2 : -.18*2));
  vertMoveByPercent(lp3,(down3 ? .4*2 : -.3*2));
  vertMoveByPercent(lp4,(down4 ? .7*2 : -1*2));

  down2 = checkAndCorrectDirection(down2, lp2);
  down3 = checkAndCorrectDirection(down3, lp3);
  down4 = checkAndCorrectDirection(down4, lp4);

  //allign frog to the correct lily_pad
  if(!lost){
    switch(currentlily){
      case 2:
        frog.style.top = lp2.style.top;
        break;
      case 3:
        frog.style.top = lp3.style.top;
        break;
      case 4:
        frog.style.top = lp4.style.top;
        break;
      case 5:
        frog.style.top = lp5.style.top;
        if(currentlily === 5 && !lost){
          lost = true; //just to stop game
          alert("You win!");
        }
        break;
      default:
    }
  }//if !lost

};

setInterval(animate, 10);

const changeActiveLily = () => {
  let oldLily = document.querySelector("#lilypad" + (currentlily-1));
  //console.log(oldLily);
  let newLily = document.querySelector("#lilypad" + currentlily);
  oldLily.className = "lilypad";
  newLily.className = "lilypad active";
  //check if the jump is in range
  if(Math.abs(parseFloat(oldLily.style.top) - parseFloat(newLily.style.top)) > 8){
    //invalid jump
    frogger.style.filter = "grayscale(100%)";
    lost = true;
    alert("RIP froggo");
  }
}
const jumpFrogEvent = (e) => {
    if(!lost){//turn off if lost
      console.log(frog.style.left);

      let posX = parseFloat(frog.style.left);

      frog.style.left = posX + 16.5 + "%";
      console.log("click");
      currentlily++;
      changeActiveLily();

    }

};




frogger.addEventListener("click", jumpFrogEvent);

const body = document.querySelector("body");
body.addEventListener("keypress", jumpFrogEvent);

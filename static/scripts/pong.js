let p1UpInterval = null;
let p2UpInterval = null;
let p1DownInterval = null;
let p2DownInterval = null;

const refreshTime = 10; //refresh time in ms

function hitTest(a, b){
  let compStyA = window.getComputedStyle(a);
  let compStyB = window.getComputedStyle(b);
  a.y = parseFloat(compStyA.getPropertyValue("top"));
  a.height = parseFloat(compStyA.getPropertyValue("height"));
  a.x = parseFloat(compStyA.getPropertyValue("left"));
  a.width = parseFloat(compStyA.getPropertyValue("width"));

  b.y = parseFloat(compStyB.getPropertyValue("top"));
  b.height = parseFloat(compStyB.getPropertyValue("height"));
  b.x = parseFloat(compStyB.getPropertyValue("left"));
  b.width = parseFloat(compStyB.getPropertyValue("width"));

  // console.log(a.y);
  // console.log(a.height);
  // console.log(a.x);
  // console.log(a.width);
  //
  // console.log(b.y);
  // console.log(b.height);
  // console.log(b.x);
  // console.log(b.width);
  return !(
      ((a.y + a.height) < (b.y)) ||
      (a.y > (b.y + b.height)) ||
      ((a.x + a.width) < b.x) ||
      (a.x > (b.x + b.width))
  );
}
//activate correct header button
const topNavBtn = document.getElementById("pong.html");
topNavBtn.className = "active";

const gameBoard = document.getElementById("gameBoard");
const compStyleBoard = window.getComputedStyle(gameBoard);
//player movement control
const player1 = document.getElementById("player1");
const player2 = document.getElementById("player2");

function movePlayer(e,playerElem){
  //console.log("movePlayer1 running");
  const compStylePlayer = window.getComputedStyle(playerElem);

  let topPos = compStylePlayer.getPropertyValue("top");//returns in px
  let boardHeight = parseFloat(compStyleBoard.getPropertyValue("height"));

  let playerHeight = parseFloat(compStylePlayer.getPropertyValue("height"));
  //console.log(player1.style.top);
  //console.log(topPos);
  topPos = parseFloat(topPos);
  if(e.code === "KeyW" && topPos > 0){//move up
    topPos -= 8;
  }
  else if(e.code === "KeyS" && topPos < boardHeight - playerHeight){
    topPos += 8;
  }
  //for player 2
  if(e.code === "KeyI" && topPos > 0){//move up
    topPos -= 8;
  }
  else if(e.code === "KeyK" && topPos < boardHeight - playerHeight){
    topPos += 8;
  }
  playerElem.style.top = topPos + "px";
}
//move player with intervals
function animatePlayer(direction, playerElem){
  //console.log("movePlayer1 running");
  const compStylePlayer = window.getComputedStyle(playerElem);

  let topPos = compStylePlayer.getPropertyValue("top");//returns in px
  let boardHeight = parseFloat(compStyleBoard.getPropertyValue("height"));

  let playerHeight = parseFloat(compStylePlayer.getPropertyValue("height"));
  //console.log(player1.style.top);
  //console.log(topPos);
  topPos = parseFloat(topPos);
  if(direction.toLowerCase() === "up" && topPos > 0){//move up
    topPos -= 3;
  }
  else if(topPos < boardHeight - playerHeight){//assume down
    topPos += 3;
  }

  playerElem.style.top = topPos + "px";
}


//window event listener for button presses
window.addEventListener("keydown", (e) => {
  //console.log("window keydown event listener fired");
  //console.log(e.code);
  // if(e.code === "KeyW" || e.code === "KeyS"){
  //   movePlayer(e,player1);
  // }
  // if(e.code === "KeyI" || e.code === "KeyK"){
  //   movePlayer(e,player2);
  // }
  //player 1 animation
  if(e.code === "KeyW" && !p1UpInterval){
    if(p1DownInterval){
      clearInterval(p1DownInterval);
      p1DownInterval=null;
    }
    p1UpInterval = setInterval(() => {animatePlayer("up",player1);},refreshTime);
  }
  else if(e.code === "KeyS" &&!p1DownInterval){
    if(p1UpInterval){
      clearInterval(p1UpInterval);
      p1UpInterval=null;
    }
    p1DownInterval = setInterval(() => {animatePlayer("down",player1);},refreshTime);
  }

  //player 2 animation

  if(e.code === "KeyI"&&!p2UpInterval){
    if(p2DownInterval){
      clearInterval(p2DownInterval);
      p2DownInterval=null;
    }
    p2UpInterval = setInterval(() => {animatePlayer("up",player2);},refreshTime);
  }
  else if(e.code === "KeyK"&&!p2DownInterval){
    if(p2UpInterval){
      clearInterval(p2UpInterval);
      p2UpInterval=null;
    }
    p2DownInterval = setInterval(() => {animatePlayer("down",player2);},refreshTime);
  }


});

window.addEventListener("keyup", (e) =>{
  if(e.code === "KeyW"){
    clearInterval(p1UpInterval);
    p1UpInterval = null;
    return;
  }
  if(e.code === "KeyS"){
    clearInterval(p1DownInterval);
    p1DownInterval = null;
    return;
  }
  if(e.code === "KeyI"){
    clearInterval(p2UpInterval);
    p2UpInterval = null;
    return;
  }
  if(e.code === "KeyK"){
    clearInterval(p2DownInterval);
    p2DownInterval = null;
    return;
  }

});

let ballVelX = 4;
let ballVelY = .1;
const ball = document.getElementById("ball");
const compStyleBall = window.getComputedStyle(ball);
const animateBall = () =>{
  let ballHeight = parseFloat(compStyleBall.getPropertyValue("height"));
  let posX = parseFloat(compStyleBall.getPropertyValue("left"));
  let posY = parseFloat(compStyleBall.getPropertyValue("top"));
  if(hitTest(ball,player2) || hitTest(ball,player1)){
    console.log("hitTest true");
    ballVelX *= -1; //reverse direction
    //randomize the Y direction lul
    ballVelY += (Math.random() * 5)-2.5;
  }
  else if(!hitTest(ball, gameBoard)){//ball is going out
    ballVelY *= -1;
  }
  ball.style.left = posX+ballVelX + "px";
  ball.style.top = posY+ballVelY + "px";

}

setInterval(animateBall, 10);

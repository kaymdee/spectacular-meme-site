console.log('Script is running...');
//likeBtn js in topNav
const likeBtn =
  document.querySelector("#likedPost");

const yourBtn =
    document.querySelector("#profilePost");

const likeAction = () => {
  if(likeAction){
    yourBtn.style.backgroundColor = "#ffef00";
    yourBtn.style.color = "#2dc248";
    yourBtn.style.borderColor ="#2dc248"


  likeBtn.style.backgroundColor = "#2dc248";
  likeBtn.style.color = "#ffef00";
  likeBtn.style.borderColor ="#ffef00"
}

//  likeBtn.classList.add("liked");
};

likeBtn.addEventListener("click", likeAction);

const yourPostAction = () => {
  if(likeAction){
    likeBtn.style.backgroundColor = "#ffef00";
    likeBtn.style.color = "#2dc248";
    likeBtn.style.borderColor ="#2dc248"


  yourBtn.style.backgroundColor = "#2dc248";
  yourBtn.style.color = "#ffef00";
  yourBtn.style.borderColor ="#ffef00"
  //yourBtn.classList.add("liked");
}
}
yourBtn.addEventListener("click", yourPostAction);

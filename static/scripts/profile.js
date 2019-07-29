const showLikedPostsBtn = document.getElementById("likedPost");
const profilePostsDiv = document.getElementById("profilePostsDiv");
const likedPostsDiv = document.getElementById("likedPostsDiv");
const showProfilePostsBtn = document.getElementById("profilePost");
showLikedPostsBtn.addEventListener("click", (e) =>{
  likedPostsDiv.classList.remove("hidden")
  profilePostsDiv.classList.add("hidden")

});
showProfilePostsBtn.addEventListener("click", (e) =>{
  likedPostsDiv.classList.add("hidden")
  profilePostsDiv.classList.remove("hidden")

});

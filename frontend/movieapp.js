/*
    Module: movieapp.js
    Author: Nashith vp
    Description: javascript file for movieapp front end

    License:

    Created on: 15-02-2024 
*/


function logging_in_function() {
    alert("Logging in....");
}

////////////////////// USER ////////////////////////////
let i = 0
create_user = () => {
    if (i % 2 == 0){st = "new user ceated";} else {st = "AAAAAAAAAAA"}; //jsut for demo
    i= ++i % 2;
    console.log(i)
    const element = document.getElementById("create-user");
    element.textContent = st;
    element.style.color = "white";

}

watch_movie = () => {
    st = "You can watch";
    const element = document.getElementById("watch-movie");
    element.textContent = st;
    element.style.color = "white";

}

post_rating = () => {
    st = "Rrating is posted";
    const element = document.getElementById("post-rating");
    element.textContent = st;
    element.style.color = "white";

}


find_user = () => {
    st = "Found";
    const element = document.getElementById("find-user");
    element.textContent = st;
    element.style.color = "white";

}

update_user = () => {
    st = "Updated";
    const element = document.getElementById("update-user");
    element.textContent = st;
    element.style.color = "white";

}

delete_user = () => {
    st = "Deleted";
    const element = document.getElementById("delete-user");
    element.textContent = st;
    element.style.color = "white";

}

///////////////////////// MOVIE /////////////////////////

display_movies = () => {
    st = "Displayed";
    const element = document.getElementById("display-movies");
    element.textContent = st;
    element.style.color = "white";

}

create_movie_info = () => {
    st = "Created";
    const element = document.getElementById("create-movie");
    element.textContent = st;
    element.style.color = "white";

}

edit_movie_info = () => {
    st = "Edited";
    const element = document.getElementById("edit-movie");
    element.textContent = st;
    element.style.color = "white";

}

delete_movie_info = () => {
    st = "Deleted";
    const element = document.getElementById("delete-movie");
    element.textContent = st;
    element.style.color = "white";

}


const nameDIV = document.getElementById('account_name');
const followerDIV = document.getElementById('Follower');
const followingDIV = document.getElementById('Following');
const followButtonDIV = document.getElementById('follow_button');

nameDIV.innerHTML = '';
followerDIV.innerHTML = '';
followingDIV.innerHTML = '';
followButtonDIV.innerHTML = '';

function getCSRFToken() {
    const selectElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return selectElement.value;
}


fetch(`${baseUrl}/account/${profile_id}`)
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    if (currentUser){
        followButtonDIV.innerHTML += `<button class="likeButton" onclick="">dsf</button>`
    }
    else{
        followButtonDIV.innerHTML += `<a href="/login" class="loginButton"><button>like</button></a>`
    }

    followerDIV.innerHTML+= `${data.follower_count}`;
    followingDIV.innerHTML += `${data.following_count}`;
    nameDIV.innerHTML += `${data.account_name}`;
    console.log(data)
})


.catch(error => {
    console.error('Error fetching data:', error);
    // Handle error, e.g., display an error message on the page
});




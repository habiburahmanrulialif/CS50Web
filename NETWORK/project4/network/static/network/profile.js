const nameDIV = document.getElementById('account_name');
const followerDIV = document.getElementById('Follower');
const followingDIV = document.getElementById('Following');
const followButtonDIV = document.getElementById('follow_button');

function clean(){
    nameDIV.innerHTML = '';
    followerDIV.innerHTML = '';
    followingDIV.innerHTML = '';
    followButtonDIV.innerHTML = '';
}

clean()

function getCSRFToken() {
    const selectElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return selectElement.value;
}

const csrfToken = getCSRFToken()

function follow_counter(){
    fetch(`${baseUrl}/account/${profile_id}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        followerDIV.innerHTML+= `${data.result.follower_count}`;
        followingDIV.innerHTML += `${data.result.following_count}`;
        nameDIV.innerHTML += `${data.result.account_name}`;

        if (currentUser){
            let account_name = data.result.account_name;
            if (currentUser == account_name){
                followButtonDIV.innerHTML += ``;
            }
            else{
                followButtonDIV.innerHTML += `<button class="likeButton" onclick="follow_button()">${data.check ? 'unfollow' : 'follow'}</button>`;
            }
            
        }
        else{
            followButtonDIV.innerHTML += `<a href="/login" class="loginButton"><button>follow</button></a>`;
        }

        console.log(data)
    })

    .catch(error => {
        console.error('Error fetching data:', error);
        // Handle error, e.g., display an error message on the page
    });
}

function follow_button(){
    fetch(`${baseUrl}/follow/${profile_id}`, {
        method: 'PUT',
        headers:{
            'X-CSRFToken': csrfToken
        }
        })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
        clean()
        follow_counter()
    })

    .catch(error => {
        console.error('Error fetching data:', error);
        // Handle error, e.g., display an error message on the page
    });
}

follow_counter()
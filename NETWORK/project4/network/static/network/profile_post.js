function getCSRFToken() {
    const selectElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return selectElement.value;
}


var currentPage = 1;
const baseUrl = window.location.protocol + '//' + window.location.host;
const userID = 1;
const profileURL = `${baseUrl}/profile/${userID}/`;

function fetchData(page) {
    fetch(`${profileURL}?page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => displayData(data))
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error, e.g., display an error message on the page
        });
}

function displayData(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    const fetchLikeStatusPromises = data.results.map(item =>
        fetch(`${baseUrl}/check_like_status/${item.id}/`).then(response => response.json())
    );

    Promise.all(fetchLikeStatusPromises)
        .then(likeStatuses => {
            data.results.forEach((item, index) => {
                const likeData = likeStatuses[index];

                const postImage = item.post_image ? `<img class="card-img-top" src="${item.post_image}" alt="Title" />` : '';

                const isOwner = item.username === currentUser; 
                let editButton = '';
                if (isOwner) {
                    editButton = `<button class="likeButton" onclick="edit(${item.id})">Edit Post</button>`; // Custom message or action for the owner
                } 
                let checkUser = '';
                
                if (currentUser){
                    checkUser = `<button class="likeButton" onclick="like(${item.id})">${likeData.liked ? 'unlike' : 'like'}</button>`
                }
                else{
                    checkUser = `<a href="/login" class="loginButton"><button>like</button></a>`
                }
                resultsDiv.innerHTML += `
                    <div id="items">
                        <div class="card text-start">
                            ${postImage}
                            <div class="card-body">
                                <h4 class="card-title">${item.username}</h4>
                                <p class="card-text">${item.post_text}</p>
                                <p class="card-text">${item.clean_post_time}</p>
                                <p class="card-text">Like : ${item.like_count}</p>
                                ${checkUser}
                                ${editButton}
                            </div>
                        </div>
                    </div>
                `;
            });
        })
        .catch(error => {
            console.error('Error fetching like statuses:', error);
            // Handle error if needed
        });

    document.getElementById('prevBtn').disabled = !data.previous;
    document.getElementById('nextBtn').disabled = !data.next;
}

document.getElementById('prevBtn').addEventListener('click', function() {
    if (currentPage > 1) {
        currentPage--;
        fetchData(currentPage);
    }
});

document.getElementById('nextBtn').addEventListener('click', function() {
    currentPage++;
    fetchData(currentPage);
});

// Initial fetch when the page loads
fetchData(currentPage);


function like(id){
    const csrfToken = getCSRFToken();
    fetch(`${baseUrl}/post/${id}`, {
        method: 'PUT',
        headers:{
            'X-CSRFToken': csrfToken
        }
        })
    .then(response =>  {
        // Handle response from the server
        console.log(response);
        fetchData(currentPage);
    })
}
var currentPage = 1;
document.querySelector('#editPost').style.display = 'none';
function fetchData(page) {
    fetch(`post/?page=${page}`)
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
        fetch(`check_like_status/${item.id}/`).then(response => response.json())
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
                let account = '';
                account = `<h4 class="card-title"><a href="/profiles/${item.post_owner}">${item.username}</a></h4>`
                resultsDiv.innerHTML += `
                    <div id="items">
                        <div class="card text-start">
                            ${postImage}
                            <div class="card-body">
                                ${account}    
                                <p class="card-text">${item.post_text}</p>
                                <p class="card-text">Posted at : ${item.clean_post_time}</p>
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
    fetch(`post/${id}`, {
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

function edit(id){
    document.querySelector('#editPost').style.display = 'block';

    fetch(`post/${id}`, {
        method: 'GET'
        })
    .then(response =>  {
        // Handle response from the server
        console.log(response);
        return response.json();
    })
    .then(data => {
        console.log(data);
        var editTextInput = document.querySelector('#editTextInput');

        if (data && data.post_text !== undefined) {
            editTextInput.value = data.post_text;
        } else {
            console.error('Invalid data or missing post_text property.');
        }
        editTextInput.focus();
        var hiddenValue = document.querySelector('#postID');
        hiddenValue.value = data.id;
    })
    .catch(error => {
        console.error('Error fetching or setting data:', error);
        });
}
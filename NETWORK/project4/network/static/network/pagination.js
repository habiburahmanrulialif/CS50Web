let currentPage = 1;

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

    data.results.forEach(item => {
        if (item.post_image){
            resultsDiv.innerHTML += `
            <div id="items">
                <div class="card text-start">
                    <img class="card-img-top" src="${item.post_image}" alt="Title" />
                    <div class="card-body">
                        <h4 class="card-title">${item.post_owner}</h4>
                        <p class="card-text">${item.post_text}</p>
                    </div>
                </div>
            </div>
            `; 
        }
        else{
            resultsDiv.innerHTML += `
            <div id="items">
                <div class="card text-start">
                    <div class="card-body">
                        <h4 class="card-title">${item.post_owner}</h4>
                        <p class="card-text">${item.post_text}</p>
                    </div>
                </div>
            </div>
            `; 
        }

        
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
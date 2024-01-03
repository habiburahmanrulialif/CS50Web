function getCSRFToken() {
    const selectElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return selectElement.value;
}

function cleanForm(){
    document.getElementById('uploadForm').reset();
}

document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const csrfToken = getCSRFToken();
    let formData = new FormData();
    const textInput = document.getElementById('textInput').value;
    const imageInput = document.getElementById('imageInput').files[0];

    formData.append('textData', textInput);
    formData.append('image', imageInput);

    fetch('post/', {
        method: 'POST',
        body: formData,
        headers:{
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        // Handle response from the server
        console.log('Data uploaded successfully');
    })
    .catch(error => {
        // Handle errors
        console.error('Error uploading data:', error);
    });
    
    cleanForm()
});
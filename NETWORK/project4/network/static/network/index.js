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

    fetch('posting/', {
        method: 'POST',
        body: formData,
        headers:{
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        // Handle response from the server
        console.log('Data uploaded successfully');
        fetchData(currentPage);
    })
    .catch(error => {
        // Handle errors
        console.error('Error uploading data:', error);
    });
    cleanForm();
});

document.getElementById('uploadFormEdit').addEventListener('submit', function(e) {
    e.preventDefault();
    const csrfToken = getCSRFToken();
    let formData = new FormData();
    const textInput = document.getElementById('editTextInput').value;
    const imageInput = document.getElementById('editimageInput').files[0];

    formData.append('textData', textInput);
    formData.append('image', imageInput);
    const hiddenData = document.getElementById('postID').value;

    console.log('textInput:', textInput);
    console.log('imageInput:', imageInput);
    console.log('hiddenData:', hiddenData);
    console.log('csrfToken:', csrfToken);
    fetch(`postEdit/${hiddenData}`, {
        method: 'POST',
        body: formData,
        headers:{
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        // Handle response from the server
        console.log(response);
        fetchData(currentPage);
        document.querySelector('#editPost').style.display = 'none';
    })
    .catch(error => {
        // Handle errors
        console.error('Error uploading data:', error);
    });
});
document.addEventListener('DOMContentLoaded', function() {
    view();
});

function view(){
    document.getElementById("left").style.visibility = 'hidden';
    document.getElementById("mid").style.display = 'block';
    document.getElementById("right").style.visibility = 'hidden';
}
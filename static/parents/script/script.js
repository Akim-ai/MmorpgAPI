const TOKEN = function get_token() {
    let _token = localStorage.getItem('token');
    if (!_token){
        window.location.replace = 'http://localhost:8000/sign-in/';
    }
    return JSON.parse(_token);
}();

const API_PREFIX = document.getElementById('api_prefix').innerText.slice(0, -1).toString();

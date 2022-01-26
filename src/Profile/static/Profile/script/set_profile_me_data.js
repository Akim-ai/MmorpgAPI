function set_avatar(url) {
    let img = document.createElement('img');
    img.src = url;
    img.classList = ['avatar'];
    img.alt = 'avatar of user';
    img.id = 'avatar';

    let place = document.getElementById('avatar_container');
    place.appendChild(img);
}

function set_user_data(key, value) {
    let paragraph = document.createElement('p');
    let prefix;
    switch (key) {
        case ('announcements'):
            prefix = 'Количество созданных объявлений: ';
            break;
        case ('announcement_responses'):
            prefix = 'Количество оправленных откликов на объявления: ';
            break;
        case ('bio'):
            prefix = 'Биография: ';
            break;
        case ('city'):
            prefix = 'Город: ';
            break;
        case ('country'):
            prefix = 'Страна: ';
            break;
        default:
            prefix = ''
            break;
    }
    paragraph.innerText = prefix + value;
    paragraph.classList = [key, ];
    paragraph.id = key;

    let place = document.getElementById('user-data');
    place.appendChild(paragraph);
}


function get_data_onload() {
    fetch(window.location.origin + '/' + API_PREFIX + window.location.pathname, {
        method: 'GET',
        headers: {'Content-type': 'application/json;charset=UTF-8', 'Authorization': 'Token '+ TOKEN},
    })
    .then((res) => {
        res = res.json();
        return res
    })
    .then((data) => {
        if (data.detail === 'Invalid authentication. Could not decode token.'){
            window.location.replace('http://localhost:8000/sign-in/');
        }
        return data
    })
    .then((data) => {
        for (const key in data){
            if (data[key]){
                const value = data[key];
                if (value !== null){
                    if (key !== 'avatar'){
                        set_user_data(key, value);
                    }
                    else{
                        set_avatar(value);
                    }
                }
            }
        }
    })
}
window.addEventListener('load', get_data_onload)
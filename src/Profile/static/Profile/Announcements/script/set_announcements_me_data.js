let announcement_page = 1;
let announcement_count;

const DATA_CONTAINER = document.getElementById('data-container');

function set_responses(data, announcement) {

}

function get_responses(announcement_id, response_page) {
    fetch(
        window.location.origin+'/'+API_PREFIX+window.location.pathname
        +announcement_id+'/response/'+'?page='+response_page,{
        method: 'GET',
        headers: {
            'Content-type': 'application/json;charset=UTF-8', 'Authorization': 'Token '+ TOKEN
        },
    })
        .then((res) => {
            console.log(res)
            res = res.json();
            return res
        })
        .then((data) => {
           if (data.detail === 'Invalid authentication. Could not decode token.'){
                window.location.replace('http://localhost:8000/sign-in/');
           }
           console.log(data);
           return data
        })
}

//must write a func that adds responses on scroll of open announcement

function first_get_responses(announcement_id) {
    let announcement = document.getElementById('announcement_'+announcement_id);
    let responses_cnt = parseInt(announcement.getElementsByClassName('announcement_stats')[0].getElementsByClassName('announcement_cnt_responses')[0].innerHTML);
    // must add event to announcement
    const responses = get_responses(announcement_id, '1');

    set_responses(responses, announcement);
}

// must write opening announcement

function set_data(data) {

    for (let key in data){

        const value = data[key];
        const announcement = document.createElement('div');

        announcement.id = 'announcement_'+value['id'];
        announcement.classList = 'announcement_container announcement';


        const date = document.createElement('p');
        const category = document.createElement('p');
        const cnt_responses = document.createElement('p');

        date.innerText = value['create_date'];
        category.innerText = value['category'];
        cnt_responses.innerText = value['responses'];
        if (parseInt(value['responses'])){
            announcement.addEventListener(
                'mouseup', function _first_get_responses( e){
                    first_get_responses(value.id);
                    this.removeEventListener('mouseup', _first_get_responses)
                    },
                )

            const responses_container = document.createElement('div');
            responses_container.id = 'responses_of_announcement_'+value.id;

            responses_container.hidden = true;


            responses_container.innerHTML = '1';
            announcement.append(responses_container);
        }

        date.classList = 'announcement_create_date';
        category.classList = 'announcement_category';
        cnt_responses.classList = 'announcement_cnt_responses';

        const stats = document.createElement('div');
        stats.classList = 'announcement_stats';

        stats.appendChild(category);
        stats.appendChild(cnt_responses);
        stats.appendChild(date);


        announcement.appendChild(stats);

        const title = document.createElement('p');
        const description = document.createElement('p');

        title.innerText = value['title'];
        description.innerText = value['description'];

        title.classList = 'announcement_title';
        description.classList = 'announcement_description';

        const text = document.createElement('div');
        text.classList = 'announcement_text';

        text.appendChild(title);
        text.appendChild(description);

        announcement.appendChild(text);

        DATA_CONTAINER.appendChild(announcement);

    }
    console.log(data);
}


function get_data_onload(){
    fetch(window.location.origin+'/'+API_PREFIX+window.location.pathname+'?page='+announcement_page,{
        method: 'GET',
        headers: {
            'Content-type': 'application/json;charset=UTF-8', 'Authorization': 'Token '+ TOKEN
        },
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

            if (data['next']){page+=1;} else {page=null;}

            announcement_count = data['count'];
            return data
        })
        .then((data) => {
            console.log(data)
            set_data(data['results'])
        })
}


window.addEventListener('load', get_data_onload)


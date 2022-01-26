import React from 'react'

import ConstantTextCollection from "../../components/ConstantText";
import CreateAnnouncementForm from "../../Announcements/components/createAnnouncement";
import {Link} from "react-router-dom";
import AnnouncementCollapsibleTable from "./AnnouncementResponsesTable";


export default class SelfAnnouncements extends React.Component{

    constructor(props) {
        super(props);


        this.state = {
            announcement_data: [],

            announcement_next_page: 1,
            announcement_responses: {},
            can_get_data_responses: [],

            announcement_height: 0,

            create_announcement_open: false,
            create_announcement_title: '',
            create_announcement_description: '',
            create_announcement_category: '',
        }

        this.get_announcements = this.get_announcements.bind(this);
        this.get_announcement_responses = this.get_announcement_responses.bind(this);

        this.create_responses_ref = this.create_responses_ref.bind(this)
        this.open_announcement_responses = this.open_announcement_responses.bind(this);

        this.infinity_announcement_scroll = this.infinity_announcement_scroll.bind(this);
        this.infinity_responses_scroll = this.infinity_responses_scroll.bind(this);

        this.openClose_create_announcement = this.openClose_create_announcement.bind(this);
        this.create_announcement_title_change = this.create_announcement_title_change.bind(this);
        this.create_announcement_description_change = this.create_announcement_description_change.bind(this);
        this.create_announcement_category_change = this.create_announcement_category_change.bind(this);
        this.create_announcement = this.create_announcement.bind(this);
    }

    componentDidMount() {

        const promise = this.get_data('me/announcement/', `?page=1`)
            .then((data) => {

                if(!data.results){
                    return
                }

                const announcement_responses = this.from_arrayDicts_to_dict(data.results)

                console.log(announcement_responses)

                this.setState({
                    announcement_data: data.results, announcement_next_page: data.next,
                    announcement_responses,
                });
                console.log(data.next)
                if (data.next){
                    window.addEventListener('scroll', this.infinity_announcement_scroll);
                    console.log('added')
                }
            })
    }

    componentWillUnmount() {

        window.removeEventListener('scroll', this.infinity_announcement_scroll)
        window.removeEventListener('scroll', this.infinity_responses_scroll)
    }

    from_arrayDicts_to_dict(arr){

        let new_dict ={};

        for (let i=0; i<arr.length; i++){
            if(arr[i].responses){
                new_dict[arr[i].id] = {page: 1, open: false, data: false};
            }
        }
        return new_dict
    }

    get_data(path, request='',api = 'http://localhost:8000/api/v1/'){
        return fetch(api+path+request, {
            method: 'GET',
            headers: {
                'Content-type': 'application/json;charset=UTF-8',
                'Authorization': 'Token '+ localStorage.getItem('token')},
        })
            .then(res => {
                return res.json()
            })
            .then(data => {

                if (data.detail === 'Invalid authentication. Could not decode token.'){
                    window.location.replace('/sign-in/');
                }
                return data;
            })
            .catch((error) => {
                console.log(error)
            })
    }

    get_announcements(){
        const promise = this.get_data('', '', `${this.state.announcement_next_page}`)
        promise.then((data) => {

            const announcement_responses = this.from_arrayDicts_to_dict(data.results);
            console.log(announcement_responses)
            this.setState({
                announcement_data: [...this.state.announcement_data, ...data.results],
                announcement_next_page: data.next,
                announcement_responses: {...this.announcement_responses, ...announcement_responses}
            })

            if(data.next){
                window.addEventListener('scroll', this.infinity_announcement_scroll);
                console.log('added')
            }
        })
        promise.catch((exp) => {
            console.log(exp)
        })
    }

    create_responses_ref(node){
        this[`announcementResponse_${node.id.split('_')[1]}`] = React.createRef();
        this[`announcementResponse_${node.id.split('_')[1]}`].current = node;
        return this[`announcementResponse_${node.id.split('_')[1]}`]
    }

    can_get_data_responses_checkPop(announcement_id){

        let can_get_data_responses =  this.state.can_get_data_responses;
        for (let i=0; i < can_get_data_responses.length; i++){

            if(announcement_id===can_get_data_responses[i]){
                can_get_data_responses.splice(i, 1);
                return can_get_data_responses
            }
        }
        console.log('value not found')
        return can_get_data_responses;
    }

    open_announcement_responses(event){

        const announcement_id = event.target.id.split('_')[1];
        console.log(event.target.id)
        let response_data = this.state.announcement_responses[announcement_id];

        console.log(response_data)

        if(!response_data.open){

            if(!response_data.data){

                // console.log('first open')
            const promise = this.get_data(`me/announcement/${announcement_id}/response/`, '?page=1')
                .then((data) => {

                    let next_page;
                    let can_get_data_responses = this.state.can_get_data_responses;

                    if(data.next){
                        next_page = data.next;
                        if(!(announcement_id in can_get_data_responses)){
                            can_get_data_responses.push(announcement_id);
                        }
                    }

                    let announcement_responses = this.state.announcement_responses;
                    announcement_responses[announcement_id] = {page: next_page, data: data.results, open: true};

                    console.log(response_data)
                    this.setState({can_get_data_responses, announcement_responses})

                    if (can_get_data_responses.length === 1){
                        window.addEventListener('scroll', this.infinity_responses_scroll)
                    }
                    })
                }

            else{

                // console.log('Second open')

                let announcement_responses = this.state.announcement_responses;
                response_data.open = !response_data.open;
                announcement_responses[announcement_id] = response_data;

                console.log(this.state.can_get_data_responses.length)
                let can_get_data_responses = this.state.can_get_data_responses;
                console.log((announcement_id in can_get_data_responses))
                if (can_get_data_responses.length>1){

                    let if_in = false
                    for (let i=0; i<can_get_data_responses.length; i++){if(i===can_get_data_responses[i]){if_in=true;break;}}

                    if(!if_in){can_get_data_responses.push(announcement_id);}
                }

                this.setState({announcement_responses, can_get_data_responses})
                console.log(announcement_responses)
            }
        }
        else{

            // console.log('close_page')
            console.log(this.state.can_get_data_responses)

            response_data.open = !response_data.open;
            let announcement_responses = this.state.announcement_responses;
            announcement_responses[announcement_id] = response_data;

            const can_get_data_responses = this.can_get_data_responses_checkPop(announcement_id)
            if(!can_get_data_responses.length){window.removeEventListener('scroll', this.infinity_responses_scroll, false)}
            this.setState({announcement_responses, can_get_data_responses})
            console.log(this.state.can_get_data_responses)
            console.log(can_get_data_responses.length)
        }
    }

    infinity_announcement_scroll(event){
        const scrolled = window.scrollY + window.innerHeight;
        if (scrolled + 10 >= this.announcement_container.scrollHeight){

            this.get_announcements();
            window.removeEventListener('scroll', this.infinity_announcement_scroll);
        }
    }

    get_announcement_responses(url, announcement_id){

        this.get_data('', '', url)
            .then((data)=> {
                console.log(data)

                const can_get_announcement_responses = data.next ? this.state.can_get_data_responses : this.can_get_data_responses_checkPop(announcement_id);

                let announcement_responses = this.state.announcement_responses;
                announcement_responses[announcement_id].data = [...announcement_responses[announcement_id].data, ...data.results]
                announcement_responses[announcement_id].page = data.next

                this.setState({can_get_announcement_responses, announcement_responses})
                window.addEventListener('scroll', this.infinity_responses_scroll)
            })
    }

    infinity_responses_scroll(event){

        const scrolled = window.scrollY + window.innerHeight;

        for (let i=0; i < this.state.can_get_data_responses.length; i++){
            console.log(this.state.can_get_data_responses)
            const announcement_id = this.state.can_get_data_responses[i];
            const response_container = this[`announcementResponse_3`].current;

            if (response_container.offsetTop+response_container.clientHeight <= scrolled+1){
                this.get_announcement_responses(this.state.announcement_responses[announcement_id].page, announcement_id)
                window.removeEventListener('scroll', this.infinity_responses_scroll)

                console.log(response_container.offsetTop, response_container.clientHeight, scrolled+1)
            }
        }
    }

    openClose_create_announcement(e){
        this.setState({create_announcement_open: !this.create_announcement.open})
    }

    create_announcement_title_change(event){
        this.setState({create_announcement_title: event.target.value})
    }
    create_announcement_description_change(event){
        this.setState({create_announcement_description: event.target.value})
    }
    create_announcement_category_change(event){
        this.setState({create_announcement_category: event.target.value})
    }

    create_announcement(event){
        event.preventDefault();
        if(this.state.create_announcement_title.length <= 150 && this.state.create_announcement_description.length <= 1500){
            fetch('http://localhost:8000/api/v1/announcement/', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+ localStorage.getItem('token')
                },
                body:JSON.stringify({
                    title: this.state.create_announcement_title,
                    description: this.state.create_announcement_description,
                    category: this.state.create_announcement_category,
                })
            })
                .then((res) => {
                    res = res.json();
                    return res
                })
                .then((data) => {
                    if (data.detail === 'Invalid authentication. Could not decode token.'){

                        window.location.replace('/sign-in/');
                    }
                    return data;
                })
                .then((data) => {
                    console.log(data)

                    this.setState({announcement_data: [data, ...this.state.announcement_data]})
                })
        }
        else{alert('Заголовок - максимум 150 символов, описание- максимум 1500 символов');}
    }

    render() {
        console.log(123)
        return (
        <div>
        <div>
            <Link to={'/profile/'}>Профиль</Link>
        </div>
        {this.state.create_announcement_open ?
            <CreateAnnouncementForm
                openClose={this.openClose_create_announcement}

                title={this.state.create_announcement_title}
                onTitleChange={this.create_announcement_title_change}

                description={this.state.create_announcement_description}
                onDescriptionChange={this.create_announcement_description_change}

                category={this.state.create_announcement_category}
                onCategoryChange={this.create_announcement_category_change}

                onSubmitForm={this.create_announcement}
            />
            : <button onClick={this.openClose_create_announcement}>Создать объявление</button>}
            {
                this.state.announcement_data.length > 0 ?
                    <AnnouncementCollapsibleTable
                        rows={this.state.announcement_data}
                        announcement_ref = {node => this['announcement_container'] = node}
                        response_ref = {this.create_responses_ref}
                        responses_data = {this.state.announcement_responses}
                        open_announcement = {this.open_announcement_responses}
                     />
                 :
                    ''
            }
        </div>
        )
    }
}
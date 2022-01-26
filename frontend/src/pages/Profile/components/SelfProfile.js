import React from 'react';
import { Link } from 'react-router-dom'

import '../../main.css';

import Avatar from "../../components/Avatar";
import EditableText from "../../components/EditableText";
import ButtonsCollection from "../../components/button";


class SelfProfile extends React.Component{
    constructor(props) {
        super(props);

        this.state = {
            data: {},

            form_using: {
                display_name: false,
                bio: false,
                country: false,
                city: false,
            },
            form_used: false,

            new_user_data: {
                display_name: '',
                bio: '',
                country: '',
                city: '',
            },

        };

        this.to_form_or_span = this.to_form_or_span.bind(this);
        this.user_data_input = this.user_data_input.bind(this);

        this.save_new_data_user = this.save_new_data_user.bind(this);
        this.remove_new_data_user = this.remove_new_data_user.bind(this);
    }

    componentDidMount() {
        this.get_data()
    }

    async get_data() {
        await fetch('http://localhost:8000/api/v1/me/', {
            method: 'GET',
            headers: {'Content-type': 'application/json;charset=UTF-8', 'Authorization': 'Token '+ localStorage.getItem('token')},
        })
            .then((res) => {
                res = res.json();
                return res
            })

            .then((res) => {
                (res.detail) ? window.location.replace('/sign-in') : this.setState({data: res,});
                this.setState({data: res})
            })

            .catch((e) => {console.log(e)})
    }

    to_form_or_span(event){
        let new_data = Object.assign(this.state.form_using);

        new_data[`${event.target.id}`] = !new_data[`${event.target.id}`];

        if (new_data[`${event.target.id}`]){

            if (!this.state.used_form){this.setState({form_used: true})}

            let new_user_data = Object.assign(this.state.new_user_data)
            new_user_data[event.target.id] = this.state.data[`${event.target.id}`]
            this.setState({form_using: new_data, new_user_data: new_user_data})

        }
        else{

            let use_buttons = true;
            for(const key in new_data) {
                if(new_data[key]){use_buttons=true;break;}
                else{use_buttons=false;}
            }
            this.setState({form_using: new_data, form_used: use_buttons});
        }
    }

    user_data_input(event){
        let new_data = Object.assign(this.state.new_user_data);
        new_data[event.target.id] = event.target.value;


        this.setState({new_user_data: new_data})
    }

    async save_new_data_user(event){

       const sorted_data = JSON.stringify(this.state.new_user_data);

       await fetch('http://localhost:8000/api/v1/profile/', {
            method: 'PUT',
            headers: {'Content-type': 'application/json;charset=UTF-8', 'Authorization': 'Token '+ localStorage.getItem('token')},
            body: sorted_data
       })
           .then((res) => {
               return res.json();
           })
           .then((data) => {
               this.setState({data: data})
           })
    }

    remove_new_data_user(event){

        this.setState({
            new_user_data: {
                display_name: this.state.data.display_name,
                bio: this.state.data.bio,
                country: this.state.data.country,
                city: this.state.data.city,
            },

            form_using: {
                display_name: false,
                bio: false,
                country: false,
                city: false,
            },

            form_used: false
        })

    }

    render() {
        if (!this.state.data) {return <div>Getting data</div>;}
        return(
            <div /*className='content'*/ id='content'>
                <div id='editable_user_data'><Avatar src={this.state.data.avatar}/>
                <div className='user_data_container'>
                <EditableText
                    id='display_name'
                    text={this.state.data.show_display_name}
                />

                <EditableText
                    id='bio'
                    text={
                        (this.state.form_using['bio']) ? this.state.new_user_data['bio'] : (this.state.data.bio) ? this.state.data.bio : 'Вы всегда можете заполнить биографию'}
                    forDoubleClick={this.to_form_or_span}
                    forChange={this.user_data_input}
                    use_form={this.state.form_using['bio']}
                />
                <EditableText
                    id='country'
                    text={
                        (this.state.form_using['country']) ? this.state.new_user_data['country'] : (this.state.data.country) ? this.state.data.country : 'Пока страна не определена'
                    }
                    forDoubleClick={this.to_form_or_span}
                    forChange={this.user_data_input}
                    use_form={this.state.form_using['country']}
                />
                <EditableText
                    id='city'
                    text={
                        (this.state.form_using['city']) ? this.state.new_user_data['city'] : (this.state.data.city) ? this.state.data.city : 'Город пока не определен'
                    }
                    forDoubleClick={this.to_form_or_span}
                    forChange={this.user_data_input}
                    use_form={this.state.form_using['city']}
                />
                {this.state.form_used ? <ButtonsCollection
                    buttons={[
                        {id: 'remove_new_data', text: 'Отменить изменения', type: 'submit', key: 'remove_new_data', onClick: this.remove_new_data_user},
                        {id: 'save_user_data', text: 'Сохранить', type: 'submit', key: 'save_new_data_user', onClick: this.save_new_data_user}]}
                    />
                    : ''}
                </div></div>

                <Link id='created_announcements' to='/profile/announcements/'>
                    Количество созданных объявлений: {this.state.data.announcements ? this.state.data.announcements : 0}
                </Link>

                <Link id='created_responses' to='/profile/responses/'>
                    Количество оставленных откликов: {this.state.data.announcement_responses}
                </Link>
            </div>)
    }
}

export default SelfProfile
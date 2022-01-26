import React from 'react'
import ConstantTextCollection from "../../components/ConstantText";

export default class SelfResponses extends React.Component{
    constructor(props) {
        super(props);

        this.state = {
            responses: [],
            responses_page: '',
        }

        this.infinity_scroll = this.infinity_scroll.bind(this);
    }
    componentDidMount() {

        const promise = this.get_data('http://localhost:8000/api/v1/me/responses/?page=1')
            promise.then((data) => {

                let responses_page = false;
                if (data.next){
                    responses_page = data.next;
                    window.addEventListener('scroll', this.infinity_scroll);
                }

                this.setState({responses: data.results, responses_page})

            })
    }
    componentWillUnmount() {
        window.removeEventListener('scroll', this.infinity_scroll);
    }

    get_data(url){
        return fetch(url, {
            method: 'GET',
            headers: {
                'Content-type': 'application/json;charset=UTF-8',
                'Authorization': 'Token '+ localStorage.getItem('token')},
        })
            .then((res) => {

                res = res.json();
                return res;
            })
            .then(data => {

                if (data.detail === 'Invalid authentication. Could not decode token.'){
                    window.location.replace('/sign-in/');
                }
                console.log(data)
                return data;
            })
            .catch((error) => {
                console.log(error)
            })
    }

    get_responses(){
        const promise = this.get_data(this.state.responses_page)
            promise.then((data) => {
                this.setState({
                    responses: [...this.state.responses, ...data.results],
                    responses_page: data.next
                })
                if (data.next){window.addEventListener('scroll', this.infinity_scroll)}

            })
    }

    infinity_scroll(event){
    const scrolled = window.scrollY + window.innerHeight;
        if (scrolled+10 >= this.responses_container.scrollHeight){
            window.removeEventListener('scroll', this.infinity_scroll)
            this.get_responses()
        }
    }

    render() {
        console.log(this.state.responses)
        if (!this.state.responses.length) return <div> 123 </div>
        return (
            <div>
                <div ref={(responses_container) => {this.responses_container = responses_container}}>
                    {this.state.responses.map((response) => {
                        const response_prefix = `response_${response.id}`
                        return (
                            <ConstantTextCollection
                                self={{key: response_prefix, id: response_prefix}}
                                elements={[
                                    {
                                        key: `${response_prefix}_createDate`, id: `${response_prefix}_createDate`,
                                        text: response.create_date
                                    },
                                    {
                                        key: `${response_prefix}_announcement`, id: `${response_prefix}_announcement`,
                                        text: response.announcement
                                    },
                                    {
                                        key: `${response_prefix}_text`, id: `${response_prefix}_text`,
                                        text: response.text
                                    }
                                ]}
                            />
                        )
                    })}
                </div>
            </div>
        )
    }
}
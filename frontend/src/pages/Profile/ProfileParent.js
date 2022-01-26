import React from 'react'
import Profile from "./components/Profile";
import SelfProfile from "./components/SelfProfile";


export default class ProfileParent extends React.Component{
    constructor(props) {
        super(props);

        const { search } = window.location

        if(search.length > 0){
            const user_id = search.match(/user=([0-9]*)/m)?.[1];
            if (typeof user_id === typeof ''){this.user_id = user_id}
        }

    }

    render() {

        if(typeof this.user_id === typeof '') {
            return (
                <Profile user_id ={this.user_id}/>
            )
        }
        else{
            return (
                <SelfProfile/>
            )
        }
    }
}
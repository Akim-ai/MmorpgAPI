import React from "react";
import DisplayAnnouncements from "./components/DisplayAnnouncements";
import FullAnnouncement from "./components/FullAnnouncement";


export default class Announcement extends React.Component{
    constructor(props) {
        super(props);

        const { pathname, search } = window.location;
        this.announcement_id = pathname.match(/~([0-9]*)/m)?.[1];

        if(search.length > 0){
            const page = search.match(/page=([0-9])/m)?.[1];
            this.page = page != undefined ? page : '1'
        }
        else{this.page = '1'}

    }

    render() {
        if(this.announcement_id !== undefined){
            return (
            <div>
                <FullAnnouncement history={this.props} announcement_id={this.announcement_id}/>
            </div>
            )
        }
        return (
            <div>
                <DisplayAnnouncements page={this.page}/>
            </div>
        )
    }
}

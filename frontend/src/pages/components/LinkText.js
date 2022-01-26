import React from 'react'


export default class LinkText extends React.Component{

    render() {
        return <a href={this.props.link} className={this.props.class}>{this.props.context}</a>
    }
}
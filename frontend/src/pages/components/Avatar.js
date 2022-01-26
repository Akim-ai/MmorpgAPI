import React from 'react';

export default class Avatar extends React.Component {

    render() {
        const style = {
            maxWidth: '30%',
            maxHeight: '50%',
            display: 'inline',
        }
        return <img style={style} {...this.props} alt="user avatar"/>
    }
}
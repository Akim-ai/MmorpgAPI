import React from 'react'


class Button extends React.Component{

    render() {
        return (
            <button {...this.props.data}>{this.props.data.text}</button>
        )
    }
}


export default class ButtonsCollection extends React.Component{

    render() {
        return (
            <div>
                {this.props.buttons.map(button => {
                    return <Button data={button}/>
                })}
            </div>
        );
    }
}
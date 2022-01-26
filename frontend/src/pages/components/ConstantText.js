import React from 'react'


class ConstantText extends React.Component {
    render() {
        return (
            <span {...this.props.data}>{this.props.data.text}</span>
        )
    }
}

export default class ConstantTextCollection extends React.Component{
    render() {
        return (
            <div {...this.props.self}>
                {this.props.elements.map(element_data => {
                    return <ConstantText data={element_data}/>
                })}
            </div>
        )
    }
}
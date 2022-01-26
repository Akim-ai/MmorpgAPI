import React from 'react'


class Span extends React.Component{
    render() {
        return (
            <span {...this.props.data}>{this.props.data.text}  </span>
        )
    }
}

export default class SpanCollection extends React.Component{
    render() {
        return (
            <div id={this.props.id} className={this.props.className}>{
                this.props.span.map(span => {
                    return <Span data={span}/>
                })}
            </div>
        )
    }
}
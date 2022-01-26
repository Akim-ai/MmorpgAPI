import React from 'react';
import './styles/EditableText.css'

export default class EditableText extends React.Component{

    render() {
            if (!this.props.use_form){
                return (
                <span
                    id={this.props.id}
                    className='user_data'
                    onDoubleClick={this.props.forDoubleClick}
                    >{this.props.text}
                </span>
                )
            }
            return (
                <textarea
                       id={this.props.id}
                       className='user_data'
                       onChange={this.props.forChange}
                       onDoubleClick={this.props.forDoubleClick}
                       value={this.props.text}
                />
            )
    }
}
import React from 'react'

export default class SingInRegisterForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
      show_password: false,
      ans: {},
    };

    this.changeEmail = this.changeEmail.bind(this);
    this.changePassword = this.changePassword.bind(this);

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  changeEmail(event) {
    this.setState({email: event.target.value});
  }
  changePassword(event){
    this.setState({password: event.target.value})
  }


  successSingIn(token){
    localStorage.setItem('token', token);
    window.location.pathname = '/profile/'
  }


  handleSubmit(event) {
    this.setState({password: ''})
      fetch('http://localhost:8000/api/v1/sign-in/', {
      method: 'POST',
      headers: {'Content-type': 'application/json;charset=UTF-8'},
      body: JSON.stringify({
        email: this.state.email,
        password: this.state.password
      })
    })
        .then((res) => {
          res = res.json()
          return res
        })
        .then((data) => {
          return (data.access_token) ? this.successSingIn(data.access_token) : '';
        })
    event.preventDefault();

  }



  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Email:{' '}
          <input type="email" value={this.state.email} onChange={this.changeEmail} />
        </label>
        <br/>
        <label >
          Password:{' '}
          <input type={(this.state.show_password) ? 'text' : 'password'} value={this.state.password} onChange={this.changePassword}/>
          <button type='button' onClick={() => {this.setState({show_password: !this.state.show_password})}}>O</button>
        </label>
        <br/>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}
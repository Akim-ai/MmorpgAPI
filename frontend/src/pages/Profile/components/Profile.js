import React from 'react'
import auth_get_data from "../../../utils/fetch";
import {Avatar} from "@mui/material";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";


class DisplayProfile extends React.Component{

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Grid item container
                  id='user_data_container'
                  component={Paper}
                  xs={12} sm={12} md={12}
                  sx={{
                      marginTop: '10px',
                      padding: '10px'
                  }}
            >
                <Grid item container
                      id='name_avatar_container'
                      xs={12} sm={10} md={10}
                >
                    <Grid item
                          id='user_avatar'
                          xs={12} sm={7} md={1.4}
                          sx={{
                              backGroundImage: this.props.user.avatar
                          }}
                    >
                            {this.props.is_data ?
                                    <Avatar src={`${this.props.user.avatar}/`} alt='Аватар пользователя'
                                        sx={{
                                            width: 60,
                                            height: 60
                                        }}
                                    />
                                :
                                    <Avatar alt='Аватар пользователя'
                                        sx={{
                                            width: 60,
                                            height: 60
                                        }}
                                    >A</Avatar>
                            }
                    </Grid>
                    <Grid item container
                          id='username_place_container'
                          xs={5} sm={5} md={5}
                    >
                        <Grid item
                            id='user_name'
                              xs={3} sm={3} md={8}
                        >
                            {this.props.is_data ? this.props.user.name : 'Имя пользователя'}
                        </Grid>
                        <Grid item container
                            id='user_country'
                              xs={12} sm={3} md={8}
                        >
                            <Grid item
                                md={2}
                            >
                                <Typography
                                    variant='subtitle2'
                                    component='span'
                                >
                                    {this.props.is_data ? this.props.user.country+', ' : ''}</Typography>
                            </Grid>
                            <Grid item
                                  id='user_city'
                                  xs={12} sm={3} md={6}
                            >
                                <Typography
                                    variant='subtitle2'
                                    component='span'
                                >
                                    {this.props.is_data ? this.props.user.city : ''}
                                </Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item
                        id='user_bio'
                    >
                        {this.props.is_data ? this.props.user.bio : ''}
                    </Grid>
                </Grid>
            </Grid>
        )
    }
}


export default class Profile extends React.Component{
    constructor(props) {
        super(props);

        this.state = {
            user: {}
        }

    }

    componentDidMount() {
        auth_get_data(`http://localhost:8000/api/v1/profile/${this.props.user_id}/`)
            .then((data) => {
                console.log(data)

                this.setState({user: data})

            })
    }

    render() {
        return (
            <Grid container
                  justifyContent='center'
                  alignItems='center'
                  wrap='wrap'
            >
                <Grid item container
                    xs={12} sm={12} md={10}
                >
                    <DisplayProfile is_data={typeof this.state.user !== typeof undefined} user={this.state.user}/>
                </Grid>
            </Grid>
        )
    }
}
import React from 'react'
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Slide from '@mui/material/Slide'
import auth_get_data from '../../../utils/fetch';
import Avatar from "@mui/material/Avatar";
import Grid from '@mui/material/Grid';
import CloseIcon from '@mui/icons-material/Close';
import Link from "@mui/material/Link";


class DisplayFullAnnouncement extends React.Component{

    constructor(props) {
        super(props);
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return (nextProps !== this.props)
    }

    render() {
        console.log(this.props.announcement)
        return (
            <Box id={123}
                sx={{
                    margin: '15px 15px',
                    width: '100%',
                    display: 'inline'
                }}
            >
                <Grid container sx={12}
                      spacing={1}
                >
                        <Grid item container
                              xs={10}
                              spacing={2}
                        >
                            <Grid item xs={12}
                            >
                                <Typography
                                    variant="subtitle1" gutterBottom
                                    sx={{
                                        paddingTop: '20px'
                                    }}
                                >
                                    {this.props.announcement.title}
                                </Typography>
                            </Grid>
                            <Grid item xs={12}

                            >
                                <Typography variant='caption'
                                    sx={{
                                        paddingTop: '12px'
                                    }}
                                >
                                    {this.props.announcement.create_date}
                                </Typography>
                            </Grid>
                        </Grid>
                    <Grid item container xs={2}
                          justifyContent='center'
                          alignItems='center'
                          spacing={1}
                    >
                        <Grid item container xs={7}
                              justifyContent='center'
                              alignItems='center'
                        >
                            <Link underline='hover'
                                      color='green'
                                      href={this.props.announcement.user ? `/profile/?user=${this.props.announcement.user.id}` : '#'}
                                      sx={{
                                          cursor: 'pointer'
                                      }}
                                >
                                <Avatar alt='Аватар' src={'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.4XB8NF1awQyApnQDDmBmQwHaEo%26pid%3DApi&f=1'}/>
                            </Link>
                        </Grid>
                        <Grid item container xs={7}
                              justifyContent='center'
                              alignItems='center'
                        >
                                <Link underline='hover'
                                      color='green'
                                      href={this.props.announcement.user ? `/profile/?user=${this.props.announcement.user.id}` : '#'}
                                      sx={{
                                          cursor: 'pointer'
                                      }}
                                >
                                    <Typography variant='body1'>
                                        {this.props.announcement.user ? this.props.announcement.user.name : 'Имя создателя'}
                                    </Typography>
                                </Link>
                        </Grid>
                    </Grid>

                    <Grid item
                          sx={12}
                    >
                        <Typography variant='body2'

                        >
                            {this.props.announcement.description}
                        </Typography>
                    </Grid>
                </Grid>
            </Box>
        )
    }
}


class ReturnIcon extends React.Component{
    constructor(props) {
        super(props);
        this.return_url = window.location.pathname.replace(`details/${window.location.pathname.match(/~([0-9]*)/m)[0]}/`, '') + window.location.search
        console.log(this.return_url)
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return (nextProps !== this.props)
    }

    render() {
        return (
            <Link href={this.return_url}
                  elevation={4}

                  sx={{
                      position: 'fixed',
                      right: '10px',
                      top: '10px',
                      borderRadius: '50%',
                      display: 'inline-flex',
                }}
            >
                <CloseIcon sx={{
                        cursor: 'pointer',
                    }}
                    id='return_icon'
                />
            </Link>
        )
    }
}



export default class FullAnnouncement extends React.Component{

    constructor(props) {
        super(props);

        this.state = {
            announcement: {}
        }


        this.clickController = this.clickController.bind(this);
        window.addEventListener('click', this.clickController);

    }

    componentDidMount() {
        this.get_announcement()
    }

    get_announcement(){
        auth_get_data(`http://localhost:8000/api/v1/announcement/${this.props.announcement_id}/`)
            .then((data) => {
                console.log(data)
                this.setState({announcement: data})
            })
    }

    clickController(event){
        console.log(event.target)
        console.log(window.innerHeight)
    }



    render() {
        const announcement_prefix = `fullAnnouncement_${this.props.announcement_id}`
        return (
            <Box sx={{
                minWidth: '100vw',
                minHeight: '100vh',
                display: 'inline-flex',
                alignItems: 'center',
                flexDirection: 'row',
                justifyContent: 'center',
                margin: '0',
            }}
            >
                <ReturnIcon/>
                <Box component={Paper} sx={{
                    display: 'inline-flex',
                    minWidth: `60%`,
                    minHeight: `${window.innerHeight - 10}px`
                }}
                     elevation={4}
                >
                    <DisplayFullAnnouncement announcement={this.state.announcement}/>
                </Box>
            </Box>
        )
    }
}
import React from "react";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import AppBar from "@mui/material/AppBar";
import Container from "@mui/material/Container";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import {Menu, MenuItem} from "@mui/material";
import Link from "@mui/material/Link";
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import Avatar from "./Avatar";


export default class Header extends React.Component{

    constructor(props) {
        super(props);
        this.pages = [
            {
                key: 'announcement_link',
                link: '/announcement/',
                text: 'Объявления',
            },
        ]

        this.state = {

        }
    }

    render() {
        return (
            <AppBar position='static'>
                 <Container maxWidth='xl'>
                     <Toolbar disableGutters>
                         <Link href='/profile/'
                               color='rgb(255, 255, 255)'
                               underline='none'
                         >
                         <Typography
                            variant='h6'
                            noWrap
                            component='div'
                            sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
                         >
                             LOGO
                         </Typography>
                         </Link>
                         <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'flex' } }}>
                             {this.pages.map((page) => (
                                 <Link href={page.link}
                                       key={page.key}
                                       color='rgb(225, 225, 225)'
                                       underline='none'
                                 >
                                     <Typography>{page.text}</Typography>
                                 </Link>

                             ))}
                         </Box>
                         <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton sx={{ p: 0 }}>
              </IconButton>
            </Tooltip>
                <Menu
                  sx={{ mt: '45px' }}
                  id="menu-appbar"
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={false}
                  // onClose={}
                >
                  {/*{this.settings.map((setting) => (*/}
                  {/*  <MenuItem key={setting}>*/}
                  {/*    <Typography textAlign="center">{setting}</Typography>*/}
                  {/*  </MenuItem>*/}
                  {/*))}*/}
                </Menu>
                         </Box>
                     </Toolbar>
                 </Container>
            </AppBar>
        )
    }
}
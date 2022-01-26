import React, {useState} from 'react'
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import {type} from "@testing-library/user-event/dist/type";


class Row extends React.Component{

    constructor(props){
        super(props);

        console.log(0)
        this.state = {
            open: false
        }
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return (this.props !== nextProps || this.state !== nextState);
    }

    render() {
      return (
    <React.Fragment>
      <TableRow >
        <TableCell>
          <IconButton sx={{ '& > *': { borderBottom: 'unset' } }}
            id={this.props.announcement_prefix+'_open_button'}
            aria-label="expand row"
            size="small"
            onClick={() => {this.setState({open: !this.state.open})}}
          >
              {this.state.open ? <KeyboardArrowDownIcon/> : <KeyboardArrowUpIcon/>}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {this.props.announcement.title.slice(0, 50)}
        </TableCell>
        <TableCell align="right">{this.props.announcement.description.slice(0, 50)}</TableCell>
        <TableCell align="right">{this.props.announcement.category}</TableCell>
        <TableCell align="right">{this.props.announcement.responses}</TableCell>
        <TableCell align="right">{this.props.announcement.create_date}</TableCell>
      </TableRow>
      {
        <TableRow /*id={`announcementResponse_${}`} ref={response_ref}*/>
        <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>
          <Collapse in={this.state.open} timeout="auto" unmountOnExit>
            <Box sx={{margin: 1}}>
              <Typography variant='h6' gutterBottom component='div'>
                  Полная информация о объявлении
              </Typography>
                <Table size='small' aria-lable='announcemnet'>
                    <TableHead>
                        <TableRow>
                            <TableCell>Заголовок</TableCell>
                            <TableCell>Описание</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        <TableRow>
                            <TableCell>{this.props.announcement.title}</TableCell>
                            <TableCell> {this.props.announcement.description} </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
      }
    </React.Fragment>
  );

  }

}


export default class AnnouncementCollapsibleTable extends React.Component {

    constructor(props) {
        super(props);
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return this.props !== nextProps;
    }

    render() {
      return (
    <TableContainer component={Paper} id='announcements_container' ref={this.props.announcement_ref}>
      <Table aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>Закоговок</TableCell>
            <TableCell align="right">Описание</TableCell>
            <TableCell align="right">Категория</TableCell>
            <TableCell align="right">Клво. отктиков</TableCell>
            <TableCell align="right">Дата публикации</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {this.props.rows.map((row) => {
            const announcement_prefix = `announcement_${row.id}`;
            if(row.responses < 1){
                return (
                    <Row
                        key={announcement_prefix} announcement={row}
                        announcement_prefix={announcement_prefix}
                    />
                    )
            }
            else{
              return (
    <React.Fragment>
      <TableRow >
        <TableCell>
          <IconButton sx={{ '& > *': { borderBottom: 'unset' } }}
            id={announcement_prefix+'_open_button'}
            aria-label="expand row"
            size="small"
            onClick={this.props.open_announcement}
          >
            {this.props.responses_data[row.id].open ?  <KeyboardArrowDownIcon id={announcement_prefix+'_open_svg'}/> : <KeyboardArrowUpIcon id={announcement_prefix+'_open_svg'}/>}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {row.title.slice(0, 50)}
        </TableCell>
        <TableCell align="right">{row.description.slice(0, 50)}</TableCell>
        <TableCell align="right">{row.category}</TableCell>
        <TableCell align="right">{row.responses}</TableCell>
        <TableCell align="right">{row.create_date}</TableCell>
      </TableRow>
      <TableRow /*id={`announcementResponse_${}`} ref={response_ref}*/>
        <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>
          <Collapse in={this.props.responses_data[row.id].open} timeout="auto" mountOnEnter
            id={`${announcement_prefix}_responses_container`} ref={this.props.response_ref}
          >
            <Box sx={{margin: 1}}>
              <Typography variant="h6" gutterBottom component="div">
                Отклики
              </Typography>
              <Table size="small" aria-label="purchases">
                <TableHead>
                  <TableRow>
                    <TableCell>Дата создания</TableCell>
                    <TableCell>Текст</TableCell>
                    <TableCell align="right">Позьлователь</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {this.props.responses_data[row.id].data ? this.props.responses_data[row.id].data.map((response) => (
                    <TableRow>
                      <TableCell component="th" scope="row">
                        {response.create_date}
                      </TableCell>
                      <TableCell>{response.text} </TableCell>
                      <TableCell align="right">{response.user} </TableCell>
                    </TableRow>
                  ))
                  :
                  ''
                  }
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
                )
            }
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}}

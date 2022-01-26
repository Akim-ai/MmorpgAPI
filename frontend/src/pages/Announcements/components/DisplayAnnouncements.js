import React, {createRef, useRef} from "react";
import Box from '@mui/material/Box';
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";

import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import DatePicker from "@mui/lab/DatePicker"
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';

import auth_get_data from "../../../utils/fetch";
import Button from "@mui/material/Button";
import {useLocation, useNavigate} from "react-router-dom";
import { createBrowserHistory } from "history";
import {type} from "@testing-library/user-event/dist/type";


const CATEGORY_CHOICES = [
    { label: 'Танк' },
    { label: 'Хил' },
    { label: 'Демедж Диллер' },
    { label: 'Торговец' },
    { label: 'Гилдмастер' },
    { label: 'Квестгивер' },
    { label: 'Кузнец' },
    { label: 'Кожевник' },
    { label: 'Зельевар' },
    { label: 'Мастер Заклинаний' },

];


function url_change(url_data) {
    console.log(url_data)
    let history = createBrowserHistory()
    history.push(url_data)
}


function Pagination(props) {

    const {
        all_results_cnt,
        current_page, paginated_by
    } = props

    let PAGES = (() => {

        let pages_cnt = all_results_cnt / paginated_by
        if(pages_cnt % 1 > 0){pages_cnt = Math.ceil(pages_cnt)}
        let pages = []
        if(current_page === 1){for (let i = current_page; 5 >= i && i <= pages_cnt; i++) {pages.push(i)}}
        else{
            if(current_page === 2){
                pages.push(1)
                for (let i = current_page; 5 >= i && i <= pages_cnt; i++) {pages.push(i)}
        } else
            {
                if(current_page === pages_cnt) {
                    for (let i = current_page-5; i <= current_page; i++){if(0 < i) {pages.push(i)}}
                }
        else {
            for (let i = current_page-2; i <= pages_cnt && i <= (current_page + 2); i++){if(0 < i){pages.push(i)}}
        }}}

        return pages
    })()


    return (
        <Grid item container
              spacing={{xs: 0.5, sm: 1, md: 1.5}}
              justifyContent='center'
        >
            {current_page !== 1 ? '<' : ''}
            {PAGES.map((page) => {
                return (
                    <Grid item>
                        { page === current_page ?
                            <Typography
                                variant='inherit'
                                component='span'
                                key={`changePage_to-${page}`}
                                id={`changePage_to-${page}`}
                                sx={{
                                    cursor: 'pointer',
                                    color: 'blue',
                                }}
                                gutterBottom
                            >
                                {page}
                            </Typography>
                            :
                            <Typography
                            variant='inherit'
                            component='span'
                            key={`changePage_to-${page}`}
                            id={`changePage_to-${page}`}
                            sx={{
                                cursor: 'pointer',
                                color: 'red',
                                 }}
                            gutterBottom
                            >
                            {page}
                            </Typography>
                        }
                    </Grid>
                )
            })
            }
            {current_page !== 1 ? '>' : ''}
        </Grid>
    )
}


function DatePickerComponent(props) {

    const [date, setDate] = React.useState()

    return (
        <DatePicker
            id={`search_${props.id}_container`}
            disableFuture
            label={props.label}
            value={date}
            onChange={(newDate) => {
              setDate(newDate);
            }}
            onClick={((node) => {node.style = {'borderColor': '#00000'}})}
            renderInput={(params) =>
                <TextField id={props.id} {...params}
                    inputRef={props.set_ref}
                />
            }
        />
        )

}


class AnnouncementFilter extends React.Component{

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return nextProps !== this.props
    }

    render() {
        return (
            <Grid item container
                  id='filters_container'
                  xs={12} sm={12} md={12}
                  alignContent='flex-start'
                  spacing={{xs: 0, sm: 1, md: 2}}
            >
                <Grid item container
                      xs={12} sm={12} md={12}
                      justifyContent='center'
                >
                    <Typography
                        variant='h6'
                        component='div'
                        gutterBottom
                        id={'search-announcement_button-1'}
                    >
                        Поиск
                    </Typography>
                </Grid>
                <Grid item
                >
                    <TextField
                      id="outlined-multiline-static"
                      label="Заголовок"
                      multiline
                      inputRef={this.props.set_ref.title_icontains}
                    />
                </Grid>
                <Grid item
                >
                    <TextField
                        id='search_description'
                        label='Описание'
                        multiline
                        inputRef={this.props.set_ref.description_icontains}
                    />
                </Grid>
                <Grid item
                      xs={12} sm={12} md={12}
                >
                    <Autocomplete
                        disablePortal
                        id='category_choice_container'
                        options={CATEGORY_CHOICES}

                        sx={{
                            width: '100%',
                            height: '100%',
                            boxSizing: 'border-box'
                        }}
                        renderInput={(categories) => <TextField
                            id='category_choice'
                            {...categories} label='Категория'
                            inputRef={this.props.set_ref.category}
                            sx={{width: '100%'}}
                        />}
                    />
                </Grid>
                <Grid item>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <DatePickerComponent
                            id={'date_gte'}
                            set_ref={this.props.set_ref.date_gte}
                            label={'Создано после'}
                        />
                    </LocalizationProvider>

                </Grid>
                <Grid item>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <DatePickerComponent
                            id={'date_lte'}
                            set_ref={this.props.set_ref.date_lte}
                            label={'Создано до'}
                        />
                    </LocalizationProvider>
                </Grid>
                <Grid item container
                      xs={12} sm={12} md={12}
                      justifyContent='center'
                      mt={1}
                >
                    <Button
                        id={'search-announcement_button-2'}
                        sx={{
                            width: '80%'
                        }}
                    >
                        Искать
                    </Button>
                </Grid>
            </Grid>
        )
    }
}


class ShortAnnouncement extends React.Component{

    constructor(props) {
        super(props);
        this.prefix = `announcement_${props.announcement.id}`;

    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return this.props.announcement !== nextProps.announcement;
    }


    render() {
        return (
        <Grid item
              sx={12} sm={12} md={12}
        >
        <Link href={`details/~${this.props.announcement.id}/`} underline='none'>
        <Box id={this.prefix}
          sx={{
              margin: '0 5px 5px 5px',
              boxSizing: 'border-box',
              maxWidth: '99%',
              cursor: 'pointer',
              '&:hover': {
                backgroundColor: 'primary.main',
                opacity: [0.9, 0.8, 0.7],
              }
          }}
             component={Paper}
             onClick={this.props.detail_announcement}
        >
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                }}
                id={`${this.prefix}_title_createDate_container`}

            >
                <Typography
                    variant="h5" gutterBottom component="div"
                    id={`${this.prefix}_title`}
                >
                    {this.props.announcement.title}
                </Typography>
                <Typography
                    variant="subtitle1" gutterBottom component="div"
                    id={`${this.prefix}_createDate`}
                >
                    {this.props.announcement.create_date}
                </Typography>
            </div>
            <Typography
                variant="subtitle1" gutterBottom component="div"
                id={`${this.prefix}_category`}

            >
                {this.props.announcement.category}
            </Typography>
            <Typography
                variant="body1" gutterBottom
                id={`${this.prefix}_description`}
                sx={{
                    paddingBottom: '0.2em'
                }}
            >
                {this.props.announcement.description}
            </Typography>
        </Box>
        </Link>
        </Grid>
    )
}}


class DisplayAnnouncements extends React.Component{

    constructor(props) {
        super(props);

        const page = window.location.search.match(/page=([0-9]*)/m)?.[1]
        const current_page = typeof page !== typeof undefined ? Number(page) : 1;

        this.state = {

            announcements_data: [],
            all_results_cnt: 1,
            results_cnt: 1,
            announcement_next: `http://localhost:8000/api/v1/announcement/?page=${current_page}`,

            page: current_page,
            paginated_by: 1

        }

        const announcement_filtering = [
            'title_icontains', 'description_icontains',
            'category', 'date_lte', 'date_gte'
        ];

        let announcement_filters_dict = {};
        for (const i in announcement_filtering){announcement_filters_dict[announcement_filtering[i]] = createRef();}
        this.announcements_filters = announcement_filters_dict

        console.log(this.announcements_filters)

        this.click_controller = this.click_controller.bind(this);

    }

    componentDidMount() {
        this.get_list_announcement(this.state.announcement_next)
        window.addEventListener('click', this.click_controller)
    }

    componentWillUnmount() {
        window.removeEventListener('click', this.click_controller)
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {

        return (this.props !== nextProps.page || this.state !== nextState)
    }

    get_list_announcement(url) {

        auth_get_data(url)

            .then((data) => {
                console.log(data)
                this.setState({
                    announcement_data: data.results, all_results_cnt: data.count,
                    results_cnt: data.results.length,
                    announcement_next: data.next ? data.next : this.state.announcement_next,
                    paginated_by: data.paginated_by,
                })
            })
    }

    click_controller(event) {

        const id = event.target.id;
        if(id.length <= 0){return}

        if (id.search('changePage_to-') >= 0){this.pagination(id.replace('changePage_to-', ''))}
        else{if(id.search('search-announcement_button') >= 0){this.search_announcements()}}
    }

    pagination(page){

        this.get_list_announcement(this.state.announcement_next.replace(`page=${this.state.page}`, `page=${page}`))
        const { search, pathname } = window.location

        if(search.length > 0) {url_change(`${pathname}${search.replace('page='+this.state.page, `page=${page}`)}`, '');}
        else{url_change(`${pathname}?page=${page}`)}
        this.setState({page: Number(page) })
    }

    search_announcements(){
        console.log('in search')

        for(const i in this.announcements_filters) {
            console.log(this.announcements_filters[i].current.value)
        }
    }


    render() {
        return (
            <Grid container
                  alignContent='center'
                  flexDirection='row'
                  justifyContent='center'
                  wrap
                  mt={{sx:0, sm:1, md: 2}}
                  spacing={{ sx: 1, sm: 1, md: 2}}
            >
                <Grid item
                    xs={12} sm={12} md={2}
                >
                        <AnnouncementFilter set_ref={this.announcements_filters}/>
                </Grid>
                <Grid item container
                      xs={12} sm={12} md={9}
                >
                    {this.state.announcement_data ? this.state.announcement_data.map((announcement) => {
                        return (
                            <ShortAnnouncement
                                announcement={announcement}
                            />
                            )
                    })
                        :
                        <div> </div>
                    }
                </Grid>
                 {this.state.announcement_data ?
                     <Pagination
                         all_results_cnt={this.state.all_results_cnt}
                         current_page={this.state.page}
                         paginated_by={this.state.paginated_by}
                     />
                    :
                     <div> </div>
                 }
            </Grid>
        )
    }
}


export default DisplayAnnouncements
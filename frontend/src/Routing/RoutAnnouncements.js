import React from 'react'
import {Route, Routes} from 'react-router-dom'
import SignIn from "../pages/Sign-in/Sing-in";
import Announcement from "../pages/Announcements/AnnouncementsParent";
import {useLocation} from "react-router";

export default function AnnouncementRout() {

    const { pathname }  = useLocation();
    console.log(pathname.match(/~([0-z]*)/m)?.[1])
    const announcement_id = pathname.match(/~([0-9]*)/m)
    const detail_url = '/details/' + announcement_id?.[0]
    console.log(announcement_id ? <Route path={detail_url} element={<Announcement announcement_id={announcement_id?.[1]}/>}/> : '')

    return (
        <Routes>
            <Route path='/' element={<Announcement/>}/>
            {announcement_id ? <Route path={detail_url} element={<Announcement announcement_id={announcement_id?.[1]}/>}/> : ''}
        </Routes>
    )
}
import React from 'react';
import { /*useLocation, BrowserRouter,*/ Route, Routes } from 'react-router-dom';
import SelfProfile from "../pages/Profile/components/SelfProfile";
import SelfAnnouncements from "../pages/Profile/components/SelfAnnouncements";
import SelfResponses from "../pages/Profile/components/selfResponses";
import ProfileParent from "../pages/Profile/ProfileParent";

export default function ProfileRout() {

    // const { search } = useLocation();

    // const match_profile = search.match(/profile_type=([me|[0-9]*]*)/m)?.[1];
    // const match_page = search.match(/page_type=([a-z]*)/m)?.[1];

    // const me_prefix = '?profile_type=me'
    // const mePages_prefix = me_prefix

    // console.log(match_page, match_profile)

    return (

        <>
            <Routes>
                <Route path='/' element={<ProfileParent/>}/>
                <Route path='/announcements/' element={<SelfAnnouncements/>}/>
                <Route path='/responses/' element={<SelfResponses/>}/>
            </Routes>
        </>

    )
}
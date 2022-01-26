import React from 'react'
import {Route, Routes} from 'react-router-dom'
import SignIn from "../pages/Sign-in/Sing-in";

export default function Rout() {

    return (
        <Routes>
            <Route path='sign-in' element={<SignIn/>}/>
        </Routes>
    )
}
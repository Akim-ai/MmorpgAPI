import React from 'react'

import {Route, BrowserRouter, Routes} from 'react-router-dom'

import ProfileRout from "./Routing/RoutProfile";
import Rout from "./Routing/Rout";
import AnnouncementRout from "./Routing/RoutAnnouncements";
import Header from "./pages/components/header";


function App() {


    return (
        <>
            <Header/>
          <BrowserRouter>
              <Routes>
                  <Route path='profile/*' element={<ProfileRout/>}/>
                  <Route path='announcement/*' element={<AnnouncementRout/>}/>
                  <Route path='*' element={<Rout/>}/>
              </Routes>

          </BrowserRouter>
        </>
  );
}

export default App;

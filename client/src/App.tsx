import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './views/Login'; // adjust the path to your Login component as necessary
import Signup from './views/Signup'
import Home from './views/Home';
import LandingPage from './views/LandingPage'
import Trending from './views/Trending';
import Modules from './views/Modules'
import Contact from './views/Contact'
import Content from './views/Content'
import Issac from './views/Issac'
import Profile from './views/Profile';
import Issac2 from './views/Issac3D'
import 'regenerator-runtime/runtime';
import CourseDetails from './views/CourseDetails';
import "./views/i18n"
import PersonalisedCourses from './views/PersonalisedCourses';
import PerContent from './views/PerContent';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/details" element={<CourseDetails />} />
        <Route path="/home" element={<Home />} />
        <Route path="/trending" element={<Trending />} />
        <Route path="/explore" element={<Modules />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/pers-content" element={<PerContent />} />
        <Route path="/issac" element={<Issac />} />
        {/* <Route path="/issac" element={<Issac2 />} /> */}
        <Route path="/contact" element={<Contact />} />
        <Route path="/trending" element={<Trending />} />
        <Route path="/content" element={<Content />} />
        <Route path="*" element={<Navigate to="/" />} />
        <Route path="/pers-courses" element={<PersonalisedCourses />} />
      </Routes>
    </Router>
  );
}

export default App;
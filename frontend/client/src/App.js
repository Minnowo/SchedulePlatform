//Static imports:
import logo from './logo.svg';

//Component imports:
import Home from "./pages/Home";
import CalendarDL from './pages/CalendarDL';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Calendar from './components/Calendar';

//React & Lib imports:
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";


export default function App() {
  return (
    <Router> 
      <Routes>
      <Route path="/" element={<Home/>}></Route>
      <Route path="/login" element={<Login/>}></Route>
      <Route path="/dl" element={<CalendarDL/>}></Route>
      <Route path="profile" element={<Profile/>}></Route>
      <Route path="calendar" element={<Calendar/>}></Route>
      </Routes>
 </Router>
   );
}

//Static imports:
import logo from './logo.svg';
import './App.css';

//Component imports:
import Home from "./pages/Home";
import CalendarDL from './pages/CalendarDL';

//React & Lib imports:
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";


export default function App() {
  return (
    <Router> 
      <Routes>
      <Route path="/" element={<Home/>}></Route>
      <Route path="/dl" element={<CalendarDL/>}></Route>
      </Routes>
 </Router>
   );
}

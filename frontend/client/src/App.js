//Static imports:
import logo from './logo.svg';
import './App.css';

//Component imports:
import Home from "./components/Home";
import CalendarDL from './components/CalendarDL';

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

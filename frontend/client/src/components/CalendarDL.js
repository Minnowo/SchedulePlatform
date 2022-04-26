import React from 'react'
import { useRef } from 'react';
const CalendarDL = () => {
    //State:
    const confInput = useRef('');
    const crnInput = useRef('');

  function handleSubmit(event) {    
    let config = confInput.current.value;
    let crn = crnInput.current.value;

    //Requesting the API with above parameters:
    fetch('http://localhost:8000')
    .then(response => response.json())
    .then(data => console.log(data));

  }  

  return (
      <div>
    Pls enter your config:
    <input type="text" ref={confInput}></input>
    Enter the crn:
    <input type="text" ref={crnInput}></input>
    <button onClick={handleSubmit}>Submit </button>
    </div>
  );
}

export default CalendarDL
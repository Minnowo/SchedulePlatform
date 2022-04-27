import React from 'react'
import { useRef } from 'react';
const CalendarDL = () => {
    //State:
    const [blobURL,setBlobURL] = React.useState('');

  function RenderLink() {
      if(blobURL !== ''){
        return (
            <a href={blobURL} download="calendar.ics">DOWNLOAD</a>
        )
      } else {
          console.log('nein')
      }
  }  
    //Ref strings:
    const confInput = useRef('');
    const crnInput = useRef('');

  function handleSubmit(event) {    
    let config = confInput.current.value;
    let crn = crnInput.current.value;

    let reqBody = {
        "course_codes": [
        ],
        "crn_codes": [
          70851
        ]
      }


    //URL
    fetch('http://localhost:8000/crn/'+config+'/download' , 

    //Request Parameters
        {
        method: 'POST', // or 'PUT'
        headers: {
        'Content-Type': 'application/json',
        },
    //Post Body to API
        body: JSON.stringify(reqBody),
    })

    .then(response => response.blob())
    .then(data => {
        console.log(data);
        const href = window.URL.createObjectURL(data);
        setBlobURL(href);
        console.log(blobURL);
        RenderLink();
    }).then(
        z => {RenderLink();}
    )
    .catch((error) => {
        console.error('Error:', error);
    });  

  }  

  return (
      <div>
    Pls enter your config:
    <input type="text" ref={confInput}></input>
    Enter the crn:
    <input type="text" ref={crnInput}></input>
    <button onClick={handleSubmit}>Submit </button>
    {RenderLink()}
    </div>
  );
}

export default CalendarDL
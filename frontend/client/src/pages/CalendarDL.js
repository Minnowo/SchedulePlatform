import React from 'react'
import { useRef } from 'react';
import ENDPOINT from '../API';
const CalendarDL = () => {
    //State:
    const [blobURL,setBlobURL] = React.useState('');
    const [errMsg, setErrMsg] = React.useState('');

  //Link render
  function RenderLink() {
      if(blobURL !== ''){
        return (
            <a href={blobURL} download="calendar.ics">DOWNLOAD</a>
        )
      } else if(errMsg !== ''){
        return (
          <p>{errMsg}</p>
        )
      } 
      
      else {
          console.log('nein')
      }
  }  
    //Ref strings:
    const confInput = useRef('');
    const crnInput = useRef('');
    const courseInput = useRef('');

  function handleSubmit(event) {    

    //Stays string
    let config = confInput.current.value;
    let course = courseInput.current.value;
    
    //Parsing CRN input string as list of ints
    let crn = crnInput.current.value.split(',').map(c => parseInt(c));

    //Error handling for it:
    for(const x of crn){
      if(isNaN(x)){
        setErrMsg(`Some of your CRN entries aren't valid`);
        RenderLink();
        return;
       }
    }

    let course_codes = courseInput.current.value;

    console.log(crn);

    for(const x of crn){
      if(isNaN(x)){ console.log('NaN is present')}
    }


    let reqBody = {
        "course_codes": [
        ],
        "crn_codes": [
          70851 , 
        ]
      }


    //URL
    fetch(ENDPOINT+'crn/'+config+'/download' , 

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
        const href = window.URL.createObjectURL(data);
        return setBlobURL(href);
    }).then(
        () => {RenderLink();}
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
    Enter the course codes:
    <input type="text" ref={courseInput}></input>

    <button onClick={handleSubmit}>Submit </button>
    {RenderLink()}
    </div>
  );
}

export default CalendarDL
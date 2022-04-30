import React from 'react'
import { useRef } from 'react';
import ENDPOINT from '../API';

const Login = (props) => {

  //Ref strings:
  const usernameStr = useRef('');
  const passwordStr = useRef('');

  const loginUser = async (event) => {
    
    event.preventDefault()




    const resp = await fetch(ENDPOINT + "auth/token/", 

    //Request Params
    {
      method: 'POST',
      headers: {
        'Content-Type' : 'application/x-www-form-urlencoded' //This is what type FastAPI Login Manager wants
      },
      body: JSON.stringify(
        `grant_type=&username=${usernameStr.current.value}&password=${passwordStr.current.value}&scope=&client_id=&client_secret=`
      ),
    }).then(resp => resp.json()).then(e => console.log(e))


}


  return (
    <div>Login
    <form onSubmit={loginUser}>
        <input type="text"     
            id="login-user" 
            placeholder="Username"
            required=''
            maxLength='29'
            minLength='3'
            ref={usernameStr}>
        </input>

        <input type="text"     
            id="login-pass" 
            placeholder="Password"
            required=''
            maxLength='25'
            minLength='8'
            ref={passwordStr}>
        </input>

        <input type="submit"/>
  </form>
    </div>
  )
}

export default Login
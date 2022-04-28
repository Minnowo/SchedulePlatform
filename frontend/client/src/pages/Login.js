import React from 'react'
import { useRef } from 'react';


const Login = () => {

  //Ref strings:
  const usernameStr = useRef('');
  const passwordStr = useRef('');

  return (
    <div>Login
        <form>

        <input type="text"     
            id="login-user" 
            placeholder="Username"
            required=''
            maxLength='25'
            minLength='3'
            ref={usernameStr}>
        </input>

        <input type="text"     
            id="login-pass" 
            placeholder="Password"
            required=''
            maxLength='25'
            minLength='4'
            ref={passwordStr}>
        </input>

        </form>

    </div>
  )
}

export default Login
import React from 'react'
import ENDPOINT from '../API';
import Cookies from 'universal-cookie';
import { useEffect } from 'react';

const Profile = () => {
  
    const getProfile = async () => {

        console.log(document.cookie)

        const findCookie = (cookieName, cookies) => {
 
            //Split each cookie
            cookies = cookies.split(';');

            cookies = cookies.map(e => {
                return e.trim()
            })


            //Turn into ['key','value'] sub-array (Nested within main cookies arr)
            cookies = cookies.map(e => {
                return e.split('=')
            })
         
            //Search for the requested cookie:
         
            for(let i = 0; i < cookies.length; i++){
                if(cookies[i][0] === cookieName){
                    return cookies[i][1]
                }
            }
         
            return
        }

        const token = findCookie('access_token', document.cookie)
        console.log(token)

        const resp = await fetch(ENDPOINT + "profile/", 

        //Request Params
        {
          method: 'GET',
          headers: {
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer '+token
          }
         
        })
        
        const respJSON = await resp.json();
        console.log(respJSON)
    }   


    useEffect(() => {
        getProfile()
      });


  return (
    <div>Profile</div>
  )
}

export default Profile
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react'
import {Container,Col,Row, Button} from 'react-bootstrap'
import { useEffect } from 'react';

const Calendar = () => {

  const [columnHeader,setColumnHeader] = React.useState([]);
    
  const generateCols = () => {

    //Generation of column headers:

    const head = [
        'Times' , 'Sunday' , 'Monday',
        'Tuesday', 'Wednesday' , 'Thursday',
        'Friday', 'Saturday'
    ]

    let c = []
    for(let i = 0; i < 8; i++){
        c.push(<Col key={i}>{head[i]}</Col>)
    }
    console.log(c)
    setColumnHeader(c);

  }  



  return (
<div>
  <Row>
    {columnHeader}
  </Row>
  <Button variant="primary" onClick={generateCols}>Primary</Button>
</div>
  )
}

export default Calendar
import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Day from "./day";
import { Button } from "@mui/material";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Page({ }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);
  const [days, setDays] = useState([{ id: 0 }]);
  const [nextId, setNextId] = useState(1); // Unique counter for IDs
  // const [calcMethods, setCalcMethods] = useState([]);

  const buttonStyles = {
    backgroundColor: 'white',
    border: '2px solid #0044D4',
    color: '#0044D4',
    transition: 'background-color 0.3s, transform 0.2s ease-in-out',
    cursor: 'pointer',
    '&:hover': {
        backgroundColor: '#4f51b5',
        transform: 'scale(1.05)',
    },
    '&:active': {
        backgroundColor: '#4f51b5',
    },
  };

  const addDay = () => {
    setDays(prevDays => [
      ...prevDays,
      { id: nextId }
    ]);
    setNextId(prevId => prevId + 1);
  };

  const removeDay = (id) => {
    setDays(prevDays => prevDays.filter(day => day.id !== id));
  };

  // const calcAllDays = () => {
  //   calcMethods.forEach((calc) => {
  //     console.log(calc());
  //   });
  // }

  // const updateCalcMethods = (calcFunction) => {
  //   setCalcMethods((prev) => [...prev, calcFunction]);
  // };

  return (
    <div className="reactEntry page">
      <div className="content">
        {days.map(day => (
          <Day key={day.id} id={day.id} onRemove={removeDay} />
        ))}
        <button onClick={addDay}>Add Day</button>
      </div>
      <div style={{width: "30%"}}>
        {/* <Button variant="outlined" className="button" onClick={calcAllDays} sx={buttonStyles}>Check Schedule</Button> */}
        <img src="../static/images/north-campus.png" style={{ width: "100%" }}  alt="post_image" />
      </div>

    </div>
  );

  // <img src={imgUrl} alt="post_image" />
  //     <p>{owner}</p>
}

Page.propTypes = {
};

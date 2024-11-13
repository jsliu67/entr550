import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Day from "./day";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Page({ }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);
  const [days, setDays] = useState([{ id: 0 }]);
  const [nextId, setNextId] = useState(1); // Unique counter for IDs

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


  return (
    <div className="reactEntry">
        <div>
            {days.map(day => (
              <Day key={day.id} id={day.id} onRemove={removeDay} />
            ))}
            <button onClick={addDay}>Add Day</button>
        </div>
    </div>
  );

  // <img src={imgUrl} alt="post_image" />
  //     <p>{owner}</p>
}

Page.propTypes = {
};

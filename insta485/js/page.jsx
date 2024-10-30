import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Input from "./input";
import Class from "./class";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Page({ }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);


  const [classes, setClasses] = useState([    
    new Class(), new Class(), new Class()
  ]);
  const [numClasses, setNumClasses] = useState(3);
  const [times, setTimes] = useState([]);
//   const [next, setNext] = useState("");

    const setClassCallback = (classData, num) => {
      const newClasses = [...classes]; // Use the spread operator to create a shallow copy
      newClasses[num] = classData; // Update the specific index with new class data
      setClasses(newClasses); // Set the state with the new array
    };

    const calculateSchedule = () => {
      for (let i = 0; i < numClasses - 1; i++) {
        let timeBetween = classes[i + 1].start - classes[i].end;
        let timeTaken = times[i];
        if (timeTaken > timeBetween) {
          console.log("bad");
        } else {
          console.log("good");
        }
      }
    };

    const getData = () => {
        let searchString = "";
        classes.map((className, i) => {searchString += className + '+'});
        searchString = searchString.slice(0, -1); 
        console.log(searchString);
        fetch(`/api/data/${searchString}`)
          .then((response) => response.json())
          .then((data) => setTimes(data))
          .catch((error) => console.error('Error fetching data:', error));
    };

  return (
    <div className="reactEntry">
        <div>
            {classes.map((c, index) => (
            <Input key={index} num={index} setClassCallback={setClassCallback} />
            ))}
            <button>Add Class</button>
            <button onClick={getData}>Check Schedule</button>
        </div>
        <div>

        </div>
    </div>
  );

  // <img src={imgUrl} alt="post_image" />
  //     <p>{owner}</p>
}

Page.propTypes = {
};

import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Input from "./input";
import Class from "./class";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Day({ }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);

  const [classes, setClasses] = useState([    
    new Class(), new Class(), new Class()
  ]);
  const [numClasses, setNumClasses] = useState(3);
  const [times, setTimes] = useState([]);
  const [isValid, setIsValid] = useState(0);
//   const [next, setNext] = useState("");

    const setClassCallback = (classData, num) => {
      const newClasses = [...classes]; // Use the spread operator to create a shallow copy
      newClasses[num] = classData; // Update the specific index with new class data
      setClasses(newClasses); // Set the state with the new array
    };

    const calculateSchedule = (timeToDests) => {
      // set default value to true
      setIsValid(2);
      for (let i = 0; i < numClasses - 1; i++) {
        let timeBetween = timeDifferenceInSeconds(classes[i].end, classes[i+1].start);
        console.log(classes[i].end);
        console.log(classes[i+1].start);
        console.log(timeBetween);
        let timeTaken = timeToDests[i];
        
        if (timeBetween < timeTaken) {
          // not enough time between
          setIsValid(1);
        }
      }
    };

    function timeDifferenceInSeconds(t1, t2) {
      const [startHours, startMinutes] = t1.split(":").map(Number);
      const [endHours, endMinutes] = t2.split(":").map(Number);
  
      const startTotalMinutes = startHours * 60 + startMinutes;
      const endTotalMinutes = endHours * 60 + endMinutes;
  
      let diffMinutes = endTotalMinutes - startTotalMinutes;
  
      if (diffMinutes < 0) {
          diffMinutes += 24 * 60; // Add 24 hours in minutes
      }
  
      const diffSeconds = diffMinutes * 60;
      return diffSeconds;
    }

    const tempSetup = () => {
      const newClasses = [
        new Class("BBB", "10:00", "10:01"),
        new Class("DOW", "10:01", "10:02"),
        new Class("GGBL", "10:03", "10:04")
      ];
      setClasses(newClasses);
    }

    const addClass = () => {
      const newClasses = [...classes, new Class()]
      setClasses(newClasses);
      setNumClasses(numClasses + 1);
    }

    const getData = () => {
        let searchString = "";
        classes.map((className, i) => {searchString += className.name + '+'});
        searchString = searchString.slice(0, -1); 
        console.log(searchString);
        fetch(`/api/data/${searchString}`)
          .then((response) => response.json())
          // .then((data) => setTimes(data))
          .then((data) => calculateSchedule(data))
          .catch((error) => console.error('Error fetching data:', error));
        
    };

  return (
    <div className="reactEntry">
        <div>
            {classes.map((c, index) => (
            <Input key={index} num={index} setClassCallback={setClassCallback} />
            ))}
            <button onClick={addClass}>Add Class</button>
            <button onClick={addDay}>Add Day</button>
            <button onClick={tempSetup}>Shortcut Class</button>
            <button onClick={getData}>Check Schedule</button>
        </div>
        <div>
            <a>Schedule</a>
            <div>{isValid == 0 ? "N/A" : (isValid == 1 ? "Bad" : "Good")}</div>
        </div>
    </div>
  );

}
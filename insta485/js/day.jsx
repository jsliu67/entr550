import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Input from "./input";
import Class from "./class";
import { TextField, Button, Box } from "@mui/material";


// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Day({ id, onRemove }) {
    /* Display image and post owner of a single post */
    // const [things, setThings] = useState([]);

    const [classes, setClasses] = useState([
        new Class(), new Class(), new Class()
    ]);
    const [numClasses, setNumClasses] = useState(3);
    const [times, setTimes] = useState([]);
    const [isValid, setIsValid] = useState(0);
    const [badTimes, setBadTimes] = useState([]);

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
    //   const [next, setNext] = useState("");

    const setClassCallback = (classData, num) => {
        const newClasses = [...classes]; // Use the spread operator to create a shallow copy
        newClasses[num] = classData; // Update the specific index with new class data
        setClasses(newClasses); // Set the state with the new array
    };

    const calculateSchedule = (timeToDests) => {
        // set default value to true
        setIsValid(2);
        let newBadTimes = [];
        for (let i = 0; i < numClasses - 1; i++) {
            let timeBetween = timeDifferenceInSeconds(classes[i].end, classes[i + 1].start);
            console.log(classes[i].end);
            console.log(classes[i + 1].start);
            console.log(timeBetween);
            let timeTaken = timeToDests[i];

            if (timeBetween < timeTaken) {
                // not enough time between
                newBadTimes = [
                    ...newBadTimes,
                    { from: classes[i].name, to: classes[i + 1].name, timeBetween: timeBetween, timeTaken: timeTaken }
                ];
                setIsValid(1);
                console.log(newBadTimes)
                // console.log(badTimes)
            }
        }
        setBadTimes(newBadTimes);
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

    const tempSetupBad = () => {
        const newClasses = [
            new Class("BBB", "10:00", "10:01"),
            new Class("DOW", "10:01", "10:02"),
            new Class("GGBL", "10:03", "10:04")
        ];
        setClasses(newClasses);
    }

    const tempSetupGood = () => {
        const newClasses = [
            new Class("BBB", "10:00", "10:01"),
            new Class("DOW", "10:10", "10:12"),
            new Class("GGBL", "10:20", "10:30")
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
        classes.map((className, i) => { searchString += className.name + '+' });
        searchString = searchString.slice(0, -1);
        console.log(searchString);
        fetch(`/api/data/${searchString}`)
            .then((response) => response.json())
            // .then((data) => setTimes(data))
            .then((data) => calculateSchedule(data))
            .catch((error) => console.error('Error fetching data:', error));
        return isValid;
    };


    // useEffect(() => {
    //     // Call passValue once on mount to register the getValue function
    //     updateCalcMethods(getData, id);
    // }, [classes]);

    return (
        <div className="reactEntry day">
            <div className="day-title">     Day {id}</div>
            <div>
                {classes.map((c, index) => (
                    <Input key={index} num={index} setClassCallback={setClassCallback} />
                ))}
                <Button variant="outlined" className="button" onClick={addClass} sx={buttonStyles}>Add Class</Button>
                <Button variant="outlined" className="button" onClick={tempSetupBad} sx={buttonStyles}>Shortcut Class Bad</Button>
                <Button variant="outlined" className="button" onClick={tempSetupGood} sx={buttonStyles}>Shortcut Class Good</Button>
                <Button variant="outlined" className="button" onClick={() => onRemove(id)} sx={buttonStyles}>Remove Day</Button>
            </div>
            <Button variant="outlined" className="button" onClick={getData} sx={buttonStyles}>Check Schedule</Button>
            <div className="schedule-box">
                <a>     Schedule {id}: </a>
                <a>{isValid == 0 ? "_______________" : (isValid == 1 ? "Bad ✘" : "Good ✔")}</a>
                {
                    isValid === 1 && (
                        <div className="issue-breakdown">
                            <p>Issue Breakdown:</p>
                            {badTimes.map((badTime, index) => (
                                <div key={index}>
                                    <p>From: {badTime.from}</p>
                                    <p>To: {badTime.to}</p>
                                    <p>Time between classes: {badTime.timeBetween}</p>
                                    <p>Time to reach destination: {badTime.timeTaken}</p>
                                    <hr />
                                </div>
                            ))}
                        </div>
                    )
                }
            </div>
        </div>
    );

}

Day.propTypes = {
    id: PropTypes.number.isRequired,
    onRemove: PropTypes.func.isRequired,
};
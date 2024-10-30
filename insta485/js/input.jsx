import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Class from "./class";
// import { TimePicker } from '@mui/x-date-pickers/TimePicker';


export default function Input({ num, setClassCallback }) {
    const [thisClass, setThisClass] = useState(new Class('', '', ''));

    const handleInputChange = (field) => (event) => {
        const updatedClass = { ...thisClass, [field]: event.target.value }; // Update the specific field
        setThisClass(updatedClass); // Update state with the new class instance
        setClassCallback(thisClass, num);
    };

    return (
        <div className="reactEntry">
            Class {num}:
            <input
                className="amount-form-single"
                type="text"
                onChange={handleInputChange('name')} // Pass the field name
            />
            Start Time:
            <input
                className="amount-form-single"
                type="time"
                onChange={handleInputChange('start')} // Pass the field name
            />
            End Time:
            <input
                className="amount-form-single"
                type="time"
                onChange={handleInputChange('end')} // Pass the field name
            />
        </div>
    );
}

Input.propTypes = {
    num: PropTypes.number.isRequired,
    setClassCallback: PropTypes.func.isRequired,
};

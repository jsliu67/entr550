import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Class from "./class";
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
// import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { TextField, Button, Box } from "@mui/material";
import Dayjs from 'dayjs';


export default function Input({ num, setClassCallback }) {
    const [thisClass, setThisClass] = useState(new Class('', '', ''));

    const handleInputChange = (field) => (event) => {
        let updatedClass;
        if (field === 'start' || field === 'end') {
            // For start and end times, we update the string value
            const timeString = event ? event.format('HH:mm') : ''; // Convert to string
            updatedClass = new Class(
                thisClass.name,
                field === 'start' ? timeString : thisClass.start,
                field === 'end' ? timeString : thisClass.end
            );
        } else {
            updatedClass = new Class(
                field === 'name' ? event.target.value : thisClass.name,
                thisClass.start,
                thisClass.end
            );
        }
        setThisClass(updatedClass); // Update state with the new class instance
        setClassCallback(updatedClass, num);
    };

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <div className="styled-form">
                <Box className="input-container">
                    <Box className="input-box">
                        <TextField
                            label="Class"
                            value={thisClass.name}
                            onChange={handleInputChange('name')}
                            fullWidth
                            variant="outlined"
                        />
                    </Box>

                    <Box className="input-box">
                        <TimePicker
                            label="Start Time"
                            value={thisClass.start ? Dayjs(thisClass.start) : null} // Convert string to Dayjs
                            onChange={handleInputChange('start')}
                            renderInput={(props) => (
                                <TextField
                                    {...props}
                                    fullWidth
                                    variant="outlined"
                                />
                            )}
                        />
                    </Box>

                    <Box className="input-box">
                        <TimePicker
                            label="End Time"
                            value={thisClass.end ? Dayjs(thisClass.end) : null} // Convert string to Dayjs
                            onChange={handleInputChange('end')}
                            renderInput={(props) => (
                                <TextField
                                    {...props}
                                    fullWidth
                                    variant="outlined"
                                />
                            )}
                        />
                    </Box>
                </Box>
            </div>
        </LocalizationProvider>
    );
}

Input.propTypes = {
    num: PropTypes.number.isRequired,
    setClassCallback: PropTypes.func.isRequired,
};

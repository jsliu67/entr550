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
        // <LocalizationProvider dateAdapter={AdapterDayjs}>
        //     <div className="styled-form" style={{ padding: '16px', maxWidth: '1000px', margin: '0 auto' }}>
        //         <Box display="flex" flexDirection="row" gap={2} alignItems="center">
        //             <Box flex={1}>
        //                 <TextField
        //                     label="Class"
        //                     value={thisClass.name}
        //                     onChange={handleInputChange('name')}
        //                     fullWidth
        //                     variant="outlined"
        //                     sx={{
        //                         '& .MuiInputBase-root': {
        //                             backgroundColor: '#f7f7f7',
        //                             borderRadius: '8px',
        //                         },
        //                         '& .MuiOutlinedInput-root': {
        //                             borderColor: '#ccc',
        //                         },
        //                         '& .MuiOutlinedInput-root.Mui-focused': {
        //                             borderColor: '#3f51b5',
        //                         },
        //                     }}
        //                 />
        //             </Box>

        //             <Box flex={1}>
        //                 <TimePicker
        //                     label="Start Time"
        //                     value={thisClass.start ? Dayjs(thisClass.start) : null} // Convert string to Dayjs
        //                     onChange={handleInputChange('start')}
        //                     sx={{
        //                         '& .MuiInputBase-root': {
        //                             backgroundColor: '#f7f7f7', // Apply background color to TimePicker root
        //                             borderRadius: '8px',
        //                         },
        //                         '& .MuiOutlinedInput-root': {
        //                             borderColor: '#ccc',
        //                         },
        //                         '& .MuiOutlinedInput-root.Mui-focused': {
        //                             borderColor: '#3f51b5',
        //                         },
        //                     }}
        //                     renderInput={(props) => (
        //                         <TextField
        //                             {...props}
        //                             fullWidth
        //                             variant="outlined"
        //                             sx={{
        //                                 '& .MuiInputBase-root': {
        //                                     backgroundColor: '#f7f7f7', // Make sure the inner input field has the same background
        //                                 },
        //                             }}
        //                         />
        //                     )}
        //                 />
        //             </Box>

        //             <Box flex={1}>
        //                 <TimePicker
        //                     label="End Time"
        //                     value={thisClass.end ? Dayjs(thisClass.end) : null} // Convert string to Dayjs
        //                     onChange={handleInputChange('end')}
        //                     sx={{
        //                         '& .MuiInputBase-root': {
        //                             backgroundColor: '#f7f7f7', // Apply background color to TimePicker root
        //                             borderRadius: '8px',
        //                         },
        //                         '& .MuiOutlinedInput-root': {
        //                             borderColor: '#ccc',
        //                         },
        //                         '& .MuiOutlinedInput-root.Mui-focused': {
        //                             borderColor: '#3f51b5',
        //                         },
        //                     }}
        //                     renderInput={(props) => (
        //                         <TextField
        //                             {...props}
        //                             fullWidth
        //                             variant="outlined"
        //                             sx={{
        //                                 '& .MuiInputBase-root': {
        //                                     backgroundColor: '#f7f7f7', // Make sure the inner input field has the same background
        //                                 },
        //                             }}
        //                         />
        //                     )}
        //                 />
        //             </Box>
        //         </Box>
        //     </div>
        // </LocalizationProvider>
        // <div className="reactEntry styled-form">
        //     Class {num}:
        //     <input
        //         className="amount-form-single"
        //         type="text"
        //         value={thisClass.name}
        //         onChange={handleInputChange('name')} // Pass the field name
        //     />
        //     Start Time:
        //     <input
        //         className="amount-form-single time-inputs"
        //         type="time"
        //         value={thisClass.start}
        //         onChange={handleInputChange('start')} // Pass the field name
        //     />
        //     End Time:
        //     <input
        //         className="amount-form-single time-inputs"
        //         type="time"
        //         value={thisClass.end}
        //         onChange={handleInputChange('end')} // Pass the field name
        //     />
        //     <LocalizationProvider dateAdapter={AdapterDayjs}>
        //         <DemoContainer components={['TimePicker']}>
        //             <TimePicker label="Basic time picker" />
        //         </DemoContainer>
        //     </LocalizationProvider>
        // </div>
    );
}

Input.propTypes = {
    num: PropTypes.number.isRequired,
    setClassCallback: PropTypes.func.isRequired,
};

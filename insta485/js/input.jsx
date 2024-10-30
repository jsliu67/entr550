import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

export default function Input({ num }) {
  const [className, setClassName] = useState("");

  return (
    <div className="reactEntry">
        <a>Class {num}</a>
       <input className="amount-form-single" type="text" onChange={num => {
            let tempFoodAmounts = props.foodAmounts
            tempFoodAmounts[props.val] = num.target.value
        }} />
    </div>
  );

  // <img src={imgUrl} alt="post_image" />
  //     <p>{owner}</p>
}

Input.propTypes = {
    num: PropTypes.number.isRequired,
};

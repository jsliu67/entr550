import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Input from "./input";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Page({ }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);
  const [classes, setClasses] = useState([]);
  const [numClasses, setNumClasses] = useState(3);
//   const [next, setNext] = useState("");

  return (
    <div className="reactEntry">
        {classes.map((c) => (
          <Class key={} postUrl={post} />
        ))}
      <Input num={1}></Input>
      {console.log(1)}
    </div>
  );

  // <img src={imgUrl} alt="post_image" />
  //     <p>{owner}</p>
}

Page.propTypes = {
};

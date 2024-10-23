import React from "react"; // , { useState, useEffect }
import PropTypes from "prop-types";

export default function Like({ handleLike, handleUnlike, likesData }) {
  return (
    <div>
      {likesData ? (
        <div className="like-unlike-button">
          {likesData.lognameLikesThis ? (
            <button type="button" className="like-unlike-button" onClick={() => handleUnlike()}>
              Unlike
            </button>
          ) : (
            <button type="button" className="like-unlike-button" onClick={() => handleLike()}>
              Like
            </button>
          )}
        </div>
      ) : (
        0
      )}
      {likesData ? (
        <div>
          {likesData.numLikes} {likesData.numLikes === 1 ? "like" : "likes"}
        </div>
      ) : (
        0
      )}
    </div>
  );
}

Like.propTypes = {
  handleLike: PropTypes.func.isRequired,
  handleUnlike: PropTypes.func.isRequired,
  likesData: PropTypes.object.isRequired,
};

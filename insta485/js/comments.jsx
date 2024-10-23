import React from "react"; // { useState, useEffect }
import PropTypes from "prop-types";
// import { timers } from "cypress/types/jquery";

export default function Comment({ commentsData, handleDeleteComment }) {
  return (
    <div>
      <a href={commentsData.ownerShowUrl}>{commentsData.owner}</a>
      <span className="comment-text"> {commentsData.text}</span>

      {commentsData.lognameOwnsThis ? (
        <div>
          <button
            type="button"
            className="delete-comment-button"
            onClick={() => handleDeleteComment(commentsData.commentid)}
          >
            Delete Comment
          </button>
        </div>
      ) : (
        0
      )}
    </div>
  );
}

Comment.propTypes = {
  commentsData: PropTypes.object.isRequired,
  handleDeleteComment: PropTypes.func.isRequired,
};

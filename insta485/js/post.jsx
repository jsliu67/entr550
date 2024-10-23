import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Comment from "./comments";
import Like from "./likes";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ postUrl }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);
  const [postContent, setPostContent] = useState({});
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    // let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    // console.log(postUrl);
    fetch(postUrl.url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log(data);
        setPostContent(data);
      })

      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      // ignoreStaleRequest = true;
    };
  }, [postUrl]);

  // useEffect(() => {
  //   console.log(postContent.likes);
  // }, [postContent]);

  // const setLikes = (newLikeObject) => {
  //   console.log("TH(ESOHTESO");
  //   setPostContent({...postContent, "likes": newLikeObject});
  //   console.log(postContent);
  // };

  const handleLike = () => {
    if (postContent.likes.lognameLikesThis) {
      return;
    }
    fetch(`/api/v1/likes/?postid=${postContent.postid}`, { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        const newLikeObject = {
          lognameLikesThis: true,
          numLikes: postContent.likes.numLikes + 1,
          url: data.url,
        };
        setPostContent({ ...postContent, likes: newLikeObject });
      })
      .catch((error) => console.log(error));
  };

  const handleUnlike = () => {
    if (!postContent.likes.lognameLikesThis) {
      return;
    }
    fetch(postContent.likes.url, { method: "DELETE" })
      .then(() => {
        const newLikeObject = {
          lognameLikesThis: false,
          numLikes: postContent.likes.numLikes - 1,
          url: null,
        };
        setPostContent({ ...postContent, likes: newLikeObject });
      })
      .catch((error) => console.log(error));
  };

  // const handleDoubleClick = (event) => {
  //   console.log(event);
  // };

  const handleDeleteComment = (commentid) => {
    // if(!commentData.lognameOwnsThis) return;

    const newCommentObject = [];
    let index = -1;
    for (let i = 0; i < postContent.comments.length; i += 1) {
      if (postContent.comments[i].commentid !== commentid) {
        newCommentObject.push(postContent.comments[i]);
        console.log("test");
      } else {
        index = i;
      }
    }
    console.log(newCommentObject);
    if (index === -1) {
      return;
    }

    fetch(postContent.comments[index].url, { method: "DELETE" })
      .then(() => {
        setPostContent({ ...postContent, comments: newCommentObject });
      })
      .catch((error) => console.log(error));
  };

  const handleCommentFormSubmit = (event) => {
    event.preventDefault();
    // post a new comment
    fetch(`/api/v1/comments/?postid=${postContent.postid}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: newComment }),
    })
      .then((response) => response.json())
      .then((data) => {
        setPostContent({
          ...postContent,
          comments: [...postContent.comments, data],
        });
      })
      .catch((error) => console.error(error));
    setNewComment("");
  };

  const handleCommentFormChange = (event) => {
    setNewComment(event.target.value);
  };

  return (
    <div className="post">

      {JSON.stringify(postContent) !== '{}' ? 
        <div>
          <div className="post_header">
            <a href={postContent.ownerShowUrl}>
              <img
                className="header_img"
                src={postContent.ownerImgUrl}
                alt="person-foto"
              />
            </a>
            <a href={postContent.ownerShowUrl}>{postContent.owner}</a>
          </div>

          <a href={postContent.postShowUrl}>
            {moment(postContent.created, "YYYY-MM-DD HH:mm:ss").fromNow()}
          </a>
          <div className="post_image_container">
            <img onDoubleClick={handleLike} src={postContent.imgUrl} alt="foto" />
            {postContent.likes.lognameLikesThis && (
              <div className="heart-animation">❤️</div>
            )}
          </div>
          <div className="Likes">
            <Like
              handleLike={handleLike}
              handleUnlike={handleUnlike}
              postID={postContent.postid}
              likesData={postContent.likes}
            />
          </div>

          <div className="post_comments">
            {postContent.comments.map((comment) => (
              <Comment
                key={comment.commentid}
                commentsData={comment}
                handleDeleteComment={handleDeleteComment}
              />
            ))}
            <form className="comment-form" onSubmit={handleCommentFormSubmit}>
              <input
                type="text"
                value={newComment}
                onChange={handleCommentFormChange}
              />
            </form>
          </div>
        </div> 
        : <div></div>
      }
    </div>
  );
}
Post.propTypes = {
  postUrl: PropTypes.object.isRequired,
};

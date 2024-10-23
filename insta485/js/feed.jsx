import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Feed({ url }) {
  /* Display image and post owner of a single post */
  // const [things, setThings] = useState([]);
  const [posts, setPosts] = useState([]);
  const [next, setNext] = useState("");

  // const [imgUrl, setImgUrl] = useState("");
  // const [owner, setOwner] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          fetch(data.posts, { credentials: "same-origin" })
            .then((response) => {
              if (!response.ok) throw Error(response.statusText);
              return response.json();
            })
            .then((data2) => {
              setPosts(data2.results);
              setNext(data2.next);
            });
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, []);

  // useEffect(() => {
  //   if(next == "") return;
  //   fetch(next, { credentials: "same-origin"})
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setPosts([...posts, ...data.results]);
  //       setNext(data.next);
  //     })
  //     .catch((error) => console.log(error));
  // }, [currPage]);

  const fetchNextPosts = () => {
    if (next === "") return;
    fetch(next, { credentials: "same-origin" })
      .then((response) => response.json())
      .then((data) => {
        setPosts([...posts, ...data.results]);
        setNext(data.next);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div className="reactEntry">
      <InfiniteScroll
        dataLength={posts.length}
        // next={() => setCurrPage(currPage + 1)}
        next={fetchNextPosts}
        hasMore
      >
        {posts.map((post) => (
          <Post key={post.postid} postUrl={post} />
        ))}
      </InfiniteScroll>
      {/* <button onClick={() => setCurrPage(currPage + 1)}>GET MORE</button> */}
    </div>
  );

  // <img src={imgUrl} alt="post_image" />
  //     <p>{owner}</p>
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};

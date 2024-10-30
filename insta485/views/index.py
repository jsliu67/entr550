"""Insta485 index (main) view."""


import pathlib
import uuid
import hashlib
import arrow
import flask
from flask import jsonify
import insta485


insta485.app.secret_key = b'\xa8\xf1\xbbL\xad;\x01\x07\
    x94\xef\x89g\xd4\xc6\xd3\xd1\xaf\xca\xf0K\t\x8c\x00\x00'

def get_data(search_slug):
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM paths;"
    )
    paths = cur.fetchall()


    search = search_slug.split('+')
    print(paths)
    times = []

    for i in range(len(search) - 1):
        path_found = False
        for path in paths:
            if path['loc1'] == search[i] and path['loc2'] == search[i + 1] or path['loc1'] == search[i + 1] and path['loc2'] == search[i]:
                times.append(path['time_seconds'])
                path_found = True
                break
        if not path_found:
            times.append(-1)
            print(f"error, path not found between `{search[i]}` and `{search[i + 1]}`")
    
    print("times", times)
    return times

@insta485.app.route('/api/data/<search_slug>', methods=['GET'])
def fetch_data(search_slug):
    data = get_data(search_slug)
    return jsonify(data)

@insta485.app.route('/')
def show_index():
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # cur = connection.execute(
    #     "SELECT DISTINCT postid, filename, owner, "
    #     "posts.created, following.username2 FROM posts "
    #     "JOIN following ON following.username2 = posts.owner "
    #     "where following.username1 = ? OR posts.owner = ? "
    #     "ORDER BY postid DESC;",
    #     (user, user)
    # )
    # post_ids = cur.fetchall()

    # Add database info to context

    context = {
        # "logname": user
    }
    posts = []
    return flask.render_template("index.html", **context)



# @insta485.app.route('/users/<user_url_slug>/')
# def user_slug(user_url_slug):
#     """USER USER."""
#     # if user_url_slug not in
#     if "user" in flask.session:
#         user = flask.session["user"]

#         # Connect to database
#         connection = insta485.model.get_db()

#         # Query database
#         cur = connection.execute(
#             "SELECT DISTINCT postid, filename, owner, created FROM posts "
#             "WHERE owner = ?;",
#             (user_url_slug,)
#         )
#         post_ids = cur.fetchall()

#         cur = connection.execute(
#             "SELECT username1 FROM following "
#             "where username2 = ?;",
#             (user_url_slug,)
#         )
#         followers_val = cur.fetchall()

#         cur = connection.execute(
#             "SELECT username1 FROM following "
#             "WHERE username1 = ?;",
#             (user_url_slug,)
#         )
#         following_val = cur.fetchall()

#         cur = connection.execute(
#             "SELECT fullname FROM users "
#             "where username = ?;",
#             (user_url_slug,)
#         )
#         users = cur.fetchall()

#         context = {
#             "logname": user
#         }

#         cur = connection.execute(
#                 "SELECT * FROM following "
#                 "WHERE username1 = ? AND username2 = ?",
#                 (user, user_url_slug, )
#         )
#         follows_query = cur.fetchall()

#         # Should be 1 if logged user follows, should be 0 otherwise
#         if len(follows_query):
#             context['logname_follows_username'] = True
#         else:
#             context['logname_follows_username'] = False

#         context["username"] = user_url_slug
#         context["total_posts"] = len(post_ids)
#         context["followers"] = len(followers_val)
#         context["following"] = len(following_val)
#         context["fullname"] = users[0]["fullname"]

#         posts = [{"postid": post["postid"],
#                   "img_url": post["filename"]} for post in post_ids]
#         context["posts"] = posts

#         return flask.render_template("user.html", **context)

#     return flask.redirect(flask.url_for('login'))


# @insta485.app.route('/users/<user_url_slug>/followers/')
# def followers(user_url_slug):
#     """FOLLOWERS FOLLOWERS."""
#     if "user" in flask.session:
#         user = flask.session["user"]

#         # Connect to database
#         connection = insta485.model.get_db()

#         cur = connection.execute(
#             "SELECT * FROM users WHERE username = ?;",
#             (user_url_slug,)
#         )
#         not_existent = cur.fetchall()
#         if not not_existent:
#             # If user_url_slug is not in the database
#             flask.abort(404)

#         # Query database
#         cur = connection.execute(
#             "SELECT username1 FROM following WHERE username2 = ?",
#             (user_url_slug,)
#         )
#         followers_val = cur.fetchall()

#         context = {
#             "logname": user
#         }

#         context["followers"] = []
#         for follower in followers_val:
#             cur = connection.execute(
#                 "SELECT filename FROM users "
#                 "WHERE username = ?;",
#                 (follower["username1"],)
#             )
#             profile_pic = cur.fetchall()

#             cur = connection.execute(
#                 "SELECT * FROM following "
#                 "WHERE username1 = ? AND username2 = ?",
#                 (user, follower['username1'], )
#             )
#             follows_query = cur.fetchall()

#             temp = {}
#             temp['username'] = follower['username1']
#             temp['user_img_url'] = profile_pic[0]['filename']
#             temp['currentUser'] = user_url_slug

#             # Should be 1 if logged user follows, should be 0 otherwise
#             if len(follows_query):
#                 temp['logname_follows_username'] = True
#             else:
#                 temp['logname_follows_username'] = False

#             context['followers'].append(temp)

#         return flask.render_template('followers.html', **context)

#     return flask.redirect(flask.url_for('login'))


# @insta485.app.route('/users/<user_url_slug>/following/')
# def following(user_url_slug):
#     """FOLLOWING FOLLOWING."""
#     if "user" in flask.session:
#         user = flask.session["user"]

#         # Connect to database
#         connection = insta485.model.get_db()

#         cur = connection.execute(
#             "SELECT * FROM users WHERE username = ?;",
#             (user_url_slug,)
#         )
#         not_existent = cur.fetchall()
#         if not not_existent:
#             # If user_url_slug is not in the database
#             flask.abort(404)

#         # Query database
#         cur = connection.execute(
#             "SELECT username2 FROM following WHERE username1 = ?",
#             (user_url_slug,)
#         )
#         followings = cur.fetchall()

#         context = {
#             "logname": user
#         }
#         context["following"] = []

#         for following_val in followings:
#             cur = connection.execute(
#                 "SELECT filename FROM users "
#                 "WHERE username = ?;",
#                 (following_val["username2"],)
#             )
#             profile_pic = cur.fetchall()

#             cur = connection.execute(
#                 "SELECT * FROM following "
#                 "WHERE username1 = ? AND username2 = ?",
#                 (user, following_val['username2'], )
#             )
#             follows_query = cur.fetchall()

#             temp = {}
#             temp['username'] = following_val['username2']
#             temp['user_img_url'] = profile_pic[0]['filename']
#             temp['currentUser'] = user_url_slug

#             # Should be 1 if logged user follows, should be 0 otherwise
#             if len(follows_query):
#                 temp['logname_follows_username'] = True
#             else:
#                 temp['logname_follows_username'] = False

#             context['following'].append(temp)

#         return flask.render_template('following.html', **context)

#     return flask.redirect(flask.url_for('login'))


# @insta485.app.route('/posts/<postid_url_slug>/')
# def post_id(postid_url_slug):
#     """POSTID POSTID."""
#     # postid_url_slug is just the postid
#     if "user" in flask.session:
#         user = flask.session["user"]
#         connection = insta485.model.get_db()
#         cur = connection.execute(
#             "SELECT * FROM posts WHERE postid = ?",
#             (postid_url_slug,)
#         )
#         post_info = cur.fetchall()

#         if len(post_info) == 0:
#             # Post does not exist
#             return flask.redirect(flask.url_for('show_index'))

#         cur = connection.execute(
#                 "SELECT filename FROM users "
#                 "WHERE username=?;",
#                 (post_info[0]['owner'],)
#         )
#         owner_img_url = cur.fetchall()

#         cur = connection.execute(
#                 "SELECT likeid, owner, postid, created FROM likes "
#                 "WHERE postid=?;",
#                 (postid_url_slug,)
#         )
#         likes = cur.fetchall()

#         context = {
#             "logname": user
#         }
#         context["owner"] = post_info[0]["owner"]
#         context["img_url"] = post_info[0]["filename"]
#         context["owner_img_url"] = owner_img_url[0]["filename"]
#         context["postid"] = postid_url_slug
#         context['likes'] = len(likes)

#         time = arrow.get(post_info[0]["created"], 'YYYY-MM-DD HH:mm:ss')
#         context["timestamp"] = time.humanize()

#         # Comments
#         cur = connection.execute(
#                 "SELECT commentid, owner, postid, text, created FROM comments "
#                 "where postid=? "
#                 "ORDER BY commentid;",
#                 (postid_url_slug,)
#             )

#         context['comments'] = cur.fetchall()

#         cur = connection.execute(
#             "SELECT * FROM likes "
#             "WHERE owner=? AND postid=?",
#             (user, postid_url_slug,)
#         )

#         liked = cur.fetchall()
#         if len(liked):
#             context['liked'] = False
#         else:
#             context['liked'] = True

#         return flask.render_template("post.html", **context)

#     return flask.redirect(flask.url_for('login'))


# @insta485.app.route('/explore/')
# def explore():
#     """EXPLORE EXPLORE."""
#     if "user" in flask.session:
#         # Icon
#         # Username with link to /users/<user_url_slug>/
#         # “follow” button, See above for HTML form
#         user = flask.session["user"]

#         # Connect to database
#         connection = insta485.model.get_db()
#         # Query database
#         # Want to pull username and images of people that user does not follow

#         cur = connection.execute(
#             "SELECT DISTINCT username, filename as user_img_url FROM users "
#         )
#         users = cur.fetchall()

#         cur = connection.execute(
#             "SELECT DISTINCT username2 FROM following "
#             "WHERE username1 = ?;",
#             (user,)
#         )
#         to_delete = cur.fetchall()

#         names = [user_block for user_block in users if (
#             {"username2": user_block['username']} not in to_delete)
#             and (user_block['username'] != user)]
#         context = {
#             "logname": user,
#             "not_following": names
#         }

#         return flask.render_template("explore.html", **context)

#     return flask.redirect(flask.url_for('login'))


# @insta485.app.route('/accounts/login/')
# def login():
#     """LOGIN LOGIN."""
#     # If logged in
#     if "user" in flask.session:
#         return flask.redirect(flask.url_for('show_index'))

#     context = {}
#     return flask.render_template("login.html", **context)


# @insta485.app.route('/accounts/logout/', methods=['POST'])
# def logout():
#     """LOGOUT LOGOUT."""
#     # remove user from session
#     flask.session.pop('user', None)
#     return flask.redirect(flask.url_for('login'))


# @insta485.app.route('/accounts/create/')
# def create():
#     """CREATE CREATE."""
#     if "user" in flask.session:
#         return flask.redirect(flask.url_for('edit'))

#     context = {}
#     return flask.render_template("create.html", **context)


# @insta485.app.route('/accounts/password/')
# def password():
#     """PASSWORD PASSWORD."""
#     user = flask.session["user"]
#     context = {
#         "logname": user
#     }
#     return flask.render_template('password.html', **context)


# @insta485.app.route('/accounts/edit/')
# def edit():
#     """EDIT EDIT."""
#     # If logged in
#     if "user" in flask.session:
#         user = flask.session["user"]
#         connection = insta485.model.get_db()

#         cur = connection.execute(
#             "SELECT * FROM users WHERE username == ?;",
#             (user, )
#         )
#         user_info = cur.fetchall()

#         context = {
#             "logname": user
#         }

#         context["fullname"] = user_info[0]["fullname"]
#         context["email"] = user_info[0]["email"]
#         return flask.render_template("edit.html", **context)

#     context = {}
#     return flask.render_template("login.html", **context)


# @insta485.app.route('/accounts/delete/')
# def delete():
#     """DELETE DELETE."""
#     if "user" in flask.session:
#         user = flask.session["user"]
#         context = {
#             "logname": user,
#             "username": user
#         }
#         return flask.render_template("delete.html", **context)

#     context = {}
#     return flask.render_template("login.html", **context)


# def accounts_redirect_login(connection):
#     """ACCOUNTS REDIRECT LOGIN."""
#     user = flask.request.form['username']
#     # Checking if the user exists in the database
#     password_val = flask.request.form['password']

#     cur = connection.execute(
#         "SELECT password FROM users WHERE username =?;",
#         (user, )
#     )
#     temp = cur.fetchall()

#     if len(temp) == 0:
#         flask.abort(403)

#     password_in_database = temp[0]["password"]
#     hashed_password = hash_password(
#         password_val, password_in_database=password_in_database)

#     if len(user) == 0 or len(password_val) == 0:
#         flask.abort(400)

#     cur = connection.execute(
#         "SELECT * FROM users WHERE username ==? AND password ==?;",
#         (user, hashed_password)
#     )
#     if len(cur.fetchall()) == 0:
#         flask.abort(403)

#     flask.session['user'] = user
#     flask.session['password'] = hashed_password

#     # Had to hard code this to pass
#     # tests/app_tests/test_login_logout.py::test_login
#     # For some reason the target isnt being set in login.html to '/'


# def accounts_redirect_create(connection):
#     """ACCOUNTS REDIRECT CREATE."""
#     # Save profile picture
#     user = flask.request.form['username']
#     password_val = flask.request.form['password']
#     hashed = hash_password(password_val)
#     fileobj = flask.request.files["file"]
#     filename = fileobj.filename
#     fullname = flask.request.form['fullname']
#     email = flask.request.form['email']
#     if len(filename) == 0 or len(fullname) == 0 or len(email) == 0:
#         flask.abort(400)

#     # Check if user already in database
#     cur = connection.execute(
#         "SELECT * FROM users WHERE username ==?;",
#         (user, )
#     )
#     user_info = cur.fetchall()
#     if len(user_info) > 0:
#         flask.abort(409)

#     stem = uuid.uuid4().hex
#     suffix = pathlib.Path(filename).suffix.lower()
#     uuid_basename = f"{stem}{suffix}"

#     # Save to disk
#     path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
#     fileobj.save(path)

#     connection.execute(
#         "INSERT INTO users(username, password, fullname, email, filename) "
#         "VALUES (?,?,?,?,?);",
#         (user, hashed, fullname, email, uuid_basename)
#     )
#     # target = '/'
#     flask.session['user'] = user
#     flask.session['password'] = hashed


# def accounts_redirect_delete(connection):
#     """ACCOUNTS REDIRECT DELETE."""
#     if not flask.session['user']:
#         flask.abort(403)

#     user = flask.session['user']

#     cur = connection.execute(
#         "SELECT filename FROM users WHERE username = ?;",
#         (user, )
#     )
#     user_info = cur.fetchall()
#     filename = user_info[0]["filename"]
#     pathlib.Path.unlink(insta485.app.config["UPLOAD_FOLDER"]/filename)

#     # if os.path.exists(filename):
#     #     print(f"Removed {filename}")
#     #     os.remove(filename)
#     # else:
#     #     #flask.abort(404)
#     #     print(f"{filename} does not exist")

#     # Delete all post files
#     cur = connection.execute(
#         "SELECT filename FROM posts WHERE owner = ?;",
#         (user,)
#     )
#     post_files = cur.fetchall()
#     for post_file in post_files:
#         filename = post_file["filename"]
#         pathlib.Path.unlink(insta485.app.config["UPLOAD_FOLDER"]/filename)
#         # if os.path.exists(filename):
#         #     print(f"Removed {filename}")
#         #     os.remove(filename)
#         # else:
#         #     #flask.abort(404)
#         #     print(f"{filename} does not exist")

#     connection.execute(
#         "DELETE FROM users WHERE username ==?;",
#         (user,)
#     )

#     # Clear users session
#     flask.session.pop('user', None)
#     flask.session.pop('password', None)


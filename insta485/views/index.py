"""Insta485 index (main) view."""


import pathlib
import uuid
import hashlib
import arrow
import flask
import insta485


insta485.app.secret_key = b'\xa8\xf1\xbbL\xad;\x01\x07\
    x94\xef\x89g\xd4\xc6\xd3\xd1\xaf\xca\xf0K\t\x8c\x00\x00'


def hash_password(password_val, password_in_database=None):
    """HASHING HASHING."""
    if password_in_database is None:
        return hash_password_impl(password_val)

    algorithm, salt, _ = password_in_database.split('$')
    return hash_password_impl(password_val, algorithm, salt)


def hash_password_impl(password_val, algorithm=None, salt=None):
    """HASHING HASHING."""
    if salt is None or algorithm is None:
        algorithm = 'sha512'
        salt = uuid.uuid4().hex

    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password_val
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """DOWNLOAD DOWNLOAD."""
    if "user" not in flask.session:
        flask.abort(403)

    return flask.send_from_directory(
        insta485.app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if "user" in flask.session:
        user = flask.session["user"]

        # Connect to database
        connection = insta485.model.get_db()

        # Query database
        cur = connection.execute(
            "SELECT DISTINCT postid, filename, owner, "
            "posts.created, following.username2 FROM posts "
            "JOIN following ON following.username2 = posts.owner "
            "where following.username1 = ? OR posts.owner = ? "
            "ORDER BY postid DESC;",
            (user, user)
        )
        post_ids = cur.fetchall()

        # Add database info to context

        context = {
            "logname": user
        }
        posts = []
        for post in post_ids:
            new_post = {}
            new_post['postid'] = post['postid']
            new_post['owner'] = post['username2']
            new_post['img_url'] = post['filename']

            time = arrow.get(post['created'], 'YYYY-MM-DD HH:mm:ss')
            new_post['timestamp'] = time.humanize()

            cur = connection.execute(
                "SELECT filename FROM users "
                "WHERE username=?;",
                (post['username2'],)
            )
            prof_pic = cur.fetchall()

            new_post['owner_img_url'] = prof_pic[0]['filename']

            cur = connection.execute(
                "SELECT likeid, owner, postid, created FROM likes "
                "WHERE postid=?;",
                (post['postid'],)
            )
            likes = cur.fetchall()
            new_post['likes'] = len(likes)

            cur = connection.execute(
                "SELECT commentid, owner, postid, text, created FROM comments "
                "where postid=? "
                "ORDER BY commentid;",
                (post['postid'],)
            )

            new_post['comments'] = cur.fetchall()

            cur = connection.execute(
                "SELECT * FROM likes "
                "WHERE owner=? AND postid=?",
                (user, post['postid'],)
            )

            liked = cur.fetchall()
            if len(liked):
                new_post['liked'] = False
            else:
                new_post['liked'] = True

            posts.append(new_post)

        context['posts'] = posts

        return flask.render_template("index.html", **context)

    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/users/<user_url_slug>/')
def user_slug(user_url_slug):
    """USER USER."""
    # if user_url_slug not in
    if "user" in flask.session:
        user = flask.session["user"]

        # Connect to database
        connection = insta485.model.get_db()

        # Query database
        cur = connection.execute(
            "SELECT DISTINCT postid, filename, owner, created FROM posts "
            "WHERE owner = ?;",
            (user_url_slug,)
        )
        post_ids = cur.fetchall()

        cur = connection.execute(
            "SELECT username1 FROM following "
            "where username2 = ?;",
            (user_url_slug,)
        )
        followers_val = cur.fetchall()

        cur = connection.execute(
            "SELECT username1 FROM following "
            "WHERE username1 = ?;",
            (user_url_slug,)
        )
        following_val = cur.fetchall()

        cur = connection.execute(
            "SELECT fullname FROM users "
            "where username = ?;",
            (user_url_slug,)
        )
        users = cur.fetchall()

        context = {
            "logname": user
        }

        cur = connection.execute(
                "SELECT * FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (user, user_url_slug, )
        )
        follows_query = cur.fetchall()

        # Should be 1 if logged user follows, should be 0 otherwise
        if len(follows_query):
            context['logname_follows_username'] = True
        else:
            context['logname_follows_username'] = False

        context["username"] = user_url_slug
        context["total_posts"] = len(post_ids)
        context["followers"] = len(followers_val)
        context["following"] = len(following_val)
        context["fullname"] = users[0]["fullname"]

        posts = [{"postid": post["postid"],
                  "img_url": post["filename"]} for post in post_ids]
        context["posts"] = posts

        return flask.render_template("user.html", **context)

    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/users/<user_url_slug>/followers/')
def followers(user_url_slug):
    """FOLLOWERS FOLLOWERS."""
    if "user" in flask.session:
        user = flask.session["user"]

        # Connect to database
        connection = insta485.model.get_db()

        cur = connection.execute(
            "SELECT * FROM users WHERE username = ?;",
            (user_url_slug,)
        )
        not_existent = cur.fetchall()
        if not not_existent:
            # If user_url_slug is not in the database
            flask.abort(404)

        # Query database
        cur = connection.execute(
            "SELECT username1 FROM following WHERE username2 = ?",
            (user_url_slug,)
        )
        followers_val = cur.fetchall()

        context = {
            "logname": user
        }

        context["followers"] = []
        for follower in followers_val:
            cur = connection.execute(
                "SELECT filename FROM users "
                "WHERE username = ?;",
                (follower["username1"],)
            )
            profile_pic = cur.fetchall()

            cur = connection.execute(
                "SELECT * FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (user, follower['username1'], )
            )
            follows_query = cur.fetchall()

            temp = {}
            temp['username'] = follower['username1']
            temp['user_img_url'] = profile_pic[0]['filename']
            temp['currentUser'] = user_url_slug

            # Should be 1 if logged user follows, should be 0 otherwise
            if len(follows_query):
                temp['logname_follows_username'] = True
            else:
                temp['logname_follows_username'] = False

            context['followers'].append(temp)

        return flask.render_template('followers.html', **context)

    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/users/<user_url_slug>/following/')
def following(user_url_slug):
    """FOLLOWING FOLLOWING."""
    if "user" in flask.session:
        user = flask.session["user"]

        # Connect to database
        connection = insta485.model.get_db()

        cur = connection.execute(
            "SELECT * FROM users WHERE username = ?;",
            (user_url_slug,)
        )
        not_existent = cur.fetchall()
        if not not_existent:
            # If user_url_slug is not in the database
            flask.abort(404)

        # Query database
        cur = connection.execute(
            "SELECT username2 FROM following WHERE username1 = ?",
            (user_url_slug,)
        )
        followings = cur.fetchall()

        context = {
            "logname": user
        }
        context["following"] = []

        for following_val in followings:
            cur = connection.execute(
                "SELECT filename FROM users "
                "WHERE username = ?;",
                (following_val["username2"],)
            )
            profile_pic = cur.fetchall()

            cur = connection.execute(
                "SELECT * FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (user, following_val['username2'], )
            )
            follows_query = cur.fetchall()

            temp = {}
            temp['username'] = following_val['username2']
            temp['user_img_url'] = profile_pic[0]['filename']
            temp['currentUser'] = user_url_slug

            # Should be 1 if logged user follows, should be 0 otherwise
            if len(follows_query):
                temp['logname_follows_username'] = True
            else:
                temp['logname_follows_username'] = False

            context['following'].append(temp)

        return flask.render_template('following.html', **context)

    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/posts/<postid_url_slug>/')
def post_id(postid_url_slug):
    """POSTID POSTID."""
    # postid_url_slug is just the postid
    if "user" in flask.session:
        user = flask.session["user"]
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT * FROM posts WHERE postid = ?",
            (postid_url_slug,)
        )
        post_info = cur.fetchall()

        if len(post_info) == 0:
            # Post does not exist
            return flask.redirect(flask.url_for('show_index'))

        cur = connection.execute(
                "SELECT filename FROM users "
                "WHERE username=?;",
                (post_info[0]['owner'],)
        )
        owner_img_url = cur.fetchall()

        cur = connection.execute(
                "SELECT likeid, owner, postid, created FROM likes "
                "WHERE postid=?;",
                (postid_url_slug,)
        )
        likes = cur.fetchall()

        context = {
            "logname": user
        }
        context["owner"] = post_info[0]["owner"]
        context["img_url"] = post_info[0]["filename"]
        context["owner_img_url"] = owner_img_url[0]["filename"]
        context["postid"] = postid_url_slug
        context['likes'] = len(likes)

        time = arrow.get(post_info[0]["created"], 'YYYY-MM-DD HH:mm:ss')
        context["timestamp"] = time.humanize()

        # Comments
        cur = connection.execute(
                "SELECT commentid, owner, postid, text, created FROM comments "
                "where postid=? "
                "ORDER BY commentid;",
                (postid_url_slug,)
            )

        context['comments'] = cur.fetchall()

        cur = connection.execute(
            "SELECT * FROM likes "
            "WHERE owner=? AND postid=?",
            (user, postid_url_slug,)
        )

        liked = cur.fetchall()
        if len(liked):
            context['liked'] = False
        else:
            context['liked'] = True

        return flask.render_template("post.html", **context)

    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/explore/')
def explore():
    """EXPLORE EXPLORE."""
    if "user" in flask.session:
        # Icon
        # Username with link to /users/<user_url_slug>/
        # “follow” button, See above for HTML form
        user = flask.session["user"]

        # Connect to database
        connection = insta485.model.get_db()
        # Query database
        # Want to pull username and images of people that user does not follow

        cur = connection.execute(
            "SELECT DISTINCT username, filename as user_img_url FROM users "
        )
        users = cur.fetchall()

        cur = connection.execute(
            "SELECT DISTINCT username2 FROM following "
            "WHERE username1 = ?;",
            (user,)
        )
        to_delete = cur.fetchall()

        names = [user_block for user_block in users if (
            {"username2": user_block['username']} not in to_delete)
            and (user_block['username'] != user)]
        context = {
            "logname": user,
            "not_following": names
        }

        return flask.render_template("explore.html", **context)

    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/accounts/login/')
def login():
    """LOGIN LOGIN."""
    # If logged in
    if "user" in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    context = {}
    return flask.render_template("login.html", **context)


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """LOGOUT LOGOUT."""
    # remove user from session
    flask.session.pop('user', None)
    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/accounts/create/')
def create():
    """CREATE CREATE."""
    if "user" in flask.session:
        return flask.redirect(flask.url_for('edit'))

    context = {}
    return flask.render_template("create.html", **context)


@insta485.app.route('/accounts/password/')
def password():
    """PASSWORD PASSWORD."""
    user = flask.session["user"]
    context = {
        "logname": user
    }
    return flask.render_template('password.html', **context)


@insta485.app.route('/accounts/edit/')
def edit():
    """EDIT EDIT."""
    # If logged in
    if "user" in flask.session:
        user = flask.session["user"]
        connection = insta485.model.get_db()

        cur = connection.execute(
            "SELECT * FROM users WHERE username == ?;",
            (user, )
        )
        user_info = cur.fetchall()

        context = {
            "logname": user
        }

        context["fullname"] = user_info[0]["fullname"]
        context["email"] = user_info[0]["email"]
        return flask.render_template("edit.html", **context)

    context = {}
    return flask.render_template("login.html", **context)


@insta485.app.route('/accounts/delete/')
def delete():
    """DELETE DELETE."""
    if "user" in flask.session:
        user = flask.session["user"]
        context = {
            "logname": user,
            "username": user
        }
        return flask.render_template("delete.html", **context)

    context = {}
    return flask.render_template("login.html", **context)


def accounts_redirect_login(connection):
    """ACCOUNTS REDIRECT LOGIN."""
    user = flask.request.form['username']
    # Checking if the user exists in the database
    password_val = flask.request.form['password']

    cur = connection.execute(
        "SELECT password FROM users WHERE username =?;",
        (user, )
    )
    temp = cur.fetchall()

    if len(temp) == 0:
        flask.abort(403)

    password_in_database = temp[0]["password"]
    hashed_password = hash_password(
        password_val, password_in_database=password_in_database)

    if len(user) == 0 or len(password_val) == 0:
        flask.abort(400)

    cur = connection.execute(
        "SELECT * FROM users WHERE username ==? AND password ==?;",
        (user, hashed_password)
    )
    if len(cur.fetchall()) == 0:
        flask.abort(403)

    flask.session['user'] = user
    flask.session['password'] = hashed_password

    # Had to hard code this to pass
    # tests/app_tests/test_login_logout.py::test_login
    # For some reason the target isnt being set in login.html to '/'


def accounts_redirect_create(connection):
    """ACCOUNTS REDIRECT CREATE."""
    # Save profile picture
    user = flask.request.form['username']
    password_val = flask.request.form['password']
    hashed = hash_password(password_val)
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    if len(filename) == 0 or len(fullname) == 0 or len(email) == 0:
        flask.abort(400)

    # Check if user already in database
    cur = connection.execute(
        "SELECT * FROM users WHERE username ==?;",
        (user, )
    )
    user_info = cur.fetchall()
    if len(user_info) > 0:
        flask.abort(409)

    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)

    connection.execute(
        "INSERT INTO users(username, password, fullname, email, filename) "
        "VALUES (?,?,?,?,?);",
        (user, hashed, fullname, email, uuid_basename)
    )
    # target = '/'
    flask.session['user'] = user
    flask.session['password'] = hashed


def accounts_redirect_delete(connection):
    """ACCOUNTS REDIRECT DELETE."""
    if not flask.session['user']:
        flask.abort(403)

    user = flask.session['user']

    cur = connection.execute(
        "SELECT filename FROM users WHERE username = ?;",
        (user, )
    )
    user_info = cur.fetchall()
    filename = user_info[0]["filename"]
    pathlib.Path.unlink(insta485.app.config["UPLOAD_FOLDER"]/filename)

    # if os.path.exists(filename):
    #     print(f"Removed {filename}")
    #     os.remove(filename)
    # else:
    #     #flask.abort(404)
    #     print(f"{filename} does not exist")

    # Delete all post files
    cur = connection.execute(
        "SELECT filename FROM posts WHERE owner = ?;",
        (user,)
    )
    post_files = cur.fetchall()
    for post_file in post_files:
        filename = post_file["filename"]
        pathlib.Path.unlink(insta485.app.config["UPLOAD_FOLDER"]/filename)
        # if os.path.exists(filename):
        #     print(f"Removed {filename}")
        #     os.remove(filename)
        # else:
        #     #flask.abort(404)
        #     print(f"{filename} does not exist")

    connection.execute(
        "DELETE FROM users WHERE username ==?;",
        (user,)
    )

    # Clear users session
    flask.session.pop('user', None)
    flask.session.pop('password', None)


@insta485.app.route('/accounts/', methods=['POST'])
def accounts_redirect():
    """ACCOUNTS ACCOUNTS."""
    target = flask.request.args.get('target')
    connection = insta485.model.get_db()

    if target is None:
        target = '/'

    if flask.request.form['operation'] == 'login':
        accounts_redirect_login(connection)

    elif flask.request.form['operation'] == 'create':
        accounts_redirect_create(connection)

    elif flask.request.form['operation'] == 'delete':
        print(target)
        accounts_redirect_delete(connection)

    elif flask.request.form['operation'] == 'edit_account':
        # Unpack flask object
        fileobj = flask.request.files["file"]
        filename = fileobj.filename

        stem = uuid.uuid4().hex
        uuid_basename = f"{stem}{pathlib.Path(filename).suffix.lower()}"

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        user = flask.session["user"]
        fullname = flask.request.form['fullname']
        email = flask.request.form['email']

        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?, filename = ? "
            "WHERE username = ?;",
            (fullname, email, uuid_basename, user)
        )

    elif flask.request.form['operation'] == 'update_password':
        user = flask.session["user"]

        if "user" in flask.session:
            cur = connection.execute(
                "SELECT password FROM users WHERE username = ?",
                (user,)
            )
            passworddb = cur.fetchall()[0]["password"]
            password_input = flask.request.form['password']

            if passworddb != hash_password(password_input, passworddb):
                flask.abort(403)

            new_password = flask.request.form['new_password1']
            new_password2 = flask.request.form['new_password2']
            if new_password != new_password2:
                flask.abort(401)

            connection.execute(
                "UPDATE users "
                "SET password = ? "
                "WHERE username = ?;",
                (hash_password(new_password), user)
            )
        else:
            flask.abort(403)

    else:
        flask.abort(400)
    return flask.redirect(target)


@insta485.app.route('/likes/', methods=['POST'])
def likes_redirect():
    """LIKES LIKES."""
    target = flask.request.args.get('target')
    user = flask.session["user"]
    postid = flask.request.form['postid']
    connection = insta485.model.get_db()

    if flask.request.form['operation'] == "like":
        cur = connection.execute(
            "SELECT * FROM likes WHERE owner = ? AND postid = ?",
            (user, postid)
        )

        query = cur.fetchall()

        if len(query) == 1:
            # If the user already liked this post
            flask.abort(409)

        connection.execute(
            "INSERT INTO likes(owner, postid, created) "
            "VALUES (?, ?, CURRENT_TIMESTAMP);",
            (user, postid,)
        )
    elif flask.request.form['operation'] == "unlike":
        cur = connection.execute(
            "SELECT * FROM likes WHERE owner = ? AND postid = ?",
            (user, postid)
        )
        query = cur.fetchall()

        if len(query) == 0:
            # If the user already unliked this post
            flask.abort(409)

        connection.execute(
            "DELETE FROM likes WHERE owner = ? AND postid =?;",
            (user, postid,)
        )

    return flask.redirect(target)


@insta485.app.route('/comments/', methods=['POST'])
def comments_redirect():
    """COMMENTS COMMENTS."""
    target = flask.request.args.get('target')
    user = flask.session['user']
    if target is None:
        target = '/'

    connection = insta485.model.get_db()

    if flask.request.form['operation'] == 'create':
        postid = flask.request.form['postid']
        text = flask.request.form['text']

        if len(text) == 0:
            flask.abort(400)

        connection.execute(
            "INSERT INTO comments (owner, postid, text, created)"
            "VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (user, postid, text,)
        )
    elif flask.request.form['operation'] == 'delete':
        commentid = flask.request.form['commentid']

        connection.execute(
            "DELETE FROM comments WHERE commentid = ?",
            (commentid,)
        )
    return flask.redirect(target)


@insta485.app.route('/following/', methods=['POST'])
def following_redirect():
    """FOLLOWING FOLLOWING."""
    target = flask.request.args.get('target')
    user = flask.session["user"]
    connection = insta485.model.get_db()

    if flask.request.form['operation'] == 'follow':
        print(user)
        connection.execute(
            "INSERT INTO following (username1, username2) "
            "VALUES (?,?);",
            (user, flask.request.form['username'])
        )

    else:
        connection.execute(
            "DELETE FROM following WHERE username1 =? AND username2 =?;",
            (user, flask.request.form['username'])
        )

    return flask.redirect(target)


@insta485.app.route('/posts/', methods=['POST'])
def post_redirect():
    """POST POST."""
    target = flask.request.args.get('target')
    user = flask.session["user"]
    connection = insta485.model.get_db()

    if target is None:
        target = f'/users/{user}/'

    if flask.request.form['operation'] == 'create':
        # 'file' does not exist in the flask form
        fileobj = flask.request.files['file']
        filename = fileobj.filename

        if len(filename) == 0:
            flask.abort(400)

        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        connection.execute(
            "INSERT INTO posts (filename, owner, created) "
            "VALUES (?, ?, CURRENT_TIMESTAMP);",
            (uuid_basename, user,)
        )

    elif flask.request.form['operation'] == 'delete':
        postid = flask.request.form['postid']

        cur = connection.execute(
            "SELECT filename FROM posts WHERE postid = ?;",
            (postid,)
        )
        filename = cur.fetchall()[0]['filename']

        pathlib.Path.unlink(insta485.app.config["UPLOAD_FOLDER"]/filename)

        connection.execute(
            "DELETE FROM posts WHERE postid = ? ",
            (postid,)
        )
    return flask.redirect(target)

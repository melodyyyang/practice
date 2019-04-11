class StaffUser:

    def __init__(self, username, real_name, pw):
        self._username = username
        self._real_name = real_name
        self._pw_hash = password_hash(pw)

    def verify_password(self, password):
        if password_verify(password, self._pw_hash):
            return True
        return False

    def logout(self):
        # how do we implement this?
        pass

    @property
    def username(self):
        return self._username

    @property
    def real_name(self):
        return self._real_name


def password_hash(raw_password):
    """ A fake password hash function, that
    does not actually do any hashing
    """
    salt = "This_Is_A_Very_Bad_But_Fake_Hash_Function"
    pw_hash = salt + raw_password
    return pw_hash


def password_verify(password, password_hash):
    """ Takes a supplied password and the
    password_hash that was stored in the database
    and returns true if the password matches its hash
    and returns false if not
    """
    hashed_password = password_hash(password)
    if hashed_password == password_hash:
        return True
    return False


def is_valid_username(username):
    """ Checks if a username contains invalid characters
    such as spaces """
    invalid_chars = [" ", ";", "'", '"', '\\']
    for ch in invalid_chars:
        if ch in username:
            return False
    return True

#@app.route("/is_existing_username", methods=['GET'])
def is_existing_username():
    username = request.args.get('username')
    if system.does_username_exist(username):
        return jsonify({"response": True, "message": "Valid username"})
    return jsonify({"response": False, "message": "This username does not exist"})

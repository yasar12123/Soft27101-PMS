class User:
    def __init__(self, username, user_fullname, user_email, password_hash, is_admin=0):
        self.username = username
        self.user_fullname = user_fullname
        self.user_email = user_email
        self.password_hash = password_hash
        self.is_admin = is_admin

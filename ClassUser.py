class User:
    def __init__(self, username, fullname, user_email, password_hash, is_admin=0):
        self.username = username
        self.fullname = fullname
        self.user_email = user_email
        self.password_hash = password_hash
        self.is_admin = is_admin

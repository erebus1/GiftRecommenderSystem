
class DBUser:
    def __init__(self, user):
        self.categories = user.categories
        self.user_type = user.user_type
        self.already_gifted = user.already_gifted
        self.sex = user.sex
        self.age = user.age


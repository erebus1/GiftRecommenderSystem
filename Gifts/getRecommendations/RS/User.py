__author__ = 'user'


class User:
    def __init__(self, age, sex, hobbies, user_type, categories_str=None, already_gifted=None):
        """

        :param age: int
        :param sex: "Male"/"Female"
        :param hobbies: list of words (one word per string)
        :param user_type: dict{type1, type2, type3, type4, type5}
        :param categories_str: list of words (one word per string)
        :param already_gifted:
        :return:
        """
        if not already_gifted: already_gifted = []
        if not categories_str: categories_str = []
        assert type(user_type) == dict
        assert type(categories_str) == list
        assert type(hobbies) == list
        assert type(already_gifted) == list
        assert type(age) == int
        assert type(sex) == str

        self.categories = {}
        self.user_type = user_type
        self.categories_str = categories_str
        self.already_gifted = already_gifted
        self.hobbies = hobbies
        self.sex = sex
        self.age = age


    def __str__(self):
        return "age: " + str(self.age) + "\nsex: " + self.sex + "\nhobbies: " + str(self.hobbies) + \
               "\nuser type: " + str(self.user_type)


    def add_category_id(self, category_id, rating=1, votes=0):
        if category_id not in self.categories:
            self.categories.update({category_id: {'rating': rating, 'votes': votes}})

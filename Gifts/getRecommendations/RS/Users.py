from Gifts.getRecommendations.Requests import tradingApi
from Gifts.getRecommendations.additionalStaff import *
from User import User
from DBUser import DBUser
from Gifts.getRecommendations.TextClasterisation.nlp import clean_texts_simple
from Gifts.getRecommendations.DB import DB


def make_input_user(user_dict):
    """
    generate user
    :return: User
    """

    user = User(int(user_dict['age']), str(user_dict['sex']), user_dict['hobbies'],
                user_dict['userType'], user_dict['lovedCategories'], user_dict['alreadyGifted'])

    return user


def simplify_hobbies_and_categories(user):
    """
    use stemmer, tokenise, remove stop words from hobbies and categories
    :param user: User
    :return: nothing, but modify user
    """
    user.hobbies_simpler = [hobby[0] for hobby in clean_texts_simple(user.hobbies)]
    user.categories_str_simpler = [category[0] for category in clean_texts_simple(user.categories_str)]


def get_categories_from_hobbies_and_categories_str(user):
    """
    search through all categories for thous, which similar to hobbies or categories
    and add them to user.categories
    :param user:
    :return:
    """
    simplify_hobbies_and_categories(user)  # stemmer and so on
    client = DB.get_client()  # open connection

    categories = client.GRS.categories.find({}, {"CategoryName": 1, "CategoryID": 1, "_id": 0})
    for category in categories:  # go through all categories
        already_added = False
        for category_str in user.categories_str_simpler:
            if category['CategoryName'].lower().find(category_str) >= 0:
                user.categories.update({str(category['CategoryID']): {"rating": 1, "votes": 0}})
                already_added = True
                break
        if already_added:
            continue
        for hobby in user.hobbies_simpler:
            if category['CategoryName'].lower().find(hobby) >= 0:
                user.categories.update({str(category['CategoryID']): {"rating": 1, "votes": 0}})
                break

    client.close()


def get_suggested_categories(hobby):
    """
    ask on ebay 10 suggested categories for hobby accessories
    :param hobby:
    :return:
    """
    response_suggested = tradingApi.run("GetSuggestedCategories", {'query': hobby + " accessories"})
    return response_suggested['SuggestedCategoryArray']['SuggestedCategory']


def add_suggested_categories(user):
    """
    for all hobbes find suggested categories and add them in user.categories
    :param user:
    :return:
    """
    for hobby in user.hobbies:
        response = get_suggested_categories(hobby)
        for category in response:
            user.add_category_id(category['Category']['CategoryID'])


def process_user(user):
    """
    add similar categories
    add suggested categories
    and save user in file

    :param user:
    :return:
    """
    get_categories_from_hobbies_and_categories_str(user)
    add_suggested_categories(user)
    save_to_file(user, 'user.data')


def add_user_to_db(user):
    client = DB.get_client()
    try:
        return client.GRS.users.insert_one(DBUser(user).__dict__).inserted_id
    finally:
        client.close()


def add_user(user_dict):
    user = make_input_user(user_dict)
    process_user(user)
    return str(add_user_to_db(user))


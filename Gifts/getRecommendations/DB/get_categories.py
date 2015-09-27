import pymongo
from Gifts.getRecommendations.Requests import tradingApi
from Gifts.getRecommendations.additionalStaff import *
from pymongo import MongoClient


def get_categories_from_api():
    """
    extract all categories from api and save to file
    :return:
    """
    categories = tradingApi.run("GetCategories", {"CategorySiteID": 0, "DetailLevel": "ReturnAll"})
    save_to_file(categories, "categories.data")


def add_child_list():
    """
    add child list to categories and save to file
    :return:
    """
    categories = extract_from_file("categories.data")['CategoryArray']['Category']

    for category_parent in categories:
        category_parent['ChildID'] = []
        for category_child in categories:
            if category_child['CategoryID'] != category_child['CategoryParentID']:
                if category_child['CategoryParentID'] == category_parent['CategoryID']:
                    category_parent['ChildID'].append(category_child['CategoryID'])

    save_to_file(categories, "new_categories.data")


def clean_categories_data():
    """
    convert string to other format
    remove useless fields

    :return:
    """
    categories = extract_from_file("new_categories.data")
    for category in categories:
        if 'AutoPayEnabled' in category:
            category.__delitem__("AutoPayEnabled")
        if 'BestOfferEnabled' in category:
            category.__delitem__("BestOfferEnabled")

        # str to int
        category['CategoryID'] = int(category['CategoryID'])
        category['CategoryID'] = int(category['CategoryID'])
        category['CategoryLevel'] = int(category['CategoryLevel'])
        category['CategoryParentID'] = int(category['CategoryParentID'])
        # str to bool
        if 'LeafCategory' in category:
            if category['LeafCategory'] == 'true':
                category['LeafCategory'] = True
            else:
                category['LeafCategory'] = False
        temp = []
        for subCategory in category['ChildID']:
            temp.append(int(subCategory))
        category['ChildID'] = temp

    save_to_file(categories, 'new_categories_cleaned.data')


def add_categories_to_db():
    """
    extract categories from file and write in db
    :return:
    """
    categories = extract_from_file("new_categories_cleaned.data")

    client = MongoClient('localhost', 27017)

    db = client.GRS

    categories_collection = db.categories

    result = categories_collection.insert_many(categories)

    print result

    client.close()


def add_index():
    """
    add indexes to id's in db
    :return:
    """
    client = MongoClient('localhost', 27017)
    db = client.GRS
    categories_collection = db.categories
    categories_collection.create_index("CategoryParentID")
    categories_collection.create_index("CategoryID")
    client.close()


def play_DB():
    client = MongoClient('localhost', 27017)

    db = client.GRS

    categories_collection = db.categories

    result = categories_collection.find({'CategoryParentID': 20081})
    # result = categories_collection.find({'LeafCategory': True})
    for category in result:
        print category

    client.close()


def main():
    get_categories_from_api()
    clean_categories_data()
    add_child_list()
    add_categories_to_db()
    add_index()

    play_DB()


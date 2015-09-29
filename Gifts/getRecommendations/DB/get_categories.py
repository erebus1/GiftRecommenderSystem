from Gifts.getRecommendations.Requests import tradingApi
from pymongo import MongoClient


def get_categories_from_api():
    """
    extract all categories from api and save to file
    :return:
    """
    categories = tradingApi.run("GetCategories", {"CategorySiteID": 0, "DetailLevel": "ReturnAll"})
    return categories

def add_child_list(categories):
    """
    add child list to categories and save to file
    :return:
    """
    categories = categories['CategoryArray']['Category']

    progress = 0
    for category_parent in categories:
        progress += 1
        print progress / float(len(categories))
        category_parent['ChildID'] = []
        for category_child in categories:
            if category_child['CategoryID'] != category_child['CategoryParentID']:
                if category_child['CategoryParentID'] == category_parent['CategoryID']:
                    category_parent['ChildID'].append(category_child['CategoryID'])

    return categories


def clean_categories_data(categories):
    """
    convert string to other format
    remove useless fields

    :return:
    """
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

    return categories

def add_categories_to_db(categories):
    """
    extract categories from file and write in db
    :return:
    """

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
    categories = get_categories_from_api()
    add_child_list(categories)
    clean_categories_data(categories)
    add_categories_to_db(categories)
    add_index()

    play_DB()


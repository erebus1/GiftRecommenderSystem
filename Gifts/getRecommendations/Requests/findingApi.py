from ebaysdk.exception import ConnectionError
from Gifts.getRecommendations.additionalStaff import *
import datetime
from ebaysdk.finding import Connection

def get_list_of_items(request, params=None):
    try:
        api = Connection()
        response = api.execute(request, params)

        assert(response.reply.ack == 'Success')
        assert(type(response.reply.timestamp) == datetime.datetime)
        assert(type(response.reply.searchResult.item) == list)

        item = response.reply.searchResult.item[0]
        assert(type(item.listingInfo.endTime) == datetime.datetime)
        assert(type(response.dict()) == dict)
        return response.dict()

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def output():
    # list = get_list_of_items("findItemsAdvanced", {'keywords': "golf accessories"})
    # save_to_file(list)
    list = extract_from_file()


    page = list['searchResult']
    # item = page['item'][1]
    items = page['item']
    print page['item'][1].keys()
    for item in items:
        print item['title']



# output()

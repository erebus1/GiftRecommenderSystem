
# coding: utf-8

#     add user

# In[77]:

import urllib, urllib2, json, requests


# In[319]:

import json, requests
url = 'http://127.0.0.1:8000/Gifts/'
request = json.dumps({'task': 'addUser', "data":{"userProfile": {'age':10, 'sex':'Male', 'hobbies':['cars','bicycle'], 
                                              'userType':{'type1':0.2,'type2':0.2,'type3':0.2,'type4':0.2,'type5':0.2,}}}})
headers = {'Content-Type': 'application/json'}
r = requests.post(url, data=request, headers=headers)



# In[320]:

r.text


#     Make List

# In[380]:

import json, requests
url = 'http://127.0.0.1:8000/Gifts/'
request = json.dumps({'task': 'makeList', "data":{"filter": {'minPrice':10, 'maxPrice':100}, "userId": "5608150678206454f82ae0f9"}})
headers = {'Content-Type': 'application/json'}
r = requests.post(url, data=request, headers=headers)


# In[381]:

r.text


#     Get first page

# In[388]:

import json, requests
url = 'http://127.0.0.1:8000/Gifts/'
request = json.dumps({'task': 'getSuggestions', "data":{"page":1, "userId": "5608150678206454f82ae0f9"}})
headers = {'Content-Type': 'application/json'}
r = requests.post(url, data=request, headers=headers)


# In[389]:

r.text


#     Rate item

# In[400]:

import json, requests
url = 'http://127.0.0.1:8000/Gifts/'
request = json.dumps({'task': 'rateItem', "data":{"itemId": "201157362895", "rating": 5, "userId": "5608150678206454f82ae0f9"}})
headers = {'Content-Type': 'application/json'}
r = requests.post(url, data=request, headers=headers)


# In[401]:

r.text


# In[ ]:




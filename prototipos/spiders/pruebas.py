# import datetime
# from datetime import datetime as dt
# date=dt(2021,3,16)

# txt = "https://www.thetrainline.com/book/results?origin=1321c6b97b1fdf4439cbd3020b1d74ac&destination=a0893c38dcb9222abe36edec6a51a1ac&outwardDate=2021-03-14T13%3A45%3A00&outwardDateType=departAfter&journeySearchType=single&passengers%5B%5D=1994-03-14%7C255981e1-2bde-4a3e-92a5-94ba790d6101&lang=es"

# import numpy as np
# listatxt=list(txt)
# lst=np.array(list(txt))
# lista=['&']*len(lst)
# mask=np.isin(lst,lista)
# indices=np.where(mask)
# listIndices=list(indices[0])
# pattern=listatxt[listIndices[1]:listIndices[2]]
# patternTxt = "".join(pattern)
# txt=txt.replace(patternTxt,"&outwardDate="+date.isoformat())

# import json
# from datetime import datetime as dt
# import requests

# data=dt(2021,3,19)

# postURL = 'https://www.thetrainline.com/buytickets/'
# postURL = 'https://www.thetrainline.com/buytickets/'
# predata = {'OriginStation':'Stockport',
# 'DestinationStation':'Birmingham New Street',
# 'RouteRestriction':'NULL',
# 'ViaAvoidStation':'',
# 'journeyTypeGroup':'return',
# 'outwardDate':'14-Apr-21',
# 'OutwardLeaveAfterOrBefore':'A',
# 'OutwardHour':'15',
# 'OutwardMinute':'15',
# 'returnDate':'16-Apr-21',
# 'InwardLeaveAfterOrBefore':'A',
# 'ReturnHour':'9',
# 'ReturnMinute':'0',
# 'AdultsTravelling':'1',
# 'ChildrenTravelling':'0',
# 'railCardsType_0':'YNG',
# 'railCardNumber_0':'1',
# 'ExtendedSearch':'Get times & tickets'}

# headers = {'User-Agent': 'AdsBot-Google (+http://www.google.com/adsbot.html)'}
# postform=requests.post(postURL,cookies=requests.post(postURL).cookies,data=headers)
# print(postform.text)

# import trainline


# results = trainline.search(
# 	departure_station="Burgos",
# 	arrival_station="Barcelona Sants",
# 	from_date="17/03/2021 00:00",
# 	to_date="27/03/2021 00:00")

# print(results.csv())



import json
from datetime import datetime as dt
import requests

data=dt(2021,3,19)

postURL = 'https://www.thetrainline.com/es'
predata = {'origin':'7e5918defb2141762dec00dfd051d16d',
'destination':'a0893c38dcb9222abe36edec6a51a1ac',

}

headers = {'User-Agent': 'AdsBot-Google (+http://www.google.com/adsbot.html)'}
postform=requests.post(postURL,cookies=requests.post(postURL).cookies)
print(postform.text)
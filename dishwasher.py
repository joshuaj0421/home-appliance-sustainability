
import requests
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# set up the request parameters
params = {
'api_key': '944509ADCB7A4F059C56E9571CA0D0D3',
  'type': 'search',
  'url': 'https://www.homedepot.com/s/dishwasher?NCNI-5',
  'sort_by': 'best_seller',
  'output': 'json'
}

# make the http GET request to BigBox API
api_result = requests.get('https://api.bigboxapi.com/request', params)

# print the JSON response from BigBox API
result = api_result.json()

#arrays
idArray = []
nameArray = []
priceArray = []
sizeArray = []
kWhArray = []

for i in range(0,5):
  id = result["search_results"][i]["product"]["item_id"]
  name = result["search_results"][i]["product"]["title"]
  price = result["search_results"][i]["offers"]['primary']['price']
  
  k = 0
  while(True):
    if(result["search_results"][i]["product"]["features"][k]['name'] == "Dishwasher Size"):
      size = result["search_results"][i]["product"]["features"][k]['value']
      break
    k += 1
  
  str(id)
  str(name)
  str(size)
  str(price)
  
  idArray.append(id)
  nameArray.append(name)
  sizeArray.append(size)
  priceArray.append(price)
  

#after finding id
for i in range(0,5):
  params = {
    'api_key': '944509ADCB7A4F059C56E9571CA0D0D3',
    'type': 'product',
    'item_id': idArray[i]
  }

  # make the http GET request to BigBox API
  api_result2 = requests.get('https://api.bigboxapi.com/request', params)

  # print the JSON response from BigBox API
  result2 = api_result2.json()

  j = 0
  while(True):
    val = result2["product"]["specifications"][j]
    if (val['name'] == "Energy Consumption (kWh/year)"):
      kWh = val['value']
      str(kWh)
      kWhArray.append(kWh)
      break
    j += 1

print("This is title array: ", nameArray)
print("This is size array: ", sizeArray)
print("This is price array: ", priceArray)
print("This is kWh array: ", kWhArray)

aoa = [nameArray,sizeArray,priceArray,kWhArray]

refrigeratorSheet = client.open("Hackathon 2023").worksheet("dishwasher")

# name
nameSection=2
for x in nameArray:
  refrigeratorSheet.update_cell(nameSection,2,x)
  nameSection += 1
  
#Price
priceSection=2
for x in priceArray:
  refrigeratorSheet.update_cell(priceSection,3,x)
  priceSection += 1
  
#Size
sizeSection=2
for x in sizeArray:
  refrigeratorSheet.update_cell(sizeSection,4,x)
  sizeSection += 1

#kWh 
kWhSection=2
for x in kWhArray:
  refrigeratorSheet.update_cell(kWhSection,5,x)
  kWhSection += 1
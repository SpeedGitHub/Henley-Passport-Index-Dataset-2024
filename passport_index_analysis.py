import requests
import pandas as pd
from datetime import datetime

# Fetching passport data from the Henley Passport Index API
res = requests.get('https://api.henleypassportindex.com/api/passports')
data = res.json()

# Processing country codes and names
code_list = [{'code': item.get('code'), 'country': item.get('name')} for item in data if item.get('code') != '']
code_list = sorted(code_list, key=lambda k: k['country'])  # Sorting by country name

# Initializing lists for processing visa requirements
origin_lst = []
destination_lst = []
requirement = []
visa_free_count_lst = []
visa_required_count_lst = []
origin_for_count = []
visa_free = 'Visa Free'
visa_required = 'Visa Required'

# Analyzing visa requirements for each country pair
for origin in code_list:
    origin_country = origin.get('country')
    origin_for_count.append(origin_country)
    count_vf = 0
    count_vr = 0
    res = requests.get('https://api.henleypassportindex.com/api/passports/' + origin.get('code') + '/countries')
    data = res.json()
    for destination in data['default']:
        destination_country = destination.get('name')
        origin_lst.append(origin_country)
        destination_lst.append(destination_country)
        is_visa_free = destination.get('pivot').get('is_visa_free')
        if str(is_visa_free) == "1":
            count_vf += 1
            requirement.append(visa_free)
        else:
            if str(origin_country) == str(destination_country):
                requirement.append("N/A")
            else:
                count_vr += 1
                requirement.append(visa_required)

    visa_free_count_lst.append(count_vf)
    visa_required_count_lst.append(count_vr)

# Creating and exporting the first dataframe
today_date = datetime.today().strftime('%Y-%m-%d')
file_name = "henley-passport-index" + "-" + today_date + ".csv"
pd_1 = pd.DataFrame({'Origin': origin_lst, 'Destination': destination_lst, 'Requirement': requirement})
pd_1.to_csv(file_name, index=False)

# Creating and exporting the second dataframe
file_name_count = "henley-passport-index-count" + "-" + today_date + ".csv"
pd_2 = pd.DataFrame({'Origin': origin_for_count, 'Visa Free': visa_free_count_lst, 'Visa Required': visa_required_count_lst})
pd_2.to_csv(file_name_count, index=False)

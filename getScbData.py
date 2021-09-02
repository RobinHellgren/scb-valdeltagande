import requests
import operator
from dataclasses import dataclass

@dataclass
class Region_Result:
    """Class for keeping track of a regions election participation."""
    region: str
    year: int
    result: float


api_url = "http://api.scb.se/OV0104/v1/doris/sv/ssd/START/ME/ME0104/ME0104D/ME0104T4"

region_code_dictionary_request = requests.get(api_url)
region_data = region_code_dictionary_request.json().get("variables")[0]

region_codes = region_data["values"]
region_codes.remove('00')

region_names = region_data["valueTexts"]
region_names.remove('Riket')

region_code_to_name_dictionary = {}
for i in range(len(region_names)):
    region_code_to_name_dictionary[region_codes[i]] = region_names[i]

data_request = requests.post(api_url,json = {
        "query": [
          {
            "code": "Region",
            "selection": {
              "filter": "vs:RegionKommun07+BaraEjAggr",
              "values": region_codes
            }
          },
          {
            "code": "ContentsCode",
            "selection": {
              "filter": "item",
              "values": [
                "ME0104B8"
              ]
            }
          }
        ],
        "response": {
          "format": "json"
        }
      })
data = data_request.json()["data"]

region_list = []
for row in data:
    row_region_code = row["key"][0]
    row_year = row["key"][1]
    row_result = row["values"][0]
    if(row_result == '..'):
        continue
    region_list.append(Region_Result(region_code_to_name_dictionary[row_region_code], row_year, row_result))

region_list_sorted = sorted(region_list,key=operator.attrgetter("result"), reverse=True)

for i in range(100):
    print(str(i+1) +": " + region_list_sorted[i].region + " - " + str(region_list_sorted[i].year) + " -> " + str(region_list_sorted[i].result) + "%" )
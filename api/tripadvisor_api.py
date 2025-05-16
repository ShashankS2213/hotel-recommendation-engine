import requests
from datetime import datetime, timedelta

headers = {
    'x-rapidapi-key': "f025d1a2ccmshc5efd75374343dbp1d5f2cjsn52c341f55c09",
    'x-rapidapi-host': "tripadvisor16.p.rapidapi.com"
}

def get_geo_id(location):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
    params = {"query": location}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        results = res.json().get("data", [])
        return results[0]["geoId"] if results else None
    return None

def get_hotels_for_location(geo_id, check_in, check_out, sort, offset):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
    params = {
        "geoId": geo_id,
        "checkIn": check_in,
        "checkOut": check_out,
        "sort": sort,
        "offset": str(offset)
    }

    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        hotels = res.json().get("data", {}).get("data", [])
        return hotels
    else:
        print(f"❌ API Failed: Status {res.status_code}")
        return []

from api.tripadvisor_api import get_geo_id, get_hotels_for_location
from utils.helpers import save_hotels_to_db
from datetime import datetime, timedelta
from db.database import Base, engine
import time

from models.offering_model import Offering

Base.metadata.create_all(engine)

def collect_hotels_rotating():
    indian_cities = [
        "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai",
        "Kolkata", "Goa", "Jaipur", "Agra", "Udaipur",
        "Varanasi", "Rishikesh", "Mysore", "Kochi", "Pune",
        "Shimla", "Manali", "Darjeeling", "Ooty", "Leh",
        "Jaisalmer", "Alleppey", "Munnar", "Lonavala", "Mahabalipuram"
    ]

    sort_options = ["POPULARITY", "RANKING", "DISTANCE", "CHEAPEST"]

    today = datetime.today()
    date_variants = [(today + timedelta(days=delta)).strftime('%Y-%m-%d') for delta in range(0, 10, 2)]

    for city in indian_cities:
        geo_id = get_geo_id(city)
        if not geo_id:
            print(f"❌ Geo ID not found for {city}")
            continue

        for check_in in date_variants:
            check_out = (datetime.strptime(check_in, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

            for sort_order in sort_options:
                for page in range(5):  # 5 pages = offsets 0, 30, 60, 90, 120
                    offset = page * 30

                    print(f"📡 Fetching {city} | {check_in}-{check_out} | sort={sort_order} | page={page+1}")
                    hotels = get_hotels_for_location(geo_id, check_in, check_out, sort_order, offset)

                    if not hotels:
                        print(f"⚠️ No more hotels found for {city}, breaking page loop.")
                        break

                    save_hotels_to_db(hotels, city)
                    time.sleep(1.2)

if __name__ == "__main__":
    collect_hotels_rotating()

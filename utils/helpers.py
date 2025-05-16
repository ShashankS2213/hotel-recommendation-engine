import re
from db.database import session
from models.offering_model import Offering

def extract_price(price_str):
    if not price_str:
        return None
    try:
        return float(price_str.replace("$", "").replace(",", "").split()[0])
    except:
        return None

def clean_review_count(raw_count):
    if not raw_count:
        return 0
    try:
        cleaned = re.sub(r"[^\d]", "", str(raw_count))
        return int(cleaned)
    except:
        return 0

def save_hotels_to_db(hotels, city):
    added_count = 0
    for h in hotels:
        try:
            price = extract_price(h.get("priceForDisplay", ""))
            rating = float(h.get("bubbleRating", {}).get("rating", 0))
            num_reviews = clean_review_count(h.get("bubbleRating", {}).get("count", 0))
            platform_id = h.get("id", "")

            existing = session.query(Offering).filter_by(platform_id=platform_id).first()
            if existing:
                existing.name = h.get("title", "")
                existing.location = city
                existing.price = price
                existing.rating = rating
                existing.num_reviews = num_reviews
            else:
                offer = Offering(
                    name=h.get("title", ""),
                    location=city,
                    price=price,
                    rating=rating,
                    num_reviews=num_reviews,
                    platform_id=platform_id
                )
                session.add(offer)
                added_count += 1

        except Exception as e:
            print("Error:", e)
            session.rollback()

    session.commit()
    print(f"✅ Added {added_count} new hotels for {city}")

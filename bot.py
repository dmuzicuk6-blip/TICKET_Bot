import requests

def check_uz(from_city, to_city, date):
    try:
        url = "https://booking.uz.gov.ua/train_search/"

        payload = {
            "from": from_city,
            "to": to_city,
            "date": date
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.post(url, data=payload, headers=headers, timeout=10)

        data = r.json()

        # якщо є поїзди
        if "value" in data and len(data["value"]) > 0:
            return True

        return False

    except Exception as e:
        print("UZ error:", e)
        return False

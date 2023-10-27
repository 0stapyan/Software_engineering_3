import requests
from datetime import datetime

def fetch_user_data(offset):

    api_url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(api_url)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('data', [])
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None

def historical_data_for_all_users(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    users_data = fetch_user_data(0)
    historical_data = []

    for user in users_data:
        last_seen = user.get('lastSeenDate', None)
        users_online = user.get('usersOnline', None)  # Handle usersOnline field

        if last_seen:
            last_seen = last_seen.split('.')[0]
            last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

            if last_seen_date <= date:
                historical_data.append({
                    'user_id': user.get('userId'),
                    'last_seen_date': last_seen_date,
                    'users_online': users_online  # Include usersOnline in the result
                })

    total_users = len(users_data)

    print(f"Users Online at {date}: {len(historical_data)}")
    print(f"Total Users: {total_users}")

historical_data_for_all_users('2023-09-27 20:00')

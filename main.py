import requests
from datetime import datetime
from datetime import timedelta

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
        users_online = user.get('usersOnline', None)

        if last_seen:
            last_seen = last_seen.split('.')[0]
            last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

            if last_seen_date <= date:
                historical_data.append({
                    'user_id': user.get('userId'),
                    'last_seen_date': last_seen_date,
                    'users_online': users_online
                })

    total_users = len(users_data)

    print(f"Users Online at {date}: {len(historical_data)}")
    print(f"Total Users: {total_users}")


def get_user_by_id(user_data, user_id):
    for user in user_data:
        if user.get('userId') == user_id:
            return user
    return None


def datetime_from_iso(iso_date_str):
    if iso_date_str:
        return datetime.strptime(iso_date_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    return None



def users_online_at_date(users_data, user_id, date):
    online_users = []
    for user in users_data:
        last_seen = user.get('lastSeenDate', None)

        if last_seen:
            last_seen_date = datetime_from_iso(last_seen)

            if last_seen_date <= date:
                online_users.append({
                    'user_id': user.get('userId'),
                    'last_seen_date': last_seen_date
                })

    return online_users


def find_nearest_online_time(users_data, user_id, date):
    found_user = get_user_by_id(users_data, user_id)

    if found_user is None:
        return (None, None)

    last_seen = found_user.get('lastSeenDate', None)

    if last_seen:
        last_seen_date = datetime_from_iso(last_seen)
        was_user_online = last_seen_date <= date

        if was_user_online:
            return (True, None)

        nearest_online_time = None

        for user in users_data:
            if user.get('userId') == user_id:
                continue

            user_last_seen = user.get('lastSeenDate', None)
            if user_last_seen:
                user_last_seen_date = datetime_from_iso(user_last_seen)
                if user_last_seen_date > date:
                    if nearest_online_time is None or user_last_seen_date < nearest_online_time:
                        nearest_online_time = user_last_seen_date

        return (False, nearest_online_time)

    return (None, None)

def predict_users_online(user_data, future_date_str):

    future_date = datetime.strptime(future_date_str, "%Y-%m-%d %H:%M")
    day = future_date.strftime('%A')
    time = future_date.strftime('%H:%M')

    matching_data = [user for user in user_data if
                 user.get('lastSeenDate') and
                 datetime_from_iso(user.get('lastSeenDate')).strftime('%A') == day and
                 datetime_from_iso(user.get('lastSeenDate')).strftime('%H:%M') == time]


    if not matching_data:
        return {"online_users" : 0}

    total_online_users =0

    for user in matching_data:
        users_online = user.get('usersOnline', 0)
        total_online_users += users_online

    average_users_online = total_online_users / len(matching_data)

    return {"online_users" : round(average_users_online)}


date_str = '2023-09-27 20:00'
user_id = 'A4DC2287-B03D-430C-92E8-02216D828709'
future_date_str = '2025-09-27 20:00'


user_data = fetch_user_data(0)
date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

online_users = users_online_at_date(user_data, user_id, date)

print(f"Users Online at {date_str}: {len(online_users)}")
print(f"Total Users: {len(user_data)}")

was_user_online, nearest_online_time = find_nearest_online_time(user_data, user_id, date)

if was_user_online is True:
    print(f"User {user_id} was online at {date}: True")
elif was_user_online is False:
    print(f"User {user_id} was online at {date}: False")
    if nearest_online_time:
        print(f"Nearest online time for user {user_id}: {nearest_online_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        print(f"User {user_id} has no other online records.")
else:
    print(f"User {user_id} wasn't found :(")

prediction = predict_users_online(user_data, future_date_str)

print(f"Predicted online users at {future_date_str}: {prediction['online_users']}")



import unittest
from unittest.mock import patch, Mock
from datetime import datetime
from main import fetch_user_data, historical_data_for_all_users, predict_users_online, predict_user_online, get_user_by_id, datetime_from_iso, users_online_at_date, find_nearest_online_time

class TestUserDataAnalysis(unittest.TestCase):

    def test_fetch_user_data_success(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'data': []}
            mock_get.return_value = mock_response

            result = fetch_user_data(0)
            self.assertEqual(result, [])

    def test_fetch_user_data_failure(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = fetch_user_data(0)
            self.assertIsNone(result)

    def test_users_online_at_date(self):
        user_data = [
            {
                'userId': '1',
                'lastSeenDate': '2023-09-27T19:00:00',
            },
            {
                'userId': '2',
                'lastSeenDate': '2023-09-27T20:00:00',
            }
        ]
        date = datetime.strptime('2023-09-27 19:30', "%Y-%m-%d %H:%M")
        result = users_online_at_date(user_data, '1', date)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['user_id'], '1')

    def test_find_nearest_online_time(self):
        user_data = [
            {
                'userId': '1',
                'lastSeenDate': '2023-09-27T19:00:00',
            },
            {
                'userId': '2',
                'lastSeenDate': '2023-09-27T20:00:00',
            }
        ]
        date = datetime.strptime('2023-09-27 19:30', "%Y-%m-%d %H:%M")
        was_online, nearest_time = find_nearest_online_time(user_data, '1', date)
        self.assertTrue(was_online)
        self.assertIsNone(nearest_time)

    def test_predict_users_online(self):
        user_data = [
            {
                'lastSeenDate': '2023-09-27T19:00:00',
                'usersOnline': 10,
            },
            {
                'lastSeenDate': '2023-09-27T19:00:00',
                'usersOnline': 5,
            }
        ]
        future_date_str = '2023-09-27 19:00'
        result = predict_users_online(user_data, future_date_str)
        self.assertEqual(result['online_users'], 7)

    def test_predict_user_online(self):
        user_data = [
            {
                'lastSeenDate': '2023-09-27T19:00:00',
            },
            {
                'lastSeenDate': '2023-09-27T19:00:00',
            },
            {
                'lastSeenDate': '2023-09-27T19:00:00',
            }
        ]
        future_date_str = '2023-09-27 19:00'
        tolerance = 0.6
        result = predict_user_online(user_data, future_date_str, '1', tolerance)
        self.assertTrue(result['willBeOnline'])
        self.assertAlmostEqual(result['onlineChance'], 0.75, places=2)


if __name__ == '__main__':
    unittest.main()

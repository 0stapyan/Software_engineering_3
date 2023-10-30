import unittest
from unittest.mock import patch, Mock
from datetime import datetime
from main import fetch_user_data, historical_data_for_all_users, predict_users_online, predict_user_online, get_user_by_id, datetime_from_iso, users_online_at_date, find_nearest_online_time

class TestIntegration(unittest.TestCase):

    def test_predict_users_online_integration(self):
         future_date_str = '2023-09-28 12:00'
         user_data = fetch_user_data(0)

         prediction = predict_users_online(user_data, future_date_str)

         self.assertTrue('online_users' in prediction)
         self.assertTrue(0 <= prediction['online_users'] <= len(user_data))

    def test_predict_user_online_integration(self):
         future_date_str = '2023-09-28 12:00'
         user_id = 'A4DC2287-B03D-430C-92E8-02216D828709'
         tolerance = 0.85
         user_data = fetch_user_data(0)

         prediction = predict_user_online(user_data, future_date_str, user_id, tolerance)

         self.assertTrue('willBeOnline' in prediction)
         self.assertTrue('onlineChance' in prediction)
         self.assertTrue(0 <= prediction['onlineChance'] <= 1)

    @patch('main.fetch_user_data')
    def test_historical_data_for_all_users(self, mock_fetch_user_data):
        mock_user_data = [
            {
                'userId': 1,
                'lastSeenDate': '2023-10-27T12:00:00.000',
                'usersOnline': 10
            },
            {
                'userId': 2,
                'lastSeenDate': '2023-10-26T12:00:00.000',
                'usersOnline': 5
            },
        ]

        mock_fetch_user_data.return_value = mock_user_data

        date_str = '2023-10-27 10:00'

        result = historical_data_for_all_users(date_str)

        expected_result = {
            "historical_data": [
                {
                    'user_id': 1,
                    'last_seen_date': datetime(2023, 10, 27, 12, 0),
                    'users_online': 10
                }
            ],
            "total_users": 2
        }

        self.assertEqual(result, expected_result)

    def test_get_user_by_id_found(self):
        user_data = [
            {
                'userId': 'user1',
                'name': 'User One',
                'email': 'user1@example.com',
            },
            {
                'userId': 'user2',
                'name': 'User Two',
                'email': 'user2@example.com',
            },
        ]

        user_id_to_find = 'user1'

        found_user = get_user_by_id(user_data, user_id_to_find)


        self.assertEqual(found_user, user_data[0])

    def test_get_user_by_id_not_found(self):

        user_data = [
            {
                'userId': 'user1',
                'name': 'User One',
                'email': 'user1@example.com',
            },
            {
                'userId': 'user2',
                'name': 'User Two',
                'email': 'user2@example.com',
            },
        ]

        user_id_to_find = 'user3'

        found_user = get_user_by_id(user_data, user_id_to_find)

        self.assertIsNone(found_user)

    def test_users_online_at_date(self):
        user_data = [
            {
                'userId': 'user1',
                'lastSeenDate': '2023-10-27T12:00:00.000',
            },
            {
                'userId': 'user2',
                'lastSeenDate': '2023-10-26T12:00:00.000',
            },
            {
                'userId': 'user3',
                'lastSeenDate': '2023-10-27T14:00:00.000',
            },
        ]

        date_to_check = datetime_from_iso('2023-10-27T13:00:00.000')

        online_users = users_online_at_date(user_data, 'user1', date_to_check)

        expected_result = [
            {
                'user_id': 'user1',
                'last_seen_date': datetime_from_iso('2023-10-27T12:00:00.000')
            },
            {
                'user_id': 'user3',
                'last_seen_date': datetime_from_iso('2023-10-27T14:00:00.000')
            }
        ]

        self.assertEqual(online_users, expected_result)

    def test_find_nearest_online_time_user_not_online(self):
        user_data = [
            {
                'userId': 'user1',
                'lastSeenDate': '2023-10-27T12:00:00.000',
            },
            {
                'userId': 'user2',
                'lastSeenDate': '2023-10-26T12:00:00.000',
            },
            {
                'userId': 'user3',
                'lastSeenDate': '2023-10-27T14:00:00.000',
            },
        ]

        user_id = 'user2'
        date_to_check = datetime_from_iso('2023-10-27T13:00:00.000')

        result, nearest_time = find_nearest_online_time(user_data, user_id, date_to_check)

        self.assertFalse(result)
        self.assertEqual(nearest_time, datetime_from_iso('2023-10-27T12:00:00.000'))

    def test_find_nearest_online_time_user_not_found(self):
        user_data = [
            {
                'userId': 'user1',
                'lastSeenDate': '2023-10-27T12:00:00.000',
            },
            {
                'userId': 'user2',
                'lastSeenDate': '2023-10-26T12:00:00.000',
            },
            {
                'userId': 'user3',
                'lastSeenDate': '2023-10-27T14:00:00.000',
            },
        ]

        user_id = 'user4'
        date_to_check = datetime_from_iso('2023-10-27T13:00:00.000')

        result, nearest_time = find_nearest_online_time(user_data, user_id, date_to_check)

        self.assertIsNone(result)
        self.assertIsNone(nearest_time)

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

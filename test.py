import unittest
from unittest.mock import patch
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


if __name__ == '__main__':
    unittest.main()

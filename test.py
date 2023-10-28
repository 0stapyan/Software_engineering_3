import unittest
from main import fetch_user_data, historical_data_for_all_users, predict_users_online, predict_user_online

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

    if __name__ == '__main__':
        unittest.main()


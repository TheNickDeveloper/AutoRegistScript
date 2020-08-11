import unittest
import Models.EmaiModel as email_model
import Models.AccountDetails as account_detail

class TestEmailModel(unittest.TestCase):


    def test_account_details(self):
        ac_detail = account_detail.AccountDetails(1,"Nick","nick@test.com","GZ")
        self.assertEqual(ac_detail.user_id,1)
        self.assertEqual(ac_detail.email_address,"nick@test.com")
        self.assertEqual(ac_detail.region,"GZ")
        self.assertTrue(isinstance(ac_detail, account_detail.AccountDetails))


    def test_account_email_model(self):
        ac_detail = account_detail.AccountDetails(1,"Nick","nick@test.com","GZ")
        email = email_model.Email(ac_detail)

        self.assertEqual(email.to, "nick@test.com")

        body = f'''
                hi {ac_detail.user_name}<br/>
                <br/>
                Please note your account enroll has completed. <br/>
                Account: {ac_detail.user_id}<br/>
                Password: 1111<br/>
                <br/>
                BR<br/>
                Nick Tsai
            '''
        self.assertEqual(email.body, body)

        self.assertEqual(email.subject, "Enroll account completed")
        self.assertTrue(isinstance(email, email_model.Email))


if __name__ == '__main__':
    unittest.main()

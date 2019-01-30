import unittest
from sms_1 import sms

class test_sms(unittest.TestCase):

    def setUp(self):
        self.sms_obj = sms()

    def test_succes_scenario(self):
        acc_bal = self.sms_obj.get_account_balance()
        tns = self.sms_obj.get_all_numbers()
        uuid = self.sms_obj.send_msg(tns[0], tns[1])
        msg_price = self.sms_obj.get_message_detail(uuid)
        us_pricing = self.sms_obj.get_sms_pricing_details()
        self.assertEquals(msg_price,us_pricing)
        after_balance = self.sms_obj.get_account_balance()
        self.assertEquals(after_balance,acc_bal-msg_price)


    def test_wrong_number(self):
        acc_bal = self.sms_obj.get_account_balance()
        tns = self.sms_obj.get_all_numbers()
        uuid = self.sms_obj.send_msg(tns[0], '1234')
        self.assertNotEqual(uuid,202)

if __name__ == '__main__':
    unittest.main()






import requests
import base64
import json

class sms:
    def __init__(self):
        self.auth_id = 'MAODUZYTQ0Y2FMYJBLOW'
        self.auth_token = 'ODgyYmQxYTQ2N2FkNDFiZTNhZWY4MDAwYWY4NzY0'
        self.request_url = 'https://api.plivo.com/v1/Account/'
        self.authorization = base64.b64encode(self.auth_id+':'+self.auth_token)


    def get_account_balance(self): #wont be needed - Can be removed
        resp = requests.get(self.request_url+self.auth_id,headers={'Authorization':'Basic '+self.authorization})
        resp.raise_for_status() ## Fails if 4xx or 5xx status code
        account_balance = json.loads(resp.text)

        return float(account_balance['cash_credits'])

    def get_all_numbers(self):
        headers = {'type':'', 'Authorization': 'Basic '+self.authorization}
        resp = requests.get(self.request_url + self.auth_id + '/Number/' , headers = headers)
        numbers = json.loads(resp.text)
        tn_count = numbers['meta']['total_count']
        tn = []
        for x in range(0,tn_count,1):
            tn.append(numbers['objects'][x]['number'])


        return tn

    def send_msg(self, number1, number2): #can handle only 2 TNs since the account has 2 numbers
        headers = {'Authorization': 'Basic '+self.authorization,'Content-Type': 'application/json'}
        body = {'src':number1 , 'dst':number2, 'text': 'Hello, Test message from Plivo'}
        resp = requests.post(self.request_url+self.auth_id+'/Message/', data = json.dumps(body), headers = headers )
        if resp.status_code != 202:
            return resp.status_code

        json_data = json.loads(resp.text)
        msg_uuid = json_data['message_uuid'][0]


        return msg_uuid

    def get_message_detail(self, msg_uuid):
        headers = {'Authorization': 'Basic '+self.authorization}
        resp = requests.get(self.request_url+self.auth_id+'/Message/'+msg_uuid+'/', headers = headers)
        json_data = json.loads(resp.text)
        resp.raise_for_status()  ## Fails if 4xx or 5xx status code
        return float(json_data['total_amount'])  # ammount decucted for this sms

    def get_sms_pricing_details(self):
        headers = {'Authorization': 'Basic ' + self.authorization}
        query_string = {'country_iso':'US'} #kept it only for US region
        resp = requests.get(self.request_url+self.auth_id+'/Pricing/', headers=headers, params= query_string)
        json_data = json.loads(resp.text)
        resp.raise_for_status()  ## Fails if 4xx or 5xx status code
        #return the sms pricing for US
        return  float(json_data['message']['outbound']['rate'])


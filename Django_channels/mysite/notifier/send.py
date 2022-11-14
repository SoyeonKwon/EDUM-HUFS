# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
# if __name__ == "__main__":
#
#     # set api key, api secret
#     api_key = "NCS6DX5TVMC0XKUF"
#     api_secret = "QAGSWWBHCMTBZFEOQK6G0KMZE4DMJRBH"
#
#     ## 4 params(to, from, type, text) are mandatory. must be filled
#     params = dict()
#     params['type'] = 'sms' # 메세지 타입 ( sms, lms, mms, ata )
#     params['to'] = '01043655330' # 전송받는 번호
#     params['from'] = '01035419130' # 전송하는 번호
#     params['text'] = 'hello' # 보낼 메세지
#
#     cool = Message(api_key, api_secret)
#
#     try:
#         response = cool.send(params)
#         print("Success Count : %s" % response['success_count'])
#         print("Error Count : %s" % response['error_count'])
#         print("Group ID : %s" % response['group_id'])
#
#         if "error_list" in response:
#             print("Error List : %s" % response['error_list'])
#
#     except CoolsmsException as e:
#         print("Error Code : %s" % e.code)
#         print("Error Message : %s" % e.msg)
#
#     sys.exit()

class Sendsms:
    def __init__(self, phone_number, place, text):
        self.phone_number = phone_number
        self.place = place
        self.text = text

    def sendSms(self):
        # set api key, api secret
        api_key = "NCS6DX5TVMC0XKUF"
        api_secret = "QAGSWWBHCMTBZFEOQK6G0KMZE4DMJRBH"

        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = self.phone_number # Recipients Number '01000000000,01000000001'
        params['from'] = '01035419130'  # Sender number
        params['text'] = self.place + ' 카메라에 ' + self.text + '한 상황이 발생하였습니다.' # Message

        cool = Message(api_key, api_secret)

        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        sys.exit()

def run(phone_number, cam_location, s_type):
    use = Sendsms(phone_number, cam_location, s_type)
    use.sendSms()

# if __name__ == "__main__":
#     run()
#!/usr/bin/env python
'''
Webex functions to send messages using a bot

-------------------------------------------------------------------------
Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

import os
import pathlib
import requests

def send_message(token, room_id=None, email=None, message:str=None, card:dict=None):
    '''
    Function to send a Webex message 1:1 based on an email address or a Webex room based on the room_id.
    '''

    if room_id:
        payload = {
            "roomId":room_id
        }
    else:
        payload = {
            "toPersonEmail":email
        }

    if not card:
        print(f"Sending message: {message}")
        payload["markdown"] = message

    else:
        payload["text"] = "This is an adaptive card"
        payload["attachments"] = [card]

    url = "https://webexapis.com/v1/messages"

    headers = {
        "authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"Status code of sending the Webex message: {response.status_code}")

    if not response.ok:
        raise Exception(f"Error: {response.text}")

    return response.json()

def create_card_payload(template:str, section_title:str, title:str, text_list:list):
    '''Create a card payload from Jinja2 template and values from YAML file.'''
    import jinja2,json

    with open(template, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())

    try:
        card = template.render(section_title=section_title, title=title, text_list=text_list)
        return json.loads(card)
    except Exception as err:
        raise Exception("Card creation failed.") from err


if __name__ == "__main__":
    webex_token = os.getenv("WEBEX_TOKEN")
    space = os.getenv("WEBEX_ROOM")


    status_card_path = (pathlib.Path(__file__).parent).joinpath('cards', 'status_update_card.j2')
    approval_card_path = (pathlib.Path(__file__).parent).joinpath('cards', 'approval_card.j2')


    approval_input = [
        {
            "title": "Change ticket",
            "value": "#12345"
        },


        {
            "title": "Change type",
            "value": "VLAN change"
        },

        {
            "title": "Device",
            "value": "rtr-esp-access-1"
        },

        {
            "title": "Interface",
            "value": "GigabitEthernet"
        },

        {
            "title": "New VLAN",
            "value": "15"
        }
    ]

    status_update_input = [
        {"text":"❌ Ping test failed ❌", "bold": True},
        {"text":"10.105.22.34 is unreachable", "bold":False}
        ]

    status_update = create_card_payload(template=status_card_path,
                                         section_title="Status update",
                                         title="Test results",
                                         text_list=status_update_input)

    approval_card = create_card_payload(template=approval_card_path,
                                         section_title="REQUESTING APPROVAL",
                                         title="VLAN Update",
                                         text_list=approval_input)

    send_message(webex_token, space, card=status_update)
    send_message(webex_token, space, card=approval_card)
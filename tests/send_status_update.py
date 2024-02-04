import os
from pyats import results
import pathlib
from .webex import webex_functions


def send_status_update(section_results, title):

    text_list = _form_message(section_results)
    section_title = "Status update"

    status_card_path = (pathlib.Path(__file__).parent).joinpath('webex','cards', 'status_update_card.j2')

    status_update = webex_functions.create_card_payload(
                                        template=status_card_path,
                                         section_title=section_title,
                                         title=title,
                                         text_list=text_list)

    webex_token = os.getenv("WEBEX_TOKEN")
    space = os.getenv("WEBEX_ROOM")
    webex_functions.send_message(webex_token, space, card=status_update)


def _form_message(section_results):

    if section_results['result'] == results.Passed:
        result_text = "✅ Ping test passed ✅"
    elif section_results['result'] == results.Failed:
        result_text = "❌ Ping test failed ❌"
    else:
        result_text = f"Ping not successful: {str(results['result'])}"

    text_list = [
        {"text":result_text, "bold":True},
    ]

    for section in section_results['sections']:
        if section['result'] == results.Passed:
            icon = "✅"
        elif section['result'] == results.Failed:
            icon = "❌"
        else:
            icon = "🚧"
        text_list.append(
            {
                "text":f"- {section['name']} ➡️ {str(section['result'])} {icon}",
                "bold":False
            }
        )
    return text_list

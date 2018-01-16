# encoding: utf-8

import sys
from workflow import Workflow, web
import urllib
from config import channels

api_url = 'https://api.elisaviihde.fi/etvrecorder/ajaxprograminfo.sl'

def main(wf):
    for channel in channels:
        now_and_next_progs = wf.cached_data(
            'now_and_next_' + channel,
            lambda: get_now_and_next_program(channel),
            max_age=60
        )

        wf.add_item(
            title=channel,
            subtitle=urllib.unquote(
                now_and_next_progs
            ).decode('utf8'),
            arg=channel,
            valid=True,
            icon='icons/{}.png'.format(channel)
        )

    # Send the results to Alfred as XML
    wf.send_feedback()


def get_now_and_next_program(channel):
    params = {'24h': channel}
    r = web.get(api_url, params)

    r.raise_for_status()

    result = r.json()

    programs = result['programs']

    now_and_next_progs = '{} - {} - {}'.format(
        programs[0]['name'].encode('utf-8'),
        programs[0]['simple_end_time'],
        programs[1]['name'].encode('utf-8'),
    )

    return now_and_next_progs


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))


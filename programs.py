# encoding: utf-8

import sys
from workflow import Workflow, web
import urllib
from config import api_url, channels

def main(wf):
    channel = sys.argv[1]

    if channel not in channels:
        return

    programs = wf.cached_data(
        channel + ' programs',
        lambda: get_programs(channel),
        max_age=60
    )

    for program in programs:
        wf.add_item(
            arg=program['id'],
            title=urllib.unquote(
                program['name'].encode('utf-8')
            ).decode('utf8'),
            subtitle='{} - {}'.format(
                program['simple_start_time'], program['simple_end_time']
            ),
            valid=True,
            icon='icons/{}.png'.format(channel)
        )

    # Send the results to Alfred as XML
    wf.send_feedback()


def get_programs(channel):
    params = {'24h': channel}
    r = web.get(api_url, params)

    r.raise_for_status()

    result = r.json()

    return result['programs']


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))


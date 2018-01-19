# encoding: utf-8

import sys
from workflow import Workflow, web
import urllib
from config import api_url

def main(wf):
    program = sys.argv[1]

    program_data = wf.cached_data(
        program + ' data',
        lambda: get_program_data(program),
        max_age=600
    )

    if not program_data:
        return

    # Title
    wf.add_item(
        title=urllib.unquote(
            program_data['name'].encode('utf-8')
        ).decode('utf8'),
        valid=True,
        icon='icons/title.png'
    )

    # Description
    wf.add_item(
        title=urllib.unquote(
            program_data['short_text'].encode('utf-8')
        ).decode('utf8'),
        subtitle=urllib.unquote(
            program_data['description'].encode('utf-8')
        ).decode('utf8'),
        valid=False,
        icon='icons/description.png'
    )

    # Channel
    wf.add_item(
        arg=program_data['channel'],
        title=urllib.unquote(
            program_data['channel'].encode('utf-8')
        ).decode('utf8'),
        subtitle='Go back to {}'.format(program_data['channel']),
        valid=True,
        icon='icons/{}.png'.format(program_data['channel'])
    )

    # Duration
    wf.add_item(
        title=program_data['flength'],
        valid=False,
        icon='icons/duration.png'
    )

    # Start time
    wf.add_item(
        title=program_data['simple_start_time'],
        valid=False,
        icon='icons/start-time.png'
    )

    # End time
    wf.add_item(
        title=program_data['simple_end_time'],
        valid=False,
        icon='icons/end-time.png'
    )

    # Send the results to Alfred as XML
    wf.send_feedback()


def get_program_data(program):
    params = {'programid': program}
    r = web.get(api_url, params)

    r.raise_for_status()

    result = r.json()

    return result


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))


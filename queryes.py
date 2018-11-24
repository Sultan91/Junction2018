import json
from datetime import datetime
from typing import Dict

import requests


def get_thermalimage_by_dates(date_from: datetime, date_to: datetime):
    """
    Returns requests.Response for 'thermalimage' by dates range
    """
    # correct time template for the API
    time_template = '%Y-%m-%dT%H:%M:%S.%fZ'
    # Specified data for every query ('thermalimage' or '/alerts/priorities' or ...) this one for thermalimage
    data = {"timeDateFrom": date_from.strftime(time_template), "timeDateTo": date_to.strftime(time_template)}
    params = {'itemCount': 10, 'startIndex': 0}
    return __post_query_to_site(data=data, params=params, path='thermalimage')


def __post_query_to_site(data: Dict, params: Dict, path='', site: str = 'site_exp') -> requests.Response:
    """
    General function for posting query to the API
    :param data: data to send: dictionary with 'timeDateFrom' or whatever
    :param params: params in url like 'itemCount', 'startIndex' or ....
    :param path: path after site_id in query, like 'thermalimage' or '/alerts/priorities' or ...
    :param site: by default it is 'site_exp'
    :return: requests.Response
    """
    headers = {'x-api-key': 'scaWPobgxn4A8UhdqIBbR3tZZecEcdsC9WtwMcuP',
               'content-type': 'application/json',
               'accept': 'application/json'}
    return requests.post(f'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/{site}/{path}',
                         data=json.dumps(data), headers=headers, params=params)


if __name__ == '__main__':
    # An example for thermalimage
    date_from = datetime(year=2018, month=10, day=10, hour=11, minute=25)
    date_to = datetime(year=2018, month=10, day=10, hour=12, minute=0)
    result_q = get_thermalimage_by_dates(date_from, date_to)
    print(result_q.json())

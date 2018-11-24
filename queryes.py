import json
from datetime import datetime
from typing import Dict, Optional, List, Callable

import requests


def get_thermalimage_by_dates(date_from: datetime, date_to: datetime, item_count: int = 0,
                              start_index: int = 0) -> requests.Response:
    """
    Returns requests.Response for 'thermalimage' by dates range
    """
    # correct time template for the API
    time_template = '%Y-%m-%dT%H:%M:%S.%fZ'
    # Specified data for every query ('thermalimage' or '/alerts/priorities' or ...) this one for thermalimage
    data = {"timeDateFrom": date_from.strftime(time_template), "timeDateTo": date_to.strftime(time_template)}
    return __post_query_to_site(data=data, item_count=item_count, start_index=start_index, path='thermalimage')


def extract_data_from_thermalimage_response(response: requests.Response) -> List[Dict]:
    """
    Extracting image information from response
    :param response: response from thermalimage
    :return: list of dicts in format [{'date': 'image_array'}, {...}, ... ]
    """
    items = response.json()['data']['items']
    result_list = []
    for item in items:
        item_time = item['captureTime']
        result_list.append({item_time: item['image']})
    return result_list


def get_all_data_from_device(func: Callable, func_kwargs: Dict, func_extract: Callable) -> List[Dict]:
    """
    Returned list of data using 'function' and 'function_filter'
    :param func: function to get data
    :param func_kwargs: kwargs for the above function
    :param func_extract: function to extract_data
    :return: List of Dicts, which contains data
    """
    _item_count = 10
    _start_index = 0
    result_list = []
    is_data = True
    func_kwargs['item_count'] = _item_count
    func_kwargs['start_index'] = _start_index

    while is_data:
        # get and process data
        response: requests.Response = func(**func_kwargs)
        returned_list = func_extract(response)
        result_list.extend(returned_list)

        # check if there is more data
        is_data = response.json()['data']['hasMoreItems']

        # change start index position to new data
        _start_index = _start_index + response.json()['data']['currentItemCount']
        func_kwargs['start_index'] = _start_index

    return result_list


def __post_query_to_site(data: Dict, item_count: int = 0, start_index: int = 0, params: Optional[Dict] = None,
                         path: str = '', site: str = 'site_exp') -> requests.Response:
    """
    General function for posting query to the API
    :param data: data to send: dictionary with 'timeDateFrom' or whatever
    :param params: params in url like 'itemCount', 'startIndex'
    :param path: path after site_id in query, like 'thermalimage' or '/alerts/priorities' or ...
    :param site: by default it is 'site_exp'
    :return: requests.Response
    """
    headers = {'x-api-key': 'scaWPobgxn4A8UhdqIBbR3tZZecEcdsC9WtwMcuP',
               'content-type': 'application/json',
               'accept': 'application/json'}

    if not params:
        params = dict()
    if item_count:
        params['itemCount'] = item_count
    if start_index:
        params['startIndex'] = start_index

    return requests.post(f'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/{site}/{path}',
                         data=json.dumps(data), headers=headers, params=params, timeout=10)


if __name__ == '__main__':
    # An example for thermalimage
    date_from = datetime(year=2018, month=10, day=10, hour=11, minute=25)
    date_to = datetime(year=2018, month=10, day=10, hour=12, minute=0)
    data = get_all_data_from_device(get_thermalimage_by_dates, {'date_from': date_from, 'date_to': date_to},
                                    extract_data_from_thermalimage_response)
    print(data)

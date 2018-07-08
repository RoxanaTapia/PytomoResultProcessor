import datetime
import re


def get_results(results):
    """
    Creates a list with items in results file.

    :param results: String with the pytomo result data
    :return: list of single results
    """
    # important: insert a new line at EOF to match the last item
    items = re.compile(r"[\s\S]*?(?=\n{2,})").findall(results)
    return [item for item in items if item]


def is_valid(object):
    """
    Checks if the object contains all data described in schema @resources/pytomo_result_schema.

    :param object: A python object of a single result
    :return: True if object contains all fields in schema, False otherwise
    """
    valid_result_size = len(object) == 3
    if valid_result_size:
        gs_keys = list(object[2].keys())
        if gs_keys:
            general_stats_key = gs_keys[0]
            general_stats = object[2][general_stats_key]
            valid_general_stats_size = len(general_stats) == 8
            if valid_general_stats_size:
                download_stats = general_stats[2]
                if download_stats and len(download_stats) == 15:
                    return True
    return False


def get_dict_item(result):
    """
    Puts a result item in a dictionary structure according to schema @resources/pytomo_result_schema.

    :param result: String with a single pytomo result
    :return: A dict item with the result if valid, None otherwise
    """
    object = eval(result)

    if not is_valid(object):
        return

    gs_key = list(object[2].keys())[0]
    gs_data = object[2][gs_key]

    ds_data = gs_data[2]
    download_stats = dict(
        download_time=ds_data[0],
        video_type=ds_data[1],
        data_duration=ds_data[2],
        data_len=ds_data[3],
        encoding_rate=ds_data[4],
        total_bytes=ds_data[5],
        interruptions=ds_data[6],
        initial_data=ds_data[7],
        initial_rate=ds_data[8],
        initial_playback_buffer=ds_data[9],
        accumulated_buffer=ds_data[10],
        accumulated_playback=ds_data[11],
        current_buffer=ds_data[12],
        time_to_get_first_byte=ds_data[13],
        max_instant_thp=ds_data[14],
    )

    general_stats = dict(
        ip_address=gs_key,
        timestamp=gs_data[0],
        ping_times=gs_data[1],
        download_stats=download_stats,
        redirect_url=gs_data[3],
        resolver=gs_data[4],
        req_time=gs_data[5],
        cached_prefix=gs_data[6],
        status_code=gs_data[7]
    )

    dict_item = dict(
        video_url=object[0],
        cache_url=object[1],
        general_stats=general_stats,
    )

    return dict_item


if __name__ == '__main__':

    filename = "resources/test.txt"
    filename = "resources/pytomo_results_1.txt"
    content = open(filename, "r").read()
    results = get_results(content)

    data = list()
    for result in results:
        dict_item = get_dict_item(result)
        if dict_item:
            data.append(dict_item)

    print("Results available: {number}".format(number=len(results)))
    print("Valid results processed: {number}".format(number=len(data)))




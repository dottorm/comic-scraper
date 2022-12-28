import os
import datetime

def get_dates_list(start_date, end_date):
    """
    Produces a list of dates between the given boundaries.
    :param start_date: Starting date for the date range.
    :param end_date: Ending date for the date range.
    :return: A list of dates.
    """
    return [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]


def create_dir(dir_name):
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)
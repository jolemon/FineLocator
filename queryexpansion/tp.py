import time

time_format = "%a %b %d %H:%M:%S %Z %Y"


def cal_time_diff_by_second(time_str1, time_str2):
    seconds1 = time.mktime(time.strptime(time_str1, time_format))
    seconds2 = time.mktime(time.strptime(time_str2, time_format))
    return abs(seconds1-seconds2)


def load_all_last_modify_time(proj_path):
    dic = {}
    return dic


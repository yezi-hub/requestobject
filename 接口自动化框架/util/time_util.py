import time

def get_date():
    year = str(time.localtime().tm_year)
    month = str(time.localtime().tm_mon)
    day = str(time.localtime().tm_mday)
    return year+"-"+month+"-"+day

def get_time():
    hour = str(time.localtime().tm_hour)
    min = time.localtime().tm_min
    if min<10:
        min="0"+str(min)
    sec = str(time.localtime().tm_sec)
    return hour+":"+str(min)+":"+sec

def get_date_time():
    return get_date()+" "+get_time()

def get_chinese_date():
    year = str(time.localtime().tm_year)
    month = str(time.localtime().tm_mon)
    day = str(time.localtime().tm_mday)
    return year+"年"+month+"月"+day+"日"

def get_chinese_time():
    hour = str(time.localtime().tm_hour)
    min = time.localtime().tm_min
    if min<10:
        min="0"+str(min)
    sec = str(time.localtime().tm_sec)
    return hour+"时"+str(min)+"分"+sec+"秒"

def get_chinese_date_time():
    return get_chinese_date()+get_chinese_time()

def get_chinese_hour():
    hour = str(time.localtime().tm_hour)
    return str(hour)+"时"

def get_chinese_min():
    min = str(time.localtime().tm_min)
    return str(min)+"分"


if __name__ == "__main__":
    print(get_date())
    print(get_time())
    print(get_date_time())
    print(get_chinese_date())
    print(get_chinese_time())
    print(get_chinese_date_time())
    print(get_chinese_hour())
    print(get_chinese_min())
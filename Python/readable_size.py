import math
from GS_timing import millis


def get_size_loop(size, precision=2):
    """
    This function return file size in readable form
    Reference: https://stackoverflow.com/a/1094933/7099900
    @param int size: file size
    @param int precision: precision of float number in string
    return string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if abs(size) < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{precision}f} {unit}"


def get_size_log(size, precision=2):
    """
    This function return file size in readable form
    Reference: https://stackoverflow.com/a/18650828/7099900
    @param int size: file size
    @param int precision: precision of float number in string
    return string
    """
    if size == 0:
        return '0 bytes'
    k = 1024
    decimals = 0 if precision < 0 else precision
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    i = math.floor(math.log(size)/math.log(k))
    return f"{size/math.pow(k, i):.{decimals}f} {suffixes[i]}"


def get_size_mini(a, b=2, k=1024):
    """
    This function return file size in readable form
    Reference: https://stackoverflow.com/a/18650828/7099900
    @param int size: file size
    @param int precision: precision of float number in string
    return string
    """
    d = math.floor(math.log(a)/math.log(k))
    return "0 B" if a == 0 else f'{a/pow(k, d):.{max(0, b)}f} {["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"][d]}'


def human_read_to_byte_1(size):
    """
    This function return file size in byte form
    Slightly faster than func3 for the first few time
    Reference: https://stackoverflow.com/a/56243838/7099900
    @param int size: file size, ex: '1 PB'
    return int
    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size = size.split(' ')                # divide '1 GB' into ['1', 'GB']
    num, unit = float(size[0]), size[1]
    # index in list of sizes determines power to raise it to
    idx = size_name.index(unit)
    # ** is the "exponent" operator - you can use it instead of math.pow()
    factor = 1024 ** idx
    return num * factor


def human_read_to_byte_2(size):
    """
    This function return file size in byte form
    Reference: https://stackoverflow.com/a/56244082/7099900
    @param int size: file size, ex: '1 PB'
    return int
    """
    CONVERSION_FACTORS = {"B": 1, "KB": 1024, "MB": 1048576, "GB": 1073741824, "TB": 1099511627776,
                          "PB": 1125899906842624, "EB": 1152921504606846976, "ZB": 1180591620717411303424,
                          "YB": 1208925819614629174706176}
    num_ndx = 0
    while num_ndx < len(size):
        if str.isdigit(size[num_ndx]) or size[num_ndx] == '.':
            num_ndx += 1
        else:
            break
    num_part = float(size[:num_ndx])
    str_part = size[num_ndx:].strip().upper()
    return num_part * CONVERSION_FACTORS[str_part]


def human_read_to_byte_3(size):
    """
    This function return file size in byte form
    Slightly faster than func1 if used multiple times (might be cache)
    Reference: https://stackoverflow.com/a/62220318/7099900
    @param int size: file size, ex: '1 PB'
    return int
    """
    factors = {'B': 1, 'KB': 1024, 'MB': 1048576, 'GB': 1073741824, 'TB': 1099511627776, 'PB': 1125899906842624,
               'EB': 1152921504606846976, 'ZB': 1180591620717411303424, 'YB': 1208925819614629174706176}
    if size[-2:] in factors:
        return factors[size[-2:]]*float(size[:-2])
    return float(size[:-1])


if __name__ == "__main__":
    n = 100000
    size = 1.51234e13  # bytes

    print("*** bytes -> human ***")
    precision = 4
    flist = [get_size_loop, get_size_log, get_size_mini]
    for f in flist:
        t1 = millis()
        for _ in range(n):
            f(size, precision)
        t2 = millis()
        print(f'{f.__name__:20s} : {f(size, precision):>18s} : {t2-t1:.2f} ms')

    print("*** human -> bytes ***")
    size = get_size_loop(size, precision)
    flist = [human_read_to_byte_1, human_read_to_byte_2, human_read_to_byte_3]
    for f in flist:
        t1 = millis()
        for _ in range(n):
            f(size)
        t2 = millis()
        print(f'{f.__name__:20s} : {f(size):16.{precision}e} B : {t2-t1:.2f} ms')

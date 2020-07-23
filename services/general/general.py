
def get_mb_from_bytes(size):
    """Get megabytes from a size in bytes

    :param size: Integer value in bytes
    """
    return size/1024/1024


def get_mb_from_bytes_round(size, ndigits=2):
    """Get megabytes from a size in bytes and specific digits

    :param size: Integer value in bytes
    :param ndigits: Number of decimals
    """
    return round(get_mb_from_bytes(size), ndigits)

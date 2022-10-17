import datetime


def finditemsinlistwithbisect(itemlist: list, attrname: str, object) -> list:
    leftindex = bisectleftwithattribute(itemlist, object, attrname)
    rightindex = bisectrightwithattribute(itemlist, object, attrname)

    return itemlist[leftindex:rightindex]


def bisectleftwithattribute(a, x, attr: str, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if isinstance(x, int):
        xattr = x
    elif isinstance(x, str):
        xattr = x
    elif isinstance(x, dict):
        xattr = x[attr]
    elif isinstance(x, datetime.date):
        xattr = x
    else:
        try:
            xattr = getattr(x, attr)
        except AttributeError:
            xattr = x[attr]

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        try:
            if (getattr(a[mid], attr) if attr != '' else a[mid]) < xattr:
                lo = mid+1
            else:
                hi = mid
        except AttributeError:
            if (a[mid][attr] if attr != '' else a[mid]) < xattr:
                lo = mid + 1
            else:
                hi = mid
    return lo


def bisectrightwithattribute(a, x, attr: str, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if isinstance(x, int):
        xattr = x
    elif isinstance(x, str):
        xattr = x
    elif isinstance(x, dict):
        xattr = x[attr]
    elif isinstance(x, datetime.date):
        xattr = x
    else:
        try:
            xattr = getattr(x, attr)
        except AttributeError:
            xattr = x[attr]

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        try:
            if xattr < (getattr(a[mid], attr) if attr != '' else a[mid]):
                hi = mid
            else:
                lo = mid+1
        except AttributeError:
            if xattr < (a[mid][attr] if attr != '' else a[mid]):
                hi = mid
            else:
                lo = mid + 1
    return lo

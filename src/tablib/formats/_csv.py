""" Tablib - *SV Support.
"""

import csv
from io import StringIO


title = 'csv'
extensions = ('csv',)


DEFAULT_DELIMITER = ','


def export_stream_set(dataset, **kwargs):
    """Returns CSV representation of Dataset as file-like."""
    stream = StringIO()

    kwargs.setdefault('delimiter', DEFAULT_DELIMITER)

    _csv = csv.writer(stream, **kwargs)

    for row in dataset._package(dicts=False):
        _csv.writerow(row)

    stream.seek(0)
    return stream


def export_set(dataset, **kwargs):
    """Returns CSV representation of Dataset."""
    stream = export_stream_set(dataset, **kwargs)
    return stream.getvalue()


def import_set(dset, in_stream, headers=True, **kwargs):
    """Returns dataset from CSV stream."""

    dset.wipe()

    kwargs.setdefault('delimiter', DEFAULT_DELIMITER)

    rows = csv.reader(StringIO(in_stream), **kwargs)
    for i, row in enumerate(rows):

        if (i == 0) and (headers):
            dset.headers = row
        elif row:
            dset.append(row)


def detect(stream, delimiter=DEFAULT_DELIMITER):
    """Returns True if given stream is valid CSV."""
    try:
        csv.Sniffer().sniff(stream[:1024], delimiters=delimiter)
        return True
    except Exception:
        return False

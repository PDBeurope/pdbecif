__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"

import gzip
import mimetypes

def openGzip(file_path, mode='r'):
    try:
        return (
            gzip.open(file_path, mode) if mimetypes.guess_type(
                file_path)[1] == 'gzip' else open(file_path, mode)
        )
    except Exception as gzip_io_error:
        print('[Error opening mmCIF file]: %s' % gzip_io_error.message)
        return None

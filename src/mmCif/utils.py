__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"

import gzip
import mimetypes

def get_column(mat, i):
    return [row[i] for row in mat]

def pretty_print(mat, transpose=False):
    out = []
    n_cols = len(mat[0])

    if not transpose:
        lens = [max(map(len, get_column(mat, i))) for i in range(n_cols)]

        for row in mat:
            out.append(" ".join([val.rjust(l) for val, l in zip(row, lens)]))
    else:
        lens = [max(map(len, row)) for row in mat]

        for i in range(n_cols):
            out.append(" ".join([val.rjust(l) for val, l in zip(get_column(mat, i), lens)]))

    return "\n".join(out)

def openGzip(file_path, mode='rt'):
    try:
        return (
            gzip.open(file_path, mode) if mimetypes.guess_type(
                file_path)[1] == 'gzip' else open(file_path, mode)
        )
    except Exception as gzip_io_error:
        print('[Error opening mmCIF file]: %s' % gzip_io_error.message)
        return None

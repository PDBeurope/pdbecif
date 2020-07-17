# -*- coding: utf-8 -*-

# Copyright © 2011, 2013 Global Phasing Ltd. All rights reserved.
# 
# Author: Peter Keller
# 
# This file forms part of the GPhL StarTools library.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#
#  Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the
#  distribution.
#
#  If the regular expression used to match STAR/CIF data in the
#  redistribution is not identical to that in the original version,
#  this fact must be stated wherever the copyright notice is
#  reproduced.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import mmap
import re
import sys
from . import star_regex
from . import star_token_types

PY3 = sys.version_info[0] == 3

if PY3:
    import io

_star_pattern = re.compile(star_regex.REGEX, flags=re.UNICODE)

class StarTokeniser(object):
    """
    Simple wrapper around re.RegexObject.finditer() that emits StarToken instances
    """
    
    def __init__(self):
        self.__map = None
        self.__iterator = None
    
    def start_matching(self, cif):
        """
        Clear any existing state of this object, and prepare to start matching
        against the contents of a file.
        The parameter cif may be a string containing the pathname to a file
        (in which case it is opened in read only mode) or a file object 
        """
        if PY3 and isinstance(cif, io.TextIOBase) or \
                not PY3 and isinstance(cif, file):
            f = cif
        else:
            f = open(cif, "r")

        self.__map = mmap.mmap( f.fileno(), 0, access=mmap.ACCESS_READ )

        if PY3:
            self.__iterator = _star_pattern.finditer(self.__map.read().decode("utf-8"))
        else:
            self.__iterator = _star_pattern.finditer(self.__map)

    def __iter__(self):
        assert self.__map is not None
        return self
    
    def next(self):
        return self.__next__()

    def __next__(self):
        """
        Returns a StarToken instance representing the next token in the matched data.
        Raises StopIteration if there are no further tokens in the data.
        """
        assert self.__map is not None
        m = next(self.__iterator)
        return StarToken( m.lastindex, m.group(m.lastindex) )
        
     
class StarToken(object):
    """
    Class representing a token from STAR data.
    """
    def __init__(self, token_type, token_value):
        self.__token_type = token_type
        self.__token_value = token_value
        
    @property
    def type(self):
        """
        An integer (> 0) representing the type of this STAR token. It corresponds
        to the matching group of the STAR regular expression that matched the value.
        """
        return self.__token_type
    
    @property
    def value(self):
        """
        The value of this STAR token. If it is a quoted data value, it will have
        had any enclosing quotation removed (including the trailing newline in the
        case of semi-colon delimited text). The type of quoting will be indicated by
        the token type.
        """
        return self.__token_value
    
    @property
    def type_string(self):
        """
        The type of this STAR token as a text mnemonic
        """
        return star_token_types._token_type_as_string(self.__token_type)
    
    def __str__(self):
        return "Type: " + self.type_string + "; Value: >>>" + self.value + "<<<"

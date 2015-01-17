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

'''
Created on 25 Nov 2013

@author: pkeller
'''

# These parameters must be kept consistent with the capturing groups
# of the regular expression in star_regex.py

TOKEN_MULTILINE        = 1
TOKEN_COMMENT          = 2
TOKEN_GLOBAL           = 3
TOKEN_SAVE_FRAME       = 4
TOKEN_SAVE_FRAME_REF   = 5
TOKEN_LOOP_STOP        = 6
TOKEN_DATA_BLOCK       = 7
TOKEN_LOOP             = 8
TOKEN_BAD_CONSTRUCT    = 9
TOKEN_DATA_NAME        = 10
TOKEN_SQUOTE_STRING    = 11
TOKEN_DQUOTE_STRING    = 12
TOKEN_NULL             = 13
TOKEN_UNKNOWN          = 14
TOKEN_SQUARE_BRACKET   = 15
TOKEN_STRING           = 16
TOKEN_BAD_TOKEN        = 17

__DESCRIPTIVE_TOKEN_TYPES = [
        "", "MULTILINE", "COMMENT", "GLOBAL", "SAVE_FRAME", "SAVE_FRAME_REF",
        "LOOP_STOP", "DATA_BLOCK", "LOOP", "BAD_CONSTRUCT", "DATA_NAME", "SQUOTE_STRING",
        "DQUOTE_STRING", "NULL", "UNKNOWN", "SQUARE_BRACKET", "STRING", "BAD_TOKEN" ]

def _token_type_as_string(token_type):
    return __DESCRIPTIVE_TOKEN_TYPES[token_type]

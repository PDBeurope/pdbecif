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
#  notice, this list of conditions, the special conditions below
#  relating to the use of the regular expression, and the disclaimer
#  below.
#
#  Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions, the special conditions below
#  relating to the use of the regular expression, and the disclaimer
#  below in the documentation and/or other materials provided with the
#  distribution.
#
#  If the regular expression used to match STAR/CIF data in the
#  redistribution is not identical to that in the original version,
#  this fact must be stated wherever the copyright notice is
#  reproduced.
#
# This file contains the "GPhL StarTools regular expression",
# which is used by the GPhL StarTools library to tokenise STAR data.
# 
# Use of the GPhL StarTools regular expression separately from
# other parts of the GPhL StarTools library, with or without
# modification, in other libraries and applications, in any
# programming language, is permitted provided that the following
# conditions are met (which replace the general conditions
# for use of the GPhL StarTools library in such a case):
#
#  Distributions of libraries or applications in source code
#  form that use the GPhL StarTools regular expression must
#  retain the above copyright notice, this list of conditions
#  and the following disclaimer, and associate them with the
#  StarTools regular expression where it occurs in the source
#  code.
#
#  Distributions of libraries or applications in binary form
#  that use the GPhL StarTools regular expression must reproduce
#  the above copyright notice, this list of conditions and the
#  following disclaimer in the documentation and/or other
#  materials provided with the distribution, and state that they
#  apply to the use of the GPhL StarTools regular expression by
#  the library or application.
#
#  If the GPhL StarTools regular expression has been modified
#  from its original form in the library or application this
#  fact must be stated wherever the copyright notice is
#  reproduced.
#
#  These conditions, the copyright notice, and the included
#  disclaimer apply only to the StarTools regular expression
#  itself, not to any other code with which the regular
#  expression is associated.
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
Created on 22 Nov 2013

@author: pkeller
'''

REGEX = r"""(?xmi) # $Revision: 1.2 $  # No 'u' flag for perl 5.8.8/RHEL5 compatibility
^;([\S\s]*?)(?:\r\n|\s)^;(?:(?=\s)|$)  # Multi-line string
|(?:^|(?<=\s))(\#.*?)\r?$              # Comment
|(?:^|(?<=\s))(?:
  (global_)                            # STAR global block
  |(save_\S*)                          # STAR save frame header or terminator
  |(\$\S+)                             # STAR save frame reference
  |(stop_)                             # STAR nested loop terminator
  |(data_\S+)                          # Data block header
  |(loop_)                             # Loop header
  |((?:global_\S+)|(?:stop_\S+)|(?:data_)|(?:loop_\S+))  # Invalid privileged construct
  |(_\S+)                              # Data name
  |'(.*?)'                             # Single-quoted string
  |"(.*?)"                             # Double-quoted string
  |(\.)                                # CIF null
  |(\?)                                # CIF unknown/missing
  |([\[\]]\S*)                         # Square bracketed constructs (reserved)
  |((?:[^'";_$\s]|(?<!^);)\S*)         # Non-quoted string
  |(\S+)                               # Catch-all bad token
)
(?:(?=\s)|$)"""


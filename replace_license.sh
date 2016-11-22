#!/bin/sh
#
#___INFO__MARK_BEGIN__
##########################################################################
#
#  The Contents of this file are made available subject to the terms of
#  the Sun Industry Standards Source License Version 1.2
#
#  Sun Microsystems Inc., March, 2001
#
#
#  Sun Industry Standards Source License Version 1.2
#  =================================================
#  The contents of this file are subject to the Sun Industry Standards
#  Source License Version 1.2 (the "License"); You may not use this file
#  except in compliance with the License. You may obtain a copy of the
#  License at http://gridengine.sunsource.net/Gridengine_SISSL_license.html
#
#  Software provided under this License is provided on an "AS IS" basis,
#  WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING,
#  WITHOUT LIMITATION, WARRANTIES THAT THE SOFTWARE IS FREE OF DEFECTS,
#  MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE, OR NON-INFRINGING.
#  See the License for the specific provisions governing your rights and
#  obligations concerning the Software.
#
#  The Initial Developer of the Original Code is: Sun Microsystems, Inc.
#
#  Copyright: 2001 by Sun Microsystems, Inc.
#
#  All Rights Reserved.
#
##########################################################################
#___INFO__MARK_END__

# first argument is the name of the script, all other arguments are filenames
# shift discards the first arg0 then loop processes all other args one at a 
# time
#

shift
# loop through all filenames
for var in "$@"
do

   FILE=$var
   TMP_FILE=${FILE}.new

#Remove existing license
   sed -e "/___INFO__MARK_BEGIN__/,/___INFO__MARK_END__/d" $FILE > $TMP_FILE

#Insert new license
   sed '2 i\
\# \
\#___INFO__MARK_BEGIN__ \
\########################################################################## \
\# Copyright 2016,2017 Univa Corporation\
\# \
\# Licensed under the Apache License, Version 2.0 (the "License");\
\# you may not use this file except in compliance with the License.\
\# You may obtain a copy of the License at\
\# \
\#     http://www.apache.org/licenses/LICENSE-2.0 \
\# \
\# Unless required by applicable law or agreed to in writing, software \
\# distributed under the License is distributed on an "AS IS" BASIS, \
\# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. \
\# See the License for the specific language governing permissions and \
\# limitations under the License. \
\########################################################################### \
\#___INFO__MARK_END__ \
\# ' $TMP_FILE > $FILE

#Remove temp file
   rm -f $TMP_FILE

done

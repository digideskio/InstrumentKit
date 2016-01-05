#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# usbtmc_communicator.py: Communicator that uses Python-USBTMC to interface 
#     with TMC devices.
##
# © 2016 Steven Casagrande (scasagrande@galvant.ca).
#
# This file is a part of the InstrumentKit project.
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##

## IMPORTS #####################################################################

import io

from instruments.abstract_instruments.comm.abstract_comm import AbstractCommunicator

try:
    import vxi11
except ImportError:
    vxi11 = None

## CLASSES #####################################################################

class USBTMCCommunicator(io.IOBase, AbstractCommunicator):
    """
    Wraps a VXI11 device. Arguments are passed to `vxi11.Instrument`.
    """
    
    def __init__(self, *args, **kwargs):
        if usbtmc is None:
            raise ImportError("Packge python-vxi11 is required for XVI11 "
                              "connected instruments.")
        AbstractCommunicator.__init__(self)
            
        self._inst = vxi11.Instrument(*args, **kwargs)
    
    ## PROPERTIES ##
    
    @property
    def address(self):
        return [self._inst.host, self._inst.name]
        
    @property
    def terminator(self):
        return self._inst.term_char
    @terminator.setter
    def terminator(self, newval):
        self._inst.term_char = newval
        
    @property
    def timeout(self):
        return self._inst.timeout
    @timeout.setter
    def timeout(self, newval):
        self._inst.timeout = newval # In seconds

    ## FILE-LIKE METHODS ##
    
    def close(self):
        try:
            self._filelike.close()
        except:
            pass
        
    def read(self, size):
        msg = self._inst.read(num=size)
        return msg
        
    def write(self, msg):
        self._inst.write(msg)
        
    def seek(self, offset):
        raise NotImplementedError
        
    def tell(self):
        raise NotImplementedError
        
    def flush(self):
        raise NotImplementedError
        
    ## METHODS ##
    
    def _sendcmd(self, msg):
        self._inst.write(msg)
        
    def _query(self, msg, size=-1):
        return self._inst.ask(msg, num=size)
        

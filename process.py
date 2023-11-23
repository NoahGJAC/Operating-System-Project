import enum
import os
import sys

# ===========================================================================
# Process:
#   - pretends to be a process with data and everything
#   - can set and retrieve "data" using virtual addresses
# entry_point - first address that needs to be executed when a process starts
# size - the size of the process
# get_data(self, vaddr)
# set_data(self,start_vaddr,data)
# ===========================================================================

# STUDENT TODO: Nothing... its all done, just use the code as is

# =================================================================
# FakeProcess class
# =================================================================
class Process:

    # -------------------------------------------------------------
    # static class variables & methods
    # -------------------------------------------------------------
    __pid = 0

    @classmethod
    def __get_new_pid(class_name)->int:
        class_name.__pid = class_name.__pid + 1
        return class_name.__pid

    @classmethod
    def debug(fp, msg):
        if os.getenv("FP_DEBUG") is not None:
            print(fp, msg)

    # -------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------
    def __init__(self, entry_point=0, size=20000):
        self.pid        : int = Process.__get_new_pid()
        self.size       : int = size
        self.entry_point: int = entry_point
        self.__contents : [int] =  []
        for i in range(size+1):
            self.__contents.append(i*self.pid + 100)

    # -------------------------------------------------------------
    # print object
    # -------------------------------------------------------------
    def __str__(self):
        y = "Process: Pid: " + str(self.pid) + \
        " Max Addr: " + str(self.size - 1)
        return y

    def __repr__(self):
        return self.__str__()

    # -------------------------------------------------------------
    # get contents
    # -------------------------------------------------------------
    def get_data(self, vaddr:int) -> int:
        if vaddr <= self.size and vaddr > -1:
            return self.__contents[vaddr]
        else:
            msg = f"PROCESS: get_data: invalid address: {vaddr}"
            raise ValueError(msg)
        return

    # -------------------------------------------------------------
    # load_content
    # -------------------------------------------------------------
    def set_data(self,start_vaddr : int ,data : [int]) :
        for vaddr in range(start_vaddr,start_vaddr+len(data)):
            if vaddr < self.size and vaddr > -1:
                self.__contents[vaddr] = data[vaddr-start_vaddr]
            else:
                msg=f"PROCESS: set_data: invalid address {vaddr}"
                raise ValueError(msg)
            return

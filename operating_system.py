from multiprocessing.dummy import current_process
from urllib.error import ContentTooShortError
import mmu
import ram
import process
import page_registers

# ===========================================================================
# Operating System Memory Management
# ===========================================================================
#
# InvalidAddress(Exception) - does nothing, but program will crash with
#                             an appropriate error
# NotImplemented(Exception) - Catches the error that a function was called
#                             that has not been written yet
# page_fault(self,vaddr) - called when the MMU accesses a page register that is set to None
# load_process(self,process) - a process is being loaded
#
#

class InvalidAddress(Exception):
    pass

class NotImplemented(Exception):
    pass

class OS:

    # -------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------
    def __init__(self, ram, page_registers):


        # ---------------------------------------------------------
        # put whatever other data you want need here
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # every OS must have access to the ram
        # ---------------------------------------------------------
        # to load data into ram...
        # 'self.ram.set_data( physical_address, value )'
        self.ram = ram

        # ---------------------------------------------------------
        # Divide the RAM into frames
        # ---------------------------------------------------------
        self.ram_frames = [None] * ((self.ram.max_addr+1) // page_registers.page_size)

        # ---------------------------------------------------------
        # every OS must have access to the page_registers
        # ---------------------------------------------------------
        # to set a specific frame number for a given page 
        # 'self.page_registers.set_frame_number(page_number,frame_number)'
        # to get the frame_number from the  page registers for a specific page
        # 'frame_number = self.page_registers.get_frame_number(page_number)'
        self.page_registers = page_registers

        # page size (or frame size)
        self.page_size = page_registers.page_size

        # ---------------------------------------------------------
        # total number of frames availabe to the RAM
        # ---------------------------------------------------------
        self.num_frames_in_ram = len(self.ram_frames)

        # ---------------------------------------------------------
        # which process is currently running
        # ---------------------------------------------------------
        self.current_process = None


    # -------------------------------------------------------------
    # os deals with invalid address complaint from mmu
    # you must load the appropriate data from the process into
    # the ram, and update page registers accordlingly
    # ... other information may also need to be saved
    # -------------------------------------------------------------



    #To handle the page fault, the code first checks for an empty frame in RAM where the page can be loaded. 
    # It then calculates the page number by dividing the given virtual address by the page size. 
    # The page number is then used to set the appropriate entry in the page register, 
    # that maps page numbers to frame numbers in RAM. 
    # The code then calculates the range of addresses that belong to the page,
    #  retrieves the frame number from the page register, 
    # and iterates over the range of addresses, 
    # loading the contents of each address into the appropriate location in RAM. 
    # Finally, the code stores the loaded page in the RAM frame table.
    def page_fault(self, vaddr):
        # Check if the virtual address is valid
        if vaddr > self.current_process.size:
            raise InvalidAddress()


        # NEEDS TO BE IMPROVED TO PASS 80%, VALIDATE ADDRESS?? ABOVE IF STATEMENT DOESNT PASS TEST
        next_free_frame=0
        for frame_index in range(self.num_frames_in_ram):
            if self.ram_frames[frame_index] is None:
                next_free_frame=frame_index
                self.ram_frames[frame_index] = 0
                break

        # Calculate the page number
        page_number = vaddr // self.page_registers.page_size

        self.page_registers.set_frame_number(page_number,frame_index)

        # Calculate the start and end of the page
        page_start = page_number * self.page_registers.page_size
        page_end = page_start+self.page_registers.page_size

        # Set the page register
        self.page_registers.set_frame_number(page_number, frame_index)

        # Get frame number from page register function and store it
        frame_number = self.page_registers.get_frame_number(page_number)

        # Store the data in the RAM
        for virtual_address in range(page_start,page_end):
            # Calculate the offset within the page
            offset = virtual_address % self.page_registers.page_size
            # Calculate the actual physical address
            physical_address = next_free_frame*self.page_size + offset
            # Get the data at the virtual address and set it
            contents = self.current_process.get_data(virtual_address)
            self.ram.set_data(physical_address, contents)
            self.ram_frames[frame_number] = contents

    # -------------------------------------------------------------
    # new processes is loaded
    # NOTE: each process has the properties:
    #   pid -> uniquely identify each process (integer)
    #   entry_point -> which address is the location of the first
    #                  line of code
    #   size -> the size of the process
    # -------------------------------------------------------------
    def load_process(self, process):
        #Assign all process properties to self
        self.current_process = process
        self.pid = process.pid
        self.entry_point = process.entry_point
        self.size = process.size

        #set page registers to none
        self.page_registers.reset_all_registers_to_None()

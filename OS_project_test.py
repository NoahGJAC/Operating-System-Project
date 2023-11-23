# ==================================================================
# Asgt 6 INSTRUCTIONS:
# ==================================================================
# purpose: to complete the OS code to manage memory via 'demand paging'
#
# your job: modify the operating system code to complete the job
#           Do NOT modify any of the other files (except for maybe debug statements)
#
#
# rules:   1. The OS loads frame into RAM only when necessary,
#             - to know when a page needs to be loaded, the mmu will trigger a page_fault
#          2. When a page_fault is triggered, your code loads the required process page
#             into FIRST available RAM frame
#             - if no free RAM frame, then the first frame in RAM memory that does NOT
#               belong to the current process will be removed
#
# starter code:
#          process.py
#             properties:
#               pid             - the process id
#               size            - the size of the process
#               entry_point     - the location of the 1st command to execute
#             methods
#               get_data( vaddr:int) -> int
#               set_data( start_vaddr : int ,data : [int]) -> None
#
#          ram.py
#             properties:
#               max_addr        - maximum allowable address
#             methods
#               get_data( paddr : int ) -> int
#               set_data( paddr : int , data : int ) -> None
#
#          page_registers.py
#             properties
#               max_pages       - maximum number of pages
#               page_size       - the size of page (same as mmu.FRAME_SIZE)
#             methods
#               set_frame_number( :int , frame_num:int) -> None
#               get_frame_number ( page_num : int ) ->int
#               list_of_values() -> [int] # list[page] = frame
#               reset_all_registers_to_None() -> None
#
#          mmu.py (class MMU)
#             properties:
#               ram             - a RAM object
#               page_registers  - a Page_Registers object
#               FRAME_SIZE      - the size of each frame
#               page_fault_cb   - a function to call if there is a page fault
#             methods:
#               get_data( vaddr : int ) -> int :
#
#         operating_system.py - Student must update some of this code
#           properites
#             ram                   - a RAM object
#             page_registers        - a Page_Registers object
#             PAGE_SIZE             - size of pages
#             num_frames_in_ram     - number of frames available in RAM
#             frames                - a list for student to do whatever they want
#             current_process       - either None, or a process object
#           methods:
#             page_fault(vaddr:int) # a page fault has happened, do something
#             load_process(process ) # inputs: a process object

#
# To run your code:
#          python3 asg6_code.py
#
# MARKING:
#
# Pass these tests to get 40 %
#  load process and handle page faults, page registers set correctly
#
# Pass these tests to get 50%
#  handle page faults, page registers set correctly
#
# Pass these tests to get 70%
#  load another process, resetting of page registers
#  handle page faults, page registers set correctly
#
# Pass these tests to get 80%
# handle invalid addresses correctly
#
# Pass these tests to get 90%
#  Reload process 1 (no test)
#      ... page registers need to be restored from before
#     handle page faults, page registers set correctly
#
#  (-) Reload process 2 (no test)
#      ... page registers need to be restored from before
#     handle page faults, page registers set correctly
#
# Pass these tests to get 100%
#  (-) Load process 3 (no test)
#      ... there is no more space in RAM, so now page_fault code
#          needs to remove first page in RAM that is NOT used by Process 3
#     handle page faults, page registers set correctly
#
#  (-) Reload process 1 (no test)
#      ... there is no more space in RAM, so now page_fault code
#          needs to remove first page in RAM that is NOT used by Process 1
#      ... and page registers need to be adjusted for the process whose page has been removed
#     handle page faults, page registers set correctly
#
# Coding Standards (Could lose up to 20% of mark if not good)
#      - good comments (describe the PURPOSE of the code, not just
#                       what it is doing)
#      - break things down into separate functions as necessary
#      - good variable names
#      - no magic numbers, etc.
#      - other things.
# ===========================================================================

import sys,traceback
import mmu
import operating_system
import ram
import process
import page_registers as pr

FRAME_SIZE = 1024
PAGE_SIZE = FRAME_SIZE
MAX_PROCESS_SIZE = 200*FRAME_SIZE

# ===========================================================================
# make our computer
# ===========================================================================
ram = ram.RAM()
p_reg = pr.Page_Registers(MAX_PROCESS_SIZE, FRAME_SIZE)
os = operating_system.OS(ram, p_reg)
mmu = mmu.MMU(ram, p_reg, PAGE_SIZE, os.page_fault)

# ===========================================================================
# run tests
# ===========================================================================
mark25 = True
mark40 = True
mark50 = True
mark70 = True
mark80 = True
mark90 = True
mark100 = True
current_process = None

##### NOTE:  it is easy enough to make these tests pass without actually
#####        using paging.  You will not get marks if that is the case

test_number = None
def run_tests():
    global current_process
    frame_num = 0
    process1_entry_frame_num = None
    global test_number
    test_number = 0
    print("\n\n")

    # ===========================================================================
    # ... load process frame containing entry entry_point
    #          get the page registry set properly
    #          able to read content from ram
    # ===========================================================================
    if mark40:
        vaddr = 1027
        print ("\n","="*60)
        print("Pass these tests to get 40 %")
        print("="*60)

        # load process
        print(" (-) Load process 1 (no test) ")
        p1 = process.Process(entry_point=vaddr,size=712000)
        current_process = p1
        process1_entry_frame_num = frame_num
        load_process(p1)

        print(f" (1) MMU retrieves content of RAM at virtual address {vaddr} ")
        test_get_value(p1,vaddr)  # this should be in frame 0

        print(f" (2) page register {vaddr//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr//FRAME_SIZE,frame_num)

        frame_num = frame_num+1
        print ("\nYou have acheived 40% if you did not hard code results")

    # ===========================================================================
    # ... load additional frames into memory,
    #     update the page registry as required
    #     able to read content from ram
    # ===========================================================================
    if mark50:
        vaddr1 = 70000
        vaddr2 = 25000
        print("\n","="*60)
        print ("Pass these tests to get 50%")
        print("="*60)

        print(f" (3) MMU retrieves content of RAM at virtual address {vaddr1} ")
        test_get_value(p1,vaddr1)  # frame 68 should be loaded into page 1

        print(f" (4) page register {vaddr1//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr1//FRAME_SIZE,frame_num)

        print(f" (5) MMU retrieves content of RAM at virtual address {vaddr2} ")
        frame_num = frame_num+1
        test_get_value(p1,vaddr2)  # frame 24 should be loaded into page 2

        print(f" (6) page register {vaddr2//FRAME_SIZE} should contain {frame_num+1}")
        test_page_register(vaddr2//FRAME_SIZE,frame_num)

        frame_num = frame_num+1
        print ("\nYou have acheived 50% if you did not hard code results")
        print("="*60)

    # ===========================================================================
    # ... new process, new frames loaded
    # ===========================================================================
    if mark70:
        vaddr3 = 2056
        vaddr2 = 1056
        vaddr4 = 3080
        vaddr5 = 3085
        vaddr6 = 4180
        print("\n","="*60)
        print ("Pass these tests to get 70%")
        print("="*60)

        # need to reset page numbers when new process is loaded
        print(" (-) Load process 2 (no test) ")
        p2 = process.Process(entry_point=2056,size=6000)
        current_process = p2
        load_process(p2)

        print(f" (7) Page registers are reset after loading new process ")
        test_page_register(vaddr//FRAME_SIZE,None)

        print(f" (8) MMU retrieves content of RAM at virtual address {vaddr3} ")
        test_get_value(p2,vaddr3) # needs to be loaded into next page, which is page 3

        print(f" (9) page register {vaddr3//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr3//FRAME_SIZE,frame_num)
        process2_entry_frame_num = frame_num

        print(f"(10) MMU retrieves content of RAM at virtual address {vaddr2} ")
        frame_num = frame_num+1
        test_get_value(p2,vaddr2) # needs to be loaded into next page

        print(f"(11) page register {vaddr2//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr2//FRAME_SIZE,frame_num)

        print(f"(12) MMU retrieves content of RAM at virtual address {vaddr4} ")
        frame_num = frame_num+1
        test_get_value(p2,vaddr4) # needs to be loaded into next page

        print(f"(13) page register {vaddr4//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr4//FRAME_SIZE,frame_num)

        print(f"(14) MMU retrieves content of RAM at virtual address {vaddr5} ")
        test_get_value(p2,vaddr5) # do NOT create a new page

        print(f"(15) page register {vaddr5//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr5//FRAME_SIZE,frame_num)

        print(f"(16) MMU retrieves content of RAM at virtual address {vaddr6} ")
        frame_num = frame_num+1
        test_get_value(p2,vaddr6) # needs to be loaded into next page

        print(f"(17) page register {vaddr6//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr6//FRAME_SIZE,frame_num)

        frame_num = frame_num+1

        print ("\nYou have acheived 70% if you did not hard code results")
        print("="*60)

    # ===========================================================================
    # ... respect the limits of the process
    #     NOTE: processes don't necessarily end on frame boundaries
    #     mmu return a value of None if address is invalid for this process
    # ===========================================================================
    if mark80:
        vaddr7 = 5999
        vaddr8 = 7200
        print("\n","="*60)
        print ("Pass these tests to get 80%")
        print("="*60)

        print(f"(18) MMU retrieves content of RAM at virtual address {vaddr7} ")
        test_get_value(p2,vaddr7) # have to load last frame of process into RAM

        print(f"(19) page register {vaddr7//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr7//FRAME_SIZE,frame_num)
        frame_num = frame_num+1

        print(f"(20) an 'InvalidAddress' exception must be raised for vaddr {vaddr8}")
        print(f"     ... this is handled by the operating_system page_fault function")
        print("\nNeed to load process frame into memory,",\
        "without exceeding last address of process")

        print(f"\nOS raises InvalidAddress Exception for invalid address {vaddr8}")
        try:
            value = mmu.get_data(vaddr8)
            print_test(False,f"Invalid Address not raised, returned {value}")
        except operating_system.InvalidAddress:
            print_test(True,"Invalid Address raised")

        print ("\nYou have acheived 80% if you did not hard code results")

    # ===========================================================================
    # ... reloading processes, pages that are loaded should not be reloaded
    # ===========================================================================
    if mark90:
        vaddr10 = 0
        vaddr11 = 7000
        print("\n","="*60)
        print ("Pass these tests to get 90%")
        print("="*60)
        print(f"\nReload process {p1}")
        print ("     ... page registers need to be restored from before")
        load_process(p1)
        current_process = p1

        print(f"(21) MMU retrieves content of RAM at virtual address {p1.entry_point} ")
        test_get_value(p1,p1.entry_point)  # this should be in page 0

        print(f"(22) page register {p1.entry_point//FRAME_SIZE} should contain {process1_entry_frame_num}")
        test_page_register(p1.entry_point//FRAME_SIZE,process1_entry_frame_num)

        print(f"(23) MMU retrieves content of RAM at virtual address {vaddr10} ")
        test_get_value(p1,vaddr10)

        print(f"(24) page register {vaddr10//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr10, frame_num)
        frame_num = frame_num+1

        print(f"(25) MMU retrieves content of RAM at virtual address {vaddr11} ")
        test_get_value(p1,vaddr11)

        print(f"(26) page register {vaddr11//FRAME_SIZE} should contain {frame_num}")
        test_page_register(vaddr11//FRAME_SIZE, frame_num)
        frame_num = frame_num+1

        print("")
        print(f"\nReload process {p2}")
        print ("     ... page registers need to be restored from before")
        load_process(p2)
        current_process = p2

        print(p_reg)

        print(f"(27) MMU retrieves content of RAM at virtual address {p2.entry_point} ")
        test_get_value(p2,p2.entry_point)

        print(f"(28) page register {p2.entry_point//FRAME_SIZE} should contain {process2_entry_frame_num}")
        test_page_register(p2.entry_point//FRAME_SIZE,process2_entry_frame_num)

        print ("\nYou have acheived 95% if you did not hard code results")
        print("="*60)

    # ===========================================================================
    if mark100: # swapping processes out of memory
    # ===========================================================================
        vaddr20 = 2056
        vaddr21 = 4056
        vaddr22 = 25000
        vaddr23 = 70000

        print("\n","="*60)
        print ("Pass these tests to get 100%")
        print("="*60)


        p3 = process.Process(entry_point=2056,size=60000)
        print(f"\nLoad new process {p3}")
        print ("     ... there is no more space in RAM, so now page_fault code ")
        print ("         needs to remove first page in RAM that is NOT used by Process 3 ")
        load_process(p3)
        current_process = p3

        print(f"(29) MMU retrieves content of RAM at virtual address {vaddr20} ")
        test_get_value(p3,vaddr20)  # this should be in page 0

        print(f"(30) page register {vaddr20//FRAME_SIZE} should contain 0")
        test_page_register(vaddr20//FRAME_SIZE,0)

        print(f"(31) MMU retrieves content of RAM at virtual address {vaddr21} ")
        test_get_value(p3,vaddr21)  # this should be in page 1

        print(f"(32) page register {vaddr21//FRAME_SIZE} should contain 1")
        test_page_register(vaddr21//FRAME_SIZE,1)

        print()
        print(f"\nreload process {p1}")
        print ("     ... there is no more space in RAM, so now page_fault code ")
        print ("         needs to remove first page in RAM that is NOT used by Process 3 ")
        print ("     ... and page registers need to be adjusted for the process whose page has been removed")
        load_process(p1)
        current_process = p1


        print(f"(33) MMU retrieves content of RAM at virtual address {vaddr22} ")
        test_get_value(p1,vaddr22)  # this is still in page 2

        print(f"(34) page register {vaddr22//FRAME_SIZE} should contain 2")
        test_page_register(vaddr22//FRAME_SIZE,2)

        print(f"(35) MMU retrieves content of RAM at virtual address {vaddr23} ")
        test_get_value(p1,vaddr23)  # loads into page 0

        print(f"(36) page register {vaddr23//FRAME_SIZE} should contain 0")
        test_page_register(vaddr23//FRAME_SIZE,0)

        print ("\nYou have acheived 100% if you did not hard code results")
        print("="*60)





# ===========================================================================
# print_test
# ===========================================================================
def print_test(result,msg):
    global test_number
    test_number = test_number + 1
    test_str = str(test_number).rjust(2)
    if result:
        print(f"ok ({test_str})\t",msg,"\n\n")
    else:
        print(f"\n*** NOK ({test_str})\t",msg)
        print("\n\n Fix above error before proceeding to next test")
        quit()

# ===========================================================================
# test_get_value
# ===========================================================================
def test_get_value(p,vaddr):
    try:
        value = mmu.get_data(vaddr)
        print (f"\n\tCurrent Process {current_process}\n",p_reg)

        t = f"Get a value using mmu from virtual address {vaddr}"+\
        f",\n\t Correct answer: {p.get_data(vaddr)}, you got: {value}"
        print_test( value is not None and p.get_data(vaddr) == value,t)
    except Exception:
        e_type, e_value, e_traceback = sys.exc_info()
        info = f'''
            Get a value using mmu from virtual address {vaddr}
            an exception {e_type} occurred
        '''
        e_output = traceback.format_exception(e_type, e_value,e_traceback)
        print_test(False,info+"\n\n"+"\n".join(e_output))


# ===========================================================================
def test_page_register(page_number,frame_number):
# ===========================================================================
    frame = p_reg.get_frame_number(page_number)
    if frame_number is None:
        t = f"Page {page_number} should not be set in page register.\n\t Correct answer: {frame_number}, you got: {frame}"
    else:
        t = f"Page {page_number} is in which frame?\n\t Correct answer: {frame_number}, you got: {frame}"
    print_test(frame == frame_number,t)

# ===========================================================================
def load_process(p):
# ===========================================================================
    try:
        print(f"\n===> loading process {p.pid}")
        os.load_process(p)
    except Exception:
        e_type, e_value, e_traceback = sys.exc_info()
        info = f'Trying to load process {p.pid}. An exception {e_type} occurred'
        e_output = traceback.format_exception(e_type, e_value,e_traceback)
        print_test(False,info+"\n\n"+"\n".join(e_output))


run_tests()

# ===========================================================================
# MMU - gets and stores data to RAM, using virtual address
#     - if virtual address cannot be properly converted to a
#       physical address, then call the callback function "page_fault_cb"
#
# --- get_data(self, vaddr)
# --- set_data(self, vaddr, data)
# ===========================================================================

# STUDENT TODO: Nothing... its all done, just use the code as is
import ram
import page_registers as pr
class MMU:
    # -------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------
    def __init__(self,ram:ram.RAM, page_registers: pr.Page_Registers, \
                frame_size: int, page_fault_cb: callable):
        ''' constructor '''
        self.ram : ram.RAM = ram
        self.page_registers :pr.Page_Registers= page_registers
        self.frame_size : int = frame_size
        self.page_fault_cb : int = page_fault_cb

    # -------------------------------------------------------------
    # get physical address from virtual address
    # -------------------------------------------------------------
    def _get_physical_address_from_virtual(self, vaddr : int)->(int) :
        page_number :int  = vaddr // self.frame_size
        offset      :int  = vaddr - page_number * self.frame_size
        frame_number:int  = self.page_registers.get_frame_number(page_number)

        # if address is invalid, we have to ask OS to load
        # required page, and try again
        if frame_number is None:
            self.page_fault_cb(vaddr)
            frame_number = self.page_registers.get_frame_number(page_number)

        # return the physical address
        return frame_number*self.frame_size + offset

    # -------------------------------------------------------------
    # get data from ram, using virtual address, single word
    # -------------------------------------------------------------
    def get_data(self, vaddr : int ) -> int :
        paddr = self._get_physical_address_from_virtual(vaddr)
        return self.ram.get_data(paddr)

    # -------------------------------------------------------------
    # set data in ram, using virtual address, single byte
    # -------------------------------------------------------------
    def set_data(self, vaddr: int, data: [int]) -> None:
        pass

# ===========================================================================
# Page Registers:
# --- set_frame_number(self, page_num, frame_num)
# --- get_frame_number(self, page_num)
# --- list_of_values()
# --- reset_all_registers_to_None()
# ===========================================================================

# STUDENT TODO: Nothing... its all done, just use the code as is

class Page_Registers:

    def __init__(self, max_process_size :int , page_size:int):
        self.max_pages = max_process_size // page_size
        self.__frame_numbers = [None] * self.max_pages
        self.page_size = page_size

    # -------------------------------------------------------------
    # set page register for specified page number to specified frame number
    # -------------------------------------------------------------
    def set_frame_number(self, page_num:int , frame_num:int) -> None :

        # if page number valid, then set frame register accordingly
        if page_num < self.max_pages and page_num > -1:
            self.__frame_numbers[page_num] = frame_num
        else:
            raise ValueError(f"PAGE_REGISTER: page_num: {page_num}: set_frame_number invalid")

    # -------------------------------------------------------------
    # get frame number for specified page number
    # -------------------------------------------------------------
    def get_frame_number (self, page_num : int ) ->int :
        if page_num < self.max_pages and page_num > -1:
            return self.__frame_numbers[page_num]
        else:
            raise ValueError(f"PAGE_REGISTER: {page_num}: get_frame_number invalid")
        return

    # -------------------------------------------------------------
    # return list of all page_register values
    # -------------------------------------------------------------
    def list_of_values(self) -> [int]:
        return self.__frame_numbers

    # -------------------------------------------------------------
    # resets all registers to None
    # -------------------------------------------------------------
    def reset_all_registers_to_None(self) -> None :
        self.__frame_numbers = [None] * self.max_pages


    # -------------------------------------------------------------
    # print object
    # -------------------------------------------------------------
    def __str__(self):

        # get a list of pages/frames, do NOT include unused pages/frames
        page_frame = []
        for page_number in range(self.max_pages):
            frame_number = self.__frame_numbers[page_number]
            if frame_number is not None:
                page_frame.append ([page_number, frame_number])

        # for frame_to_page, sort by frame number
        frame_to_page = sorted(page_frame,  key=lambda a: a[1])

        # store stuff to print in variable 'y'
        y = "\t----------------------------------------\n"
        y = y+ "\t|Page -> Frame    |  Frame # -> Page # |"
        for i in range(len(page_frame)):
            page_number = str(page_frame[i][0]).rjust(4)
            frame_number = str(page_frame[i][1]).rjust(4)
            y = y + f"\n\t|{page_number} -> {frame_number}     |"
            page_number = str(frame_to_page[i][0]).rjust(4)
            frame_number = str(frame_to_page[i][1]).rjust(4)
            y = y + f"  {frame_number} -> {page_number}      |"

        y = y+ "\n\t----------------------------------------"
        return y

    def __repr__(self):
        return self.__str__()

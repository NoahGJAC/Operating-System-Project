class RAM:
    # -------------------------------------------------------------
    # static class variables & methods
    # -------------------------------------------------------------
    __MAX_RAM = 10240

    # -------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------
    def __init__(self):
        self.__contents =  []
        for _ in range(RAM.__MAX_RAM):
            self.__contents.append(None)
        self.max_addr = RAM.__MAX_RAM - 1

    # -------------------------------------------------------------
    # get contents
    # -------------------------------------------------------------
    def get_data(self, paddr : int ) -> int :
        if paddr <= self.max_addr and paddr > -1:
            return self.__contents[paddr]
        else:
            raise ValueError(f"RAM: get_data: {paddr}: invalid address")
        return

    # -------------------------------------------------------------
    # load_content
    # -------------------------------------------------------------
    def set_data(self,paddr : int , data : int ) -> None:
        if paddr <= self.max_addr and paddr > -1:
            self.__contents[paddr] = data
        else:
            raise ValueError(f"RAM: set_data: {paddr}: invalid address")
        return

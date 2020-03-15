

class Score():
    def __init__(self):
        self.__fruity_count = 0
        self.__bitter_count = 0
        self.__rotten_count = 0

    def get_fruity(self):
        return self.__fruity_count

    def get_bitter(self):
        return self.__bitter_count

    def get_rotten(self):
        return self.__rotten_count

    def compute_score(self, chips_list):
        for chip in chips_list:
            if chip is not None:
                self.__fruity_count += chip.get_fruity()
                self.__fruity_count = round(self.__fruity_count, 1)
                self.__bitter_count += chip.get_bitter()
                self.__bitter_count = round(self.__bitter_count, 1)
                self.__rotten_count += chip.get_rotten()
                self.__rotten_count = round(self.__rotten_count, 1)

    def clear_score(self):
        self.__fruity_count = 0
        self.__bitter_count = 0
        self.__rotten_count = 0

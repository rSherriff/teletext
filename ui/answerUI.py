from ui.ui import UI
from ui.ui import CheckedInput

from actions.actions import AnswerCorrect

class AnswersUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        idim = [3,4,16,1] #Input dimensions
        input_one = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Richard Holmes', completion_action=AnswerCorrect(self.section.engine, 1))
        self.add_element(input_one)

        idim = [3,6,16,1]
        input_two = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Judy Langsford', completion_action=AnswerCorrect(self.section.engine, 2))
        self.add_element(input_two)

        idim = [3,12,16,1]
        input_three = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Robert Dolan', completion_action=AnswerCorrect(self.section.engine, 3))
        self.add_element(input_three)

        idim = [3,18,16,1]
        input_four = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Cat Grant', completion_action=AnswerCorrect(self.section.engine, 4))
        self.add_element(input_four)

        idim = [3,24,16,1]
        input_five = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Angelica Osman', completion_action=AnswerCorrect(self.section.engine, 5))
        self.add_element(input_five)

        idim = [3,29,16,1]
        input_six = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Steven Kielty', completion_action=AnswerCorrect(self.section.engine, 6))
        self.add_element(input_six)            

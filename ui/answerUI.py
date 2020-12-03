from ui.ui import UI
from ui.ui import CheckedInput, HoverTrigger

from actions.actions import AnswerCorrect, ShowTooltip, HideTooltip
from effects.horizontal_wipe_effect import HorizontalWipeEffect, HorizontalWipeDirection

class AnswersUI(UI):
    def __init__(self, section, x, y, tiles, correct_colour):
        super().__init__(section, x, y)
        self.elements = list()
        self.correct_colour = correct_colour

        #Idol Academy
        idim = [25,4,16,1]
        effect = HorizontalWipeEffect(self.section.engine, x=idim[0], y=idim[1] + 24, width=idim[2], height=idim[3])
        input_three = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Judy Langsford', trigger_once = True, completion_action=AnswerCorrect(self.section.engine, 'q2'), completion_colour=self.correct_colour, completion_effect=effect)
        self.add_element(input_three)

        idim = [25,6,16,1]
        effect = HorizontalWipeEffect(self.section.engine, x=idim[0], y=idim[1] + 24, width=idim[2], height=idim[3])
        input_four = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Richard Holmes', trigger_once = True, completion_action=AnswerCorrect(self.section.engine, 'q1'), completion_colour=self.correct_colour, completion_effect=effect)
        self.add_element(input_four)

        hdim = [23,2,12,1]
        hover_one = HoverTrigger(x=hdim[0], y=hdim[1], width=hdim[2], height=hdim[3], mouse_enter_action=ShowTooltip(self.section.engine, 'q1'), mouse_leave_action=HideTooltip(self.section.engine, 'q1'))
        self.add_element(hover_one)

        #Cops With Cameras
        idim = [3,4,16,1]
        effect = HorizontalWipeEffect(self.section.engine, x=idim[0], y=idim[1] + 24, width=idim[2], height=idim[3])
        input_one = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Robert Dolan', trigger_once = True, completion_action=AnswerCorrect(self.section.engine, 'q3'), completion_colour=self.correct_colour, completion_effect=effect)
        self.add_element(input_one)

        hdim = [1,2,17,1]   
        hover_one = HoverTrigger(x=hdim[0], y=hdim[1], width=hdim[2], height=hdim[3], mouse_enter_action=ShowTooltip(self.section.engine, 'q2'), mouse_leave_action=HideTooltip(self.section.engine, 'q2'))
        self.add_element(hover_one)

        #Ghost Hunters
        idim = [3,9,16,1]
        effect = HorizontalWipeEffect(self.section.engine, x=idim[0], y=idim[1] + 24, width=idim[2], height=idim[3])
        input_two = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Cat Grant', trigger_once = True, completion_action=AnswerCorrect(self.section.engine, 'q4'), completion_colour=self.correct_colour, completion_effect=effect)
        self.add_element(input_two)

        hdim = [1,7,12,1]
        hover_one = HoverTrigger(x=hdim[0], y=hdim[1], width=hdim[2], height=hdim[3], mouse_enter_action=ShowTooltip(self.section.engine, 'q3'), mouse_leave_action=HideTooltip(self.section.engine, 'q3'))
        self.add_element(hover_one)


        #Grimebusters
        idim = [47,4,16,1]
        effect = HorizontalWipeEffect(self.section.engine, x=idim[0], y=idim[1]+ 24, width=idim[2], height=idim[3])
        input_five = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Angelica Osman', trigger_once = True, completion_action=AnswerCorrect(self.section.engine, 'q5'), completion_colour=self.correct_colour, completion_effect=effect)
        self.add_element(input_five)

        hdim =  [45,2,12,1]
        hover_one = HoverTrigger(x=hdim[0], y=hdim[1], width=hdim[2], height=hdim[3], mouse_enter_action=ShowTooltip(self.section.engine, 'q4'), mouse_leave_action=HideTooltip(self.section.engine, 'q4'))
        self.add_element(hover_one)

        #Stop the presses
        idim = [47,9,16,1]
        effect = HorizontalWipeEffect(self.section.engine, x=idim[0], y=idim[1]+ 24, width=idim[2], height=idim[3])
        input_six = CheckedInput(x=idim[0], y=idim[1], width=idim[2], height=idim[3], check_string='Steven Kielty', trigger_once = True, completion_action=AnswerCorrect(self.section.engine, 'q6'), completion_colour=self.correct_colour, completion_effect=effect)
        self.add_element(input_six)     

        hdim = [45,7,16,1]
        hover_one = HoverTrigger(x=hdim[0], y=hdim[1], width=hdim[2], height=hdim[3], mouse_enter_action=ShowTooltip(self.section.engine, 'q5'), mouse_leave_action=HideTooltip(self.section.engine, 'q5'))
        self.add_element(hover_one)

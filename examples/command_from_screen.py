from OCR_Text_Commands.ocr_text_commands import TextCommand

#create a TextCommand object, specifying the computer screen as the image source
#and setting the model confidence threshold to 0.7
comms = TextCommand(camera_type = 'screen', threshold=0.7)

#start screen capture and keyword detection/recognition
comms.command_capture()





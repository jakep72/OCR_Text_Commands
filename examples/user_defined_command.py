from OCR_Text_Commands.ocr_text_commands import TextCommand
import webbrowser

#create a TextCommand object
comms = TextCommand(camera_type='web')

#define a simple custom function to open the spotify home page
def open_spotify():
    webbrowser.open('www.spotify.com/us/')

#start capturing webcam frames and monitoring for keywords.  Set the keyword 'spot' to look for in order to call
#open_spotify command    
comms.command_capture(user_keyword='spot',user_func=open_spotify)


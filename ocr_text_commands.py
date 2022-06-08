import cv2
import easyocr
import webbrowser
from PIL.ImageGrab import grab
import numpy as np

class TextCommand:
    
    def __init__(self,
                 camera_type = 'web',
                 threshold = 0.2,
                 x = 200,
                 y = 200,
                 width = 700,
                 height = 700, 
                 language = 'en',
                 decoder = 'greedy',
                 beamWidth = 5,
                 batch_size = 1,
                 workers = 0,
                 ip_user = None,
                 ip_pass = None,
                 ip_address = None
                 ):
        
        """Create a TextCommand object
        
        Description:
        ------------
        OCR_Text_Commands is a fun little tool built on top of easyocr (https://github.com/JaidedAI/EasyOCR) and opencv that
        allows you to send commands to your computer based on keywords written on a blank piece of paper (preferably using a sharpie on white paper).
        The current set of commands are very simple, but could be expanded to be a bit more complex.  Ultimately, there is
        probably little utility in further development.  Note that performance will be questionable without access to a GPU.
        
        Parameters:
        -----------
        camera_type : str
           Source frames/images to look for text in. Built in computer webcam ('web'), ip camera ('ip'), or computer screen ('screen'). 
           Only webcam and computer screen are supported for now. 

        threshold : float
            minimum model confidence level for the keyword. If the first word detected is above the threshold value, the command will be executed.

        x : int
            upper left x coordinate of the bounding box when 'screen' is specified as the image source.

        y : int
            upper left y coordinate of the bounding box when 'screen' is specified as the image source.

        width : int
            lower right x coordinate of the bounding box when 'screen' is specified as the image source.

        height : int
            lower right y coordinate of the bounding box when 'screen' is specified as the image source.
        
        -----------------------------------------------------------------------------------------------------------
        For all easyocr parameters, more documentation can be found at https://www.jaided.ai/easyocr/documentation/
        -----------------------------------------------------------------------------------------------------------
        
        language : str 
            easyocr reader class parameter.  English by default and only language supported for now.
        
        decoder : str
            easyocr readtext method parameter
        
        beamWidth : int
            easyocr readtext method parameter.
        
        batch_size : int
            easyocr readtext method parameter.
        
        workers : int
            easyocr readtext method parameter.
                                          
        ip_user : str
            username for ip camera
        
        ip_pass : str
            password for ip camera
        
        ip_address : str
            IP address of ip camera

        """
        
        self.reader = easyocr.Reader([language])
        self.decoder = decoder
        self.beamWidth = beamWidth
        self.batch_size = batch_size
        self.workers = workers
        self.threshold = threshold
        self.camera_type = camera_type
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        
        # Initialize a videocapture object to access user's built in webcam
        if camera_type == 'web':
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Untested feature -- accessing an IP camera via RTSP
        elif camera_type == 'ip':
            conn_string = "rtsp://"+ip_user+":"+ip_pass+"@"+ip_address
            self.cap = cv2.VideoCapture(conn_string)
            
    def __snap_command(self,frame):
        """
        Parameters
        ----------
        frame : array
            Draw text on the frame to notify user a snapshot has been taken.

        Saves a .jpg image of the current frame when the snap keyword is detected

        """
        cv2.imwrite('snapshot.jpg',frame)
        cv2.putText(frame,"Picture Saved Successfully!",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),2)

        
    def __search_command(self):
        """
        opens a new google search tab in default web browser 

        """
        webbrowser.open('www.google.com')
        
    def __mail_command(self):
        """
        opens gmail login page

        """
        webbrowser.open('www.google.com/mail')
        
    def __notes_command(self,frame,result):
        """
        Parameters
        ----------
        frame : array
            
        result : list, output of easyocr readtext method

        if notes keyword is detected, saves subsequent words to a text file 
        and draws bounding boxes as well as identified words on the frame

        """
        with open('notes.txt','w') as f:
            for i in range(len(result)-1):
                cv2.rectangle(frame, (int(result[i+1][0][0][0]),int(result[i+1][0][0][1])), (int(result[i+1][0][2][0]),int(result[i+1][0][2][1])), (255,0,0), 2)
                cv2.putText(frame,result[i+1][1],((int(result[i+1][0][0][0])-50),(int(result[i+1][0][0][1])-50)),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),2)
                f.write(result[i+1][1].lower()+" ")
    
    
    def command_capture(self, user_keyword = None, user_func = None, break_after = True):
        """
        Parameters
        ----------
        user_keyword : str, optional
            user defined keyword to detect. The default is None.

        user_func : func, optional
            user defined command to execute if the user defined keyword is detected. The default is None.

        break_after : bool, optional
            If true, break the while loop after the user defined command is executed. The default is True.
                
        """
        
        #use counters to prevent multiple search and/or mail commands to be executed successively
        search_counter = 0
        mail_counter = 0
        
        while True:
            
            #use grab method from PIL to access user's screen if 'screen' is specified
            if self.camera_type == 'screen':
                frame_BGR = np.array(grab(bbox=(self.x, self.y, self.width, self.height)))
                
            #use read method from OpenCV to access user's webcam or an IP Camera
            elif self.camera_type == 'web' or self.camera_type == 'ip':
                ret,frame_BGR = self.cap.read()

            else:
                raise TypeError("camera type invalid or not defined!")
            
            #easyocr requries conversion to RGB, OpenCV and PIL read BGR by default
            frame_RGB = cv2.cvtColor(frame_BGR,cv2.COLOR_BGR2RGB)
            
            #call easyocr readtext method to detect and identify text in the frame
            result = self.reader.readtext(frame_RGB, decoder=self.decoder, beamWidth = self.beamWidth,
                                     batch_size = self.batch_size, workers = self.workers)

            #take no action if a word has not been detected or if the model confidence of the detected word does not meet the specified threshold
            if len(result) > 0 and result[0][2] > self.threshold:
                
                #define the keyword as the first word detected in the upper left corner of the frame
                #and convert all letters to lowercase
                keyword = result[0][1].lower()
                
                #draw a bounding box around the keyword and label the word on the frame so user knows what is being seen
                cv2.rectangle(frame_BGR, (int(result[0][0][0][0]),int(result[0][0][0][1])), (int(result[0][0][2][0]),int(result[0][0][2][1])), (255,0,0), 2)
                cv2.putText(frame_BGR,result[0][1],((int(result[0][0][0][0])-50),(int(result[0][0][0][1])-50)),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),2)

                if keyword == 'stop':
                    #break the loop if the first word seen is stop
                    break
                
                elif keyword == 'snap':
                    #save frame as jpg image if the first word seen is snap
                    self.__snap_command(frame_BGR)
                    search_counter = 0
                    mail_counter = 0
                    
                    
                elif keyword == 'search' and search_counter == 0:
                    #open google search if the first word seen is search
                    self.__search_command()
                    search_counter = 1
                    mail_counter = 0
                
                elif keyword == 'mail' and mail_counter == 0:
                    #open gmail if the first word seen is mail
                    self.__mail_command()
                    search_counter = 0
                    mail_counter = 1
                
                elif keyword == "notes":
                    #save notes to a text file if the first word seen is notes
                    self.__notes_command(frame_BGR, result)        
                    search_counter = 0
                    mail_counter = 0
                    
                elif keyword == user_keyword:
                    #call a user defined function if the first word seen matches the user defined keyword
                    user_func()
                    search_counter = 0
                    mail_counter = 0
                    if break_after == True:
                        break

            #manual killswitch in case things go wrong
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            #display the frame so the user can see what is going on
            cv2.imshow('Display',frame_BGR)
        
        #release frames if accessing webcam or ip camera
        if self.camera_type == 'web' or self.camera_type == 'ip':
            self.cap.release()

        cv2.destroyAllWindows()
            
        
        
    
        


# OCR_Text_Commands
OCR_Text_Commands is a fun little tool built on top of easyocr (https://github.com/JaidedAI/EasyOCR) and opencv that allows you to send commands to your computer based on keywords written on a blank piece of paper (preferably using a sharpie on white paper).         The current set of commands are very simple, but could be expanded to be a bit more complex.  Ultimately, there is probably little utility in further development.

# Installation Steps

Anaconda

conda create --name <your_env-name> python==3.7

pip install easyocr

pip uninstall opencv-python-headless

pip install opencv-python==4.5.4.60

cd to new env and git clone https://github.com/jakep72/OCR_Text_Commands.git

# Usage

Navigate to OCR_Text_Commands/examples and run:

python user_defined_command.py

If your webcam is enabled, a window will appear -- hold a piece of white paper with one of the keywords listed below written on it to take an action:

-MAIL:  open gmail in the default browser

-SEARCH:  open google search engine in default browser

-NOTES:  save a note to a text file in the current working directory

-STOP:  close the window and exit the program

-SNAP:  save the current frame to a .jpg file in the current working directory (example below)

Or define your own keyword and corresponding action in the example file.


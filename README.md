# DSP-Exterior-Door-Security-via---Microphone-Signal-Processing---Face-detectionF
Digital Signal Processing project called Exterior Door Security System. Real-time Speech Signal Processing and Video Processing are used for key-word detection and Face detection.

Today, smart home appliances are controlled using different user interfaces and based
on various input devices. In this project, an exterior door security system is implemented
by processing camera and microphone signals in real-time. Implemented program sequentially 
detects two different keywords. After detection of the keywords,
it starts processing the camera signal to detect the user’s face. When a human face
is detected, the program takes a photo of the user and saves it with the precise information
of the entrance time. Speech is a natural and easy way for communication
between humans and machines. However, smart device manufacturers use a limited
set of words to control them so that the system is more affordable and accessible for
potential customers. If a user says different words then the keyword system detection
does not happen so the program does not take any action as it should be. In addition to
the implementation of the voice command detection, a pretrained face detection model
is also added to the project to strengthen the demonstration of the project.

The program processes the real-time audio for keyword detection from voice to decide
whether the user is registered or not. Detection of the keywords are done by crosscorrelation calculations between on going real-time input and pre-recorded user voice.
Program also process the video in real-time, detects the user’s face and saves the photo
of the user with the date and time information after user’s face is detected and framed.
The main function only calls the scripts in the sequence of

1 − s e c u r i t y . py
2 − banana . py
3 − f a c e d e t e c t i o n . py

security.py python script is also a stand-alone project runs by clicking. When the
door bell rings main.py calls the script called security, the program prompts the sentence below:
’ I am l i s t e n i n g , c a l l my name when you a r e r e a d y ! ’

Then assistant starts listening the guest or the resident, and asks for its name to
start the human-machine communication. Here the assistans name is the first key-word
program looks for and the initial password at the door. When the user call its name
which is “Security” the program prints the sentences below and terminates itself.
’ S e c u r i t y : Hey There ! ’
’ S e c u r i t y : What i s t h e password ? ’
Then main.py calls the banana.py script which runs for detecting the second keyword. Program asks for the password and as soon as the user says “banana” script prints
the sentences below:
’ S e c u r i t y : C o r r e c t password banana i s d e t e c t e d ! ’
After detecting the second key-word(password) banana.py script terminates itself.
Lastly main.py calls the facedetection.py script. The last script looks for a human face.
After the human face is detected and framed, it saves the image in the png file format
with the entrance time information. At the end the program informs the user about
taken face photograph and welcomes the user then terminates itself.
’ Face i s d e t e c t e d , framed and saved wi th t h e d a t e ! ’
’ Welcome Home ! ’



Pre-recorded voice signals are neccessary. They are called by the program to compare them with the microphone inputs. Some of the files are parts of the
recorded words.

R e c o r d i n g s of t h e word ” banana ”
−b1 . wav , b2 . wav , b3 . wav , b4 . wav , b5 . wav , b6 . wav
R e c o r d i n g s of t h e word ” s e c u r i t y ”
−1. wav , 2 . wav , 3 . wav
Recording p a r t s of t h e word ” s e c u r i t y ”
−p1 . wav , p2 . wav , p3 . wav
−1 2 . wav , 2 3 . wav

For details read the file called 'dsp_project_report.pdf'.


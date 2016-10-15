Facelist

What is Facelist? 
Facelist is essentially a playlist creating photo-booth. 

Dependencies: OpenCV, Pillow, Tkinter, Numpy, Soundcloud, Indico

Run facelist.py

How does it work?
	Facelist works by analyzing the photographs you take using the built in webcam reader. 
	You start by opening the application.
Activate Camera
The application starts with s splash screen where the camera display should be, you initiate the camera by clicking on the button labeled Activate Camera located above the camera viewing window. 
Taking a Picture
	1. The webcam feed is now active and you are permitted to begin taking pictures. 
	2. You can take a picture by clicking on the button labeled Take Picture located below the camera viewing window
	3. The photos are saved into the directory holding the program. 
The Magic
	1. The magic happens in the back-end. The picture taken is then cropped to localize your face. 
	2. The cropped image is then sent to indico where their API analyzes the face for emotion and returns a dictionary of emotions (string) and the probability that the face is showing that emotion. 
	3. We then search for a song on soundcloud matching the emotion and add it to a list
Playing Song
	1. Press the button labeled Play to start the song.

GitHub

	You can review our progress at : https://github.com/nigelhardy/cst205-proj2-facelist
	There are multiple branches where progress and testing have taken place so be sure to explore it 	all. 

Future Work
	Web Cam Features:
		1. Allow user to choose or create a new directory for saving camera filesA
		2. Allow users to create their own file name templates
		3. Possibility of frames for the webcam viewer
		4. Photo-booth strip creation after taking 5-6 pictures.
	GUI Features
	1. Add more track information.
	2. Artist 
	3. Label
	4. Album 
	5. Number of Plays

	Polish the GUI layout and color scheme
	Possibility of changing layout of components
	Uniform color scheme
	GUI decoration

	Playlist Features
	1. Integrate the playing of songs into GUI
	2. Gstreamer
	3. PyAudio
	4. Player Controls
	5. Allow users to pause/play songs
	6. Allow users to control track selection
	7. Links to artist SoundCloud profile
	
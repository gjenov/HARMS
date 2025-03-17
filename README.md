# NOHARMS (Non Obtrusive Human Activity Recognition in Medical Settings)
## Welcome to NOHARMS
The main functionality of this report is covered in sections 1-3

## 1) Local Machine Annotations
- This section is used for creating a .xlsx file with all annotations from an uploaded video
	- This code is defined for use with the ICARE dataset
#### Instructions:
	Open OnScreenGuiAnnotation.ipynb
	(Optional) Run code cell 1 to install ultralytics
	Run cell 2 to define our drawing function
	In cell 3, **define** your video path, video start time in "00:00:00" format, output path and sheet path
	Finally, Run cell 4 to produce an annotated video (With GUI) and .xlsx annotated output

## 2) Server / Client
	Open server.ipynb, this will be your server
	Complete same instructions as before (running cell 4 will start server)
	Open client.ipynb
	Run server.ipynb, once running run client.ipynb

	This will open two cv2 windows to display realtime annotations and GUI
	(This server and client will run on localhost)

## 3) Dashboard
	This code is used to display a sample dashboard using dash by plotly.
	To run the dashboard simply run app.py and open "http://127.0.0.1:8050/" on a web browser

## 4) Posec3d
	This code was used to train and evaluate posec3d using mmaction2
 	1) Download MMaction2 toolbox
  	2) Download and open folder posec3d in repo
  	3) To MMAction 2 toolbox: 
   		- Upload the trained model weights (our .pth was too large to upload to github)
     		- Upload the labels (labels.txt)
       		- replace the config file in "\mmaction2\configs\skeleton\posec3d" with config file: (slowonly_r50_8xb32-u48-240e_k400-keypoint_.py)
	 	- Run

### Misc. (other scripts for dashboard mockup and accuracy evaluation)
	evaluate_yolo_buffer.py is used to assess the accuracy 
 	to run, change the inputs of the truth data and input data in csv and run evaluate_yolo_buffer.py

 	UpdatingDashBoard.ipynb was used for a dashboard mockup using ngrok and novu
  	requires novu and ngrok credentials in API key variables
### Future Work
	Next steps include 1) Integrating Server / Client to send live updates to Dashboard
	2) Optimizing annotations for use in realtime
 
 	

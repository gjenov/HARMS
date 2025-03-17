# NOHARMS (Non Obtrusive Human Activity Recognition in Medical Settings)
## Welcome to NOHARMS

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

## Misc.
	evaluate_yolo_buffer.py is used to assess the accuracy 
 	to run, change the inputs of the truth data and input data in csv and run evaluate_yolo_buffer.py

### Future Work
	Next steps include 1) Integrating Server / Client to send live updates to Dashboard
	2) Optimizing annotations for use in realtime

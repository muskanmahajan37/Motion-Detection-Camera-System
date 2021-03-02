# Motion-Detection-Camera-System
An advanced system of motion detection techniques along with multimedia techniques. 
This system will be more secure than any other of these techniques alone and also as 
compared to traditional video surveillance systems.

After some research, I came up with an algorithm which detected motion by comparing 
each frame captured by the camera with the previous one. If the frames were more or less the same, 
fine, but if they had differences above a certain limit, the program would trigger a motion detection event. 
So, for every frame captured, I compared the pixels with the previous frame for brightness changes. 
If the brightness change of a certain pixel exceeded a tolerance limit, the program would increment a counter. 
At the end of the scan, it checked the value of the counter and if it exceeded a certain limit, it triggered a motion detection event. 

So my idea was to take a picture from a webcam every period of time (make it the current picture) and compare it with a previous picture and if we find a big difference between them we will save both pictures else will free memory from the old picture and make the new picture the current picture.


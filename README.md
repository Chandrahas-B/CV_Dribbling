# Basketball Drills
This application aims to identify the dribbling skills as part of the fitness.

## Functionalities

This application keeps track of the user's dribbling skills. The main components that are tracked in this application are the following:
1. Total Dribbles performed.

2. Number of dribbles in one hand.
    - Left hand
    - Right hand

3. Number of cross dribbling. (left-to-right or right-to-left).

4. The number of times the basketball went up and down during the dribbling.

## Outputs



## Steps to perform the above functionalities

To achieve the above functionalities, the following steps were implemented:

1. Breaking the video into individual frames for object detection task. This was implemented using **opencv**. All the steps were implemented in correspondence to the availbility of the opencv functions.

2. Applying masking to prevent additional components from interfering in the detection process. A mask image was applied on the frame to prevent additional boxes during the prediction. However, the results was not much of a difference with/without the bitwise and operation with the mask image.

3. The application has been tested on pre-trained **YOLOv8n** and **YOLOvl** for the detection tasks, with YOLOv8l providing accurate results.

4. The YOLO model was used to identify the Basketball ('sports ball' class) and the human with bounding boxes. This provided the co-ordinates for performing the analysis.

5. Using the human bounding box co-ordinates, the knee was identified to be at the 2/3rd location from the head. Whenever the ball crosses the knee co-ordinates. The dribbling score was increased by 1. Similarly, the functionality 4 was also satisfied by using a variable to keep track of the ball movement.

6. To identify which hand was being used, **mediapipe**'s hand posture API was used to identify the location of the hands.

7. This provided the hand co-ordinates that were used to identify which hand was the ball nearer to. Based on the distance metric and the hand co-ordinates, the single hand and cross dribbling was calculated.

## Challenges
The video had variations in the lightings which can usually cause some errors while performing the classification in object detection. This error was very evident while predicting the ball. In some cases, the 'sports ball' was considered as a 'frisbee' and sometimes not even detected.

To overcome this, object tracking with **SORT** was also experimented with **YOLOvn**. However, the use if YOLOv8l provided similar results and made SORT redundant.

Another challenge that was evident was the movement of the camera, which is not suitable for the object detection task. However, for this task, the movement did not cause any problems.
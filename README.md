# Vehicle-Detection
This code is designed to track and count vehicles moving up or down across a specified line in a video. It uses the OpenCV library for video processing and background subtraction to detect moving objects.
## Features
- Detects moving vehicles in a video using background subtraction.
- Counts vehicles crossing a predefined line in the upward or downward direction.
- Displays the vehicle count on the video feed in real-time.
- Unique ID assignment for vehicles to avoid duplicate counting.


## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Numpy


## Code Explanation
Main Steps:
1. Video Input: Captures the video from the specified file.
2. Background Subtraction: Uses the cv2.bgsegm.createBackgroundSubtractorMOG() to detect moving vehicles.
3. Contour Detection: Extracts contours of moving objects.
4. Vehicle Tracking: Assigns a unique ID to each vehicle and tracks its movement.
5. Direction Detection: Determines whether the vehicle is moving up or down based on its position relative to a predefined counting line.
6. Display Output: Shows the original video with bounding boxes, vehicle counts, and movement direction.

Key Variables:
1. min_width_rect & min_height_rect: Minimum width and height to filter detected objects.
2. count_line_position: The vertical position of the counting line.
3. offset: Allowable margin for counting vehicles as they cross the line.

Customization:
Change the counting line position: Modify the count_line_position variable in the code.Adjust the minimum size for detection: Adjust min_width_rect and min_height_rect to change the minimum size of objects considered as vehicles.

Sample Output
The program draws rectangles around detected vehicles and displays counters for vehicles moving up or down:

Output:-
VEHICLES MOVING UP: 3
VEHICLES MOVING DOWN: 2


## Future Improvements
Implement more sophisticated tracking algorithms (e.g., Kalman filters, DeepSORT).
Improve accuracy for occluded vehicles.
Add functionality to track vehicles moving in different lanes or directions.

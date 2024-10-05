import cv2
import numpy as np

# Video capture
cap = cv2.VideoCapture("video2.mp4")

min_width_rect = 80         # Min width of rectangle
min_height_rect = 80        # Min height of rectangle
count_line_position = 550   # Position of the counting line
offset = 4                  # Allowable error between pixels

# Initialize background subtractor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

# Function to calculate the center of a rectangle
def center_handle(x, y, w, h):
    cx = int(x + w / 2)
    cy = int(y + h / 2)
    return cx, cy

# Initialize variables
detect = []
up_counter = 0
down_counter = 0
previous_centers = []
vehicle_id = 0
vehicle_trackers = {}
counted_vehicles = set()  # Set to keep track of counted vehicle IDs

while True:
    ret, frame1 = cap.read()
    
    if not ret:
        break

    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    
    # Applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5), np.uint8))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilat_data = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilat_data = cv2.morphologyEx(dilat_data, cv2.MORPH_CLOSE, kernel)
    counterShape, _ = cv2.findContours(dilat_data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw the counting line
    cv2.line(frame1, (25, count_line_position), (1500, count_line_position), (255, 127, 0), 3)

    # Process each detected object
    new_detect = []
    for (i, c) in enumerate(counterShape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_rect) and (h >= min_height_rect)
        if not validate_counter:
            continue
        
        center = center_handle(x, y, w, h)
        new_detect.append((x, y, w, h))

        # Assign unique ID to new vehicles
        vehicle_id += 1
        vehicle_trackers[vehicle_id] = (x, y, w, h)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, f"Vehicle {vehicle_id}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 244, 0), 2)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

    # Track vehicles and count only once
    for id, (x, y, w, h) in list(vehicle_trackers.items()):
        cx, cy = center_handle(x, y, w, h)
        
        # Check if the vehicle has already been counted
        if id in counted_vehicles:
            continue
        
        if (count_line_position - offset) < cy < (count_line_position + offset):
            # Determine direction
            matched = False
            for prev_center in previous_centers:
                prev_x, prev_y = prev_center
                if abs(prev_x - cx) < min_width_rect and abs(prev_y - cy) < min_height_rect:
                    if cy < prev_y:
                        down_counter += 1
                        print(f"Vehicle Moving Down Counter: {down_counter}")
                    elif cy > prev_y:
                        up_counter += 1
                        print(f"Vehicle Moving Up Counter: {up_counter}")
                    matched = True
                    break
            if not matched:
                previous_centers.append((cx, cy))
                counted_vehicles.add(id)  # Mark vehicle as counted
        else:
            previous_centers.append((cx, cy))
    
    # Display the counters on the frame
    cv2.putText(frame1, f"VEHICLES MOVING UP: {up_counter}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame1, f"VEHICLES MOVING DOWN: {down_counter}", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Show the frame
    cv2.imshow('Video Original', frame1)
    
    # Break the loop on pressing 'Enter'
    if cv2.waitKey(1) == 13:
        break

# Release resources
cv2.destroyAllWindows()
cap.release()

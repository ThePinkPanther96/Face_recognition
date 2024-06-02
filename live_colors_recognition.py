import cv2
import numpy as np


# Initial color ranges
color_ranges = {
    'red': {
        'lower': np.array([170, 70, 50]), 
        'upper': np.array([180, 255, 255])
    },
    'blue': {
        'lower': np.array([100, 150, 0]),
        'upper': np.array([140, 255, 255])
    }
}



def nothing(x):
    # Function to use when operating trackbar
    pass



def create_trackbar(color):
    # Initialize trackbars with current values from color_ranges dictionary
    cv2.createTrackbar(f"L - H ({color})", "Trackbars", color_ranges[color]['lower'][0], 180, nothing)
    cv2.createTrackbar(f"L - S ({color})", "Trackbars", color_ranges[color]['lower'][1], 255, nothing)
    cv2.createTrackbar(f"L - V ({color})", "Trackbars", color_ranges[color]['lower'][2], 255, nothing)
    cv2.createTrackbar(f"U - H ({color})", "Trackbars", color_ranges[color]['upper'][0], 180, nothing)
    cv2.createTrackbar(f"U - S ({color})", "Trackbars", color_ranges[color]['upper'][1], 255, nothing)
    cv2.createTrackbar(f"U - V ({color})", "Trackbars", color_ranges[color]['upper'][2], 255, nothing)



def trakbars():
    cv2.namedWindow("Trackbars") # Create window
    for color in color_ranges:
        create_trackbar(color)



def update_color_ranges():
    for color in color_ranges:
        l_h = cv2.getTrackbarPos(f"L - H ({color})", "Trackbars")
        l_s = cv2.getTrackbarPos(f"L - S ({color})", "Trackbars")
        l_v = cv2.getTrackbarPos(f"L - V ({color})", "Trackbars")
        u_h = cv2.getTrackbarPos(f"U - H ({color})", "Trackbars")
        u_s = cv2.getTrackbarPos(f"U - S ({color})", "Trackbars")
        u_v = cv2.getTrackbarPos(f"U - V ({color})", "Trackbars")
        
        color_ranges[color]['lower'] = np.array([l_h, l_s, l_v])
        color_ranges[color]['upper'] = np.array([u_h, u_s, u_v])



def define_color(hsv, color_ranges):
    combined_mask = None
    for color, ranges in color_ranges.items():
        mask = cv2.inRange(hsv, ranges['lower'], ranges['upper'])
        if combined_mask is None:
            combined_mask = mask 
        else:
            combined_mask = cv2.bitwise_or(combined_mask, mask)
    
    cv2.imshow("Combined Mask", combined_mask)



def load_camera(color_ranges):
    cap = cv2.VideoCapture(0) # 0 is for one webcam
    trakbars()
    while True:
        ret, frame = cap.read() # Load frame from webcam
        if not ret:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert the frame from BGR to HSV
        
        update_color_ranges() # Update the color ranges based on trackbar positions
        define_color(hsv, color_ranges)

        cv2.imshow("Frame", frame) # Show frame from webcam

        key = cv2.waitKey(1) # Number = frame type
        if key == 27: # Number of Esc key for exiting
            break
    
    cap.release() # Close webcam
    cv2.destroyAllWindows() # Close window




# Start the camera
load_camera(color_ranges)

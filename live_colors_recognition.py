import cv2
import numpy as np
import pickle
import os

# Initial color ranges
color_ranges = {
    'red': {
        'lower': np.array([170, 70, 50]), 
        'upper': np.array([180, 255, 255])
    },
}

trackbar_settings = []

# Load settings from the pickle file if it exists
if os.path.exists('data.pkl'):
    with open('data.pkl', 'rb') as file:
        trackbar_settings = pickle.load(file)


def save_data(trackbar_settings):
    with open('data.pkl', 'wb') as file: # Write data
        pickle.dump(trackbar_settings, file) # "dump" = save data


def nothing(x):
    pass


def create_trackbar(color):
    initial_l_h = 90
    initial_l_s = 120
    initial_l_v = 150
    initial_u_h = 100
    initial_u_s = 200
    initial_u_v = 250
    
    # Initialize trackbars with current values from color_ranges dictionary
    initial_l_h = color_ranges[color]['lower'][0]
    initial_l_s = color_ranges[color]['lower'][1]
    initial_l_v = color_ranges[color]['lower'][2]
    initial_u_h = color_ranges[color]['upper'][0]
    initial_u_s = color_ranges[color]['upper'][1]
    initial_u_v = color_ranges[color]['upper'][2]

    # Create trackbars for the lower HSV range for the specified color
    cv2.createTrackbar(f"L - H ({color})", "Trackbars", initial_l_h, 180, nothing)  # Lower Hue range from initial_l_h to 180
    cv2.createTrackbar(f"L - S ({color})", "Trackbars", initial_l_s, 255, nothing)  # Lower Saturation range from initial_l_s to 255
    cv2.createTrackbar(f"L - V ({color})", "Trackbars", initial_l_v, 255, nothing)  # Lower Value range from initial_l_v to 255
    
    # Create trackbars for the upper HSV range for the specified color
    cv2.createTrackbar(f"U - H ({color})", "Trackbars", initial_u_h, 180, nothing)  # Upper Hue range from initial_u_h to 180
    cv2.createTrackbar(f"U - S ({color})", "Trackbars", initial_u_s, 255, nothing)  # Upper Saturation range from initial_u_s to 255
    cv2.createTrackbar(f"U - V ({color})", "Trackbars", initial_u_v, 255, nothing)  # Upper Value range from initial_u_v to 255



def apply_loaded_settings():
    if trackbar_settings:
        for setting in trackbar_settings:
            color = setting['color']
            cv2.setTrackbarPos(f"L - H ({color})", "Trackbars", setting['lower'][0])
            cv2.setTrackbarPos(f"L - S ({color})", "Trackbars", setting['lower'][1])
            cv2.setTrackbarPos(f"L - V ({color})", "Trackbars", setting['lower'][2])
            cv2.setTrackbarPos(f"U - H ({color})", "Trackbars", setting['upper'][0])
            cv2.setTrackbarPos(f"U - S ({color})", "Trackbars", setting['upper'][1])
            cv2.setTrackbarPos(f"U - V ({color})", "Trackbars", setting['upper'][2])


def trakbars():
    cv2.namedWindow("Trackbars") # Create window
    for color in color_ranges:
        create_trackbar(color)
    apply_loaded_settings() # Apply settings after creating trackbars


def update_color_ranges(trackbar_settings):

    for color in color_ranges:
        l_h = cv2.getTrackbarPos(f"L - H ({color})", "Trackbars")
        l_s = cv2.getTrackbarPos(f"L - S ({color})", "Trackbars")
        l_v = cv2.getTrackbarPos(f"L - V ({color})", "Trackbars")
        u_h = cv2.getTrackbarPos(f"U - H ({color})", "Trackbars")
        u_s = cv2.getTrackbarPos(f"U - S ({color})", "Trackbars")
        u_v = cv2.getTrackbarPos(f"U - V ({color})", "Trackbars")
        
        # Update the lower and upper HSV values in the color_ranges dictionary
        color_ranges[color]['lower'] = np.array([l_h, l_s, l_v])
        color_ranges[color]['upper'] = np.array([u_h, u_s, u_v])
        
        # Append the settings to the trackbar_settings list
        trackbar_settings.append({
            'color': color,
            'lower': [l_h, l_s, l_v],
            'upper': [u_h, u_s, u_v]
        })


def define_color(hsv, color_ranges):
    combined_mask = None
    # Iterate over each color and its ranges in the color_ranges dictionary
    for color, ranges in color_ranges.items():
        # Create a mask for the current color using lower and upper HSV bounds
        mask = cv2.inRange(hsv, ranges['lower'], ranges['upper'])
        # Combine the current mask with 'combined_mask' var using 'bitwise OR operation'
        if combined_mask is None:
            combined_mask = mask # If combined_mask is None, initialize it with the current mask
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
        
        update_color_ranges(trackbar_settings=trackbar_settings) # Update the color ranges based on trackbar positions
        define_color(hsv, color_ranges)

        cv2.imshow("Frame", frame) # Show frame from webcam

        key = cv2.waitKey(1) # Number = frame type
        if key == 27: # Number of Esc key for exiting
            break
    
    save_data(trackbar_settings) # Save the settings when exiting
    cap.release() # Close webcam
    cv2.destroyAllWindows() # Close window


# Start the camera
load_camera(color_ranges)

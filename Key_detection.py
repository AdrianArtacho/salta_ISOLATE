import cv2

# Create a window
cv2.namedWindow('KeyCode Detector')

print("Press any key in the OpenCV window to see its key code. Press 'q' to exit.")

while True:
    # Wait for a key press and get the key code
    key = cv2.waitKey(0) & 0xFF

    # Print the key code
    print("Key pressed:", key)

    # If 'q' is pressed, break the loop
    if key == ord('q'):
        break

cv2.destroyAllWindows()

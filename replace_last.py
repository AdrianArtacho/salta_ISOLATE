import gui.gui_enterstring_t as gui_enterstring

def main(file_path, new_first_value=0.0): # duplicate_last_row

    if new_first_value == 0.0:
        video_length = gui_enterstring.main("To make the last rectangle last until the end of the video, enter the length of the video", 
                                            "Length in seconds (e.g. 120.3)", 
                                            "Video length", 
                                            # font=("Arial", 16), 
                                            default_text='0.00',
                                            verbose=False)
        new_first_value = float(video_length)
        
    print(new_first_value, type(new_first_value))
    # exit()


    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Get the last line and split by commas
    last_line = lines[-1].strip().split(',')

    # Replace the first value with the new one
    last_line[0] = f"{new_first_value:.2f}"  # Ensures the float is formatted to 2 decimal places

    # Create the new line by joining the values with commas
    new_line = ', '.join(last_line) + '\n'

    # Append the modified line to the list of lines
    lines.append(new_line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    print(f"Last row duplicated with new first value {new_first_value} in {file_path}.")

if __name__ == "__main__":
    file_path = 'OUTPUT/rectangles_positions.txt'
    # main(file_path, new_first_value=122.20)
    main(file_path)
def read_rectangles_file(file_path):
    positions = []
    
    # Open the file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse each line and convert it into a tuple
    parsed_rectangles = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 5:
            time = float(parts[0])
            x = int(parts[1])
            y = int(parts[2])
            # if int(parts[1]) <= int(parts[3]):
            #     x_leftcorner = int(parts[1])   # x coodinate of the beginning of the rectangle
            #     x_rightcorner = int(parts[3])  
            # else:
            #     x_leftcorner = int(parts[3])   
            #     x_rightcorner = int(parts[1])  
            
            # if int(parts[2]) <= int(parts[4]):
            #     y_leftcorner = int(parts[2])   # y coordinate of the beginning as well
            #     y_rightcorner = int(parts[4])   
            # else:
            #     y_leftcorner = int(parts[4])
            #     y_rightcorner = int(parts[2]) 
            
            width = int(parts[3])
            height = int(parts[4])
            parsed_rectangles.append((time, x, y, width, height))

    # Now we need to convert parsed_rectangles into start/end tuples
    for i in range(len(parsed_rectangles)):
        start_time = parsed_rectangles[i][0]
        x, y, width, height = parsed_rectangles[i][1:]
        
        # Determine the end time
        if i < len(parsed_rectangles) - 1:
            end_time = parsed_rectangles[i + 1][0]
        else:
            end_time = start_time + 5  # Default 5-second duration for the last one

        # Append the tuple in the required format (start_time, end_time, x, y, width, height)
        positions.append((start_time, end_time, x, y, width, height))
    
    return positions

# Example usage:
file_path = 'OUTPUT/rectangles_positions.txt'
positions = read_rectangles_file(file_path)

# Print the positions to check the output
for pos in positions:
    print(pos)

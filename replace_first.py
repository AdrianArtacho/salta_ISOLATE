def main(file_path): # replace_first_float
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modify the first line
    first_line = lines[0].strip().split(',')  # Split the first line by commas
    first_line[0] = '0.00'  # Replace the first float
    lines[0] = ', '.join(first_line) + '\n'  # Recreate the line with the updated value

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    print(f"First float in {file_path} replaced with 0.00.")

if __name__ == "__main__":
    file_path = 'OUTPUT/rectangles_positions.txt'
    main(file_path)
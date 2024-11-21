# Function to process the input file and format it
def process_input_file(file_path):
    formatted_output = []
    
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            # Strip any leading/trailing whitespace and split by the '|' character
            parts = line.strip().split('|')
            
            # Extract the index and numeric value
            # print(parts)
            index = int(parts[0].strip()) + 1  # Start from 1 for the tuple index
            
            # The last part is the numeric value, we clean it of any leading/trailing spaces
            value = float(parts[-1].strip())
            formatted_value = f"{value:.2f}"

            # Everything between the index and value is the building code or name
            code = parts[2].strip()  # Building code or name
            
            # The department name is the first part
            dept = parts[1].strip()  # Department name can span the first and second parts
            
            # Format and add the tuple to the output list
            formatted_output.append(f"({index}, \"{dept}\", \"{code}\", {formatted_value})")
    
    # Join all formatted tuples with commas and newlines
    final_output = ",\n    ".join(formatted_output)
    
    return final_output

# Example of calling the function
file_path = 'data.txt'  # Make sure to specify the correct path to your text file
output = process_input_file(file_path)

# Print the formatted output
print(f"    {output}")


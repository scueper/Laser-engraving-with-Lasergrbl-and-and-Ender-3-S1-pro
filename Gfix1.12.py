# Libraries

import re
import os as os
import time as time


# Variables

lines_processed = 0
empty_lines = 0
comments = 0
command_added = 0
M3_handled = 0
M4_handled = 0
M5_handled = 0
G0_completed = 0
G1_completed = 0
G23_completed = 0
dummy = ''
logging = True # if set True, a logfile will be written for every line translated
tracking = False # if set True, the translation of every line will be displayed, and the prgogram wait for ENTER to proceed to the next line


parsed_data_actual = {
    'command': None,
    'X': None, # X-coordinate
    'Y': None, # Y-coordinate
    'Z': None, # Z-coordinate
    'F': None, # Feedrate
    'S': None, # Laser power / Spindle speed
    'I': None, # Arc parameter
    'J': None, # Arc parameter
    'R': None, # Radius for circular moves (alternative to I/J)
    # Add further relevant parameters here that might occur in your G-Code
}

# fill the "previous" parameter set with a harmless G0 to home to have it contain valid data

parsed_data_previous = {
        'command': 'G0',
        'X': '0',    # X-coordinate
        'Y': '0',    # Y-coordinate
        'Z': '0',    # Z-coordinate
        'F': '1000', # Feedrate
        'S': '0',    # Laser power / Spindle speed
        'I': '0',    # Arc parameter
        'J': '0',    # Arc parameter
        'R': '0',    # Radius for circular moves (alternative to I/J)
    # Add further relevant parameters here that might occur in your G-Code
}

# ********** Parse Function *********************

def parse_gcode_line(line):
   
    # Parses a G-Code line and extracts the command and variables.

    # Args:
    #   line (str): The G-Code line as a string.

    # Returns:
    #    dict: A dictionary with the parsed command and variables.
    #          Missing variables are set to None.

    parsed_data = {
    'command': None,
    'X': None, # X-coordinate
    'Y': None, # Y-coordinate
    'Z': None, # Z-coordinate
    'F': None, # Feedrate
    'S': None, # Laser power / Spindle speed
    'I': None, # Arc parameter
    'J': None, # Arc parameter
    'R': None, # Radius for circular moves (alternative to I/J)
        # Add further relevant parameters here that might occur in your G-Code
    }

    # print("parser is called")
    

    # Regex to find the command (G or M command) and the parameters
    # The first part of the regex catches the command at the start of the line
    # The second part catches the parameters (Letter followed by a number)
    command_match = re.match(r'^([GM]\d+)', line)
    if command_match:
        parsed_data['command'] = command_match.group(1)
        # Remove the command from the line to parse only the parameters
        line_without_command = line[len(command_match.group(1)):].strip()
    else:
        # If no G/M command was found, it might be an invalid line
        # or just a parameter without an explicit command (rare, but possible)
        line_without_command = line # The whole line remains in case it's parameters


    # Regex to find individual G-Code parameters
    # (Letter followed by a number, optionally with decimal point and minus sign)
    param_matches = re.findall(r'([A-Z][-+]?\d*\.?\d*)', line_without_command)

    # Iterate over found parameters and extract values
    for param_str in param_matches:
        param_type = param_str[0]
        
        try:
            param_value = param_str
            # Here the value is formatted to 3 decimal places
            # param_value = float(f"{param_value:.3f}") 
        except ValueError:
            # If the value after the letter is not a valid float
            continue

        # Assignment to corresponding keys in the dictionary
        # Check if the parameter is in our expected parameters
        if param_type in parsed_data:
            parsed_data[param_type] = param_value
        # Optional: If you want to log unknown parameters:
        # else:
        #     print(f"Warning: Unknown parameter '{param_type}' in line: '{line}'")
    
    return parsed_data

# ********************** Main ****************************


# Input paths for infile and outfile:

os.system('CLS')  
infile_path = "Your Working directory/" + input("Inputfile =: Your Working directory/")
print(f"Infile: {infile_path}")
print()
outfile_path = "Your Working directory/" + input("Outputfile =: Your Working directory/")
print(f"Outfile: {outfile_path}")
print()
logfile_path = "Your Working directory/Logfile.txt"
print(f"Outfile: {logfile_path}")
print()


print("Starting conversion")
print()

if logging:
    logfile = open(logfile_path, 'w')


# Open input file for reading and output file for writing

with open(infile_path, 'r') as infile, open(outfile_path, 'w') as outfile:

    # write "M3 I" at the beginning to enable the laser

    outfile.write('M3 I' + '\n')

    # Read every line of the input file, complete it, and write it to the output file

    for line in infile:
        lines_processed = lines_processed + 1
        outline = ""
    

        # Pre-filtering without parsing where parsing is not useful:

        # Filter out empty lines

        if (len(line) == 1):
            outline = line
            empty_lines = empty_lines + 1

        # Filter out comments

        elif (line[0] == ';'):
            outline = line
            comments = comments + 1

        # Send remaining lines to the parser

        else:
        
            # Parse line

            parsed_data_actual = parse_gcode_line(line)

            # Output results to logfile if logging is enabled

            if logging:
                # os.system ('clear')
                logfile.write('Line ' + str(lines_processed) + ' in:' + '\n') 
                logfile.write(line)
                logfile.write('\n')
                logfile.write('Parsed data actual' + '\n')
                logfile.write(f"ENTRY: {str(parsed_data_actual)}\n")
                logfile.write('\n')
                logfile.write('Parsed data previous' + '\n')            
                logfile.write(f"ENTRY: {str(parsed_data_previous)}\n")
                logfile.write('\n') 
                logfile.write('Process ---->') 
                logfile.write('\n')        
              
            # Line by line processing with display if tracking is enabled

            if tracking:
                os.system ('CLS')
                print('Line:' + str(lines_processed)) 
                print(line)
                print('Parsed data actual')            
                print(parsed_data_actual)
                print()
                print('Parsed data previous')            
                print(parsed_data_previous)


            # Depending on the command, fill and assemble the line

            # If the command is missing (only X,Y,S,F present), insert the last command

            if parsed_data_actual['command'] == None:

                # Case 1: Only S present

                if (parsed_data_actual['S'] != None)\
                    and (parsed_data_actual['F'] == None)\
                    and (parsed_data_actual['X'] == None)\
                    and (parsed_data_actual['Y'] == None):
                    parsed_data_actual['command'] = 'M3'

                # Case 2: Only X or only Y or X and Y present

                elif (parsed_data_actual['X'] != None) or (parsed_data_actual['Y'] != None):
                    parsed_data_actual['command'] = parsed_data_previous['command'] 
                
                # Case 3: Only F, I, J present: Add no command, do nothing

                command_added = command_added + 1 

            # Depending on the command, complete and assemble the new command line

            # Command = M3

            if str(parsed_data_actual['command']) == 'M3':

                # If S is missing, insert previous S

                if(parsed_data_actual['S'] == None):
                    parsed_data_actual['S'] = parsed_data_previous['S'] 

                outline = 'M3' + ' '\
                + str(parsed_data_actual['S'])\
                + '\n'
                M3_handled += 1

            # Command = M4, remains without parameters

            if str(parsed_data_actual['command']) == 'M4':    
 
                 # build outline

                outline = 'M3 I' + '\n' 
                M4_handled += 1

            # Command = M5, remains without parameters

            if str(parsed_data_actual['command']) == 'M5':    

                # build outline

                outline = 'M5' + '\n'
                M5_handled += 1

            # Command = G0, padded with X, Y, F and hard-coded S0

            if str(parsed_data_actual['command']) == 'G0':
                if(parsed_data_actual['X'] == None):
                    parsed_data_actual['X'] = parsed_data_previous['X']   
                if(parsed_data_actual['Y'] == None):
                    parsed_data_actual['Y'] = parsed_data_previous['Y']   
                if(parsed_data_actual['F'] == None):
                    parsed_data_actual['F'] = parsed_data_previous['F']
                # For G0 command, a missing S is not entered in the dictionary, it is always 0
                # if(parsed_data_actual['S'] == None):
                    # parsed_data_actual['S'] = 'S0' 

                # build outline

                outline = \
                str(parsed_data_actual['command']) + ' '\
                + str(parsed_data_actual['X']) + ' '\
                + str(parsed_data_actual['Y']) + ' '\
                + 'S0 ' \
                + str(parsed_data_actual['F'])\
                + '\n'


                G0_completed += 1

            # Command = G1, padded with X, Y, F and S

            if str(parsed_data_actual['command']) == 'G1':
                if(parsed_data_actual['X'] == None):
                    parsed_data_actual['X'] = parsed_data_previous['X']  
                if(parsed_data_actual['Y'] == None):
                    parsed_data_actual['Y'] = parsed_data_previous['Y']   
                if(parsed_data_actual['F'] == None):
                    parsed_data_actual['F'] = parsed_data_previous['F']
                if(parsed_data_actual['S'] == None):
                    parsed_data_actual['S'] = parsed_data_previous['S'] 

                # build outline

                outline = \
                str(parsed_data_actual['command']) + ' '\
                + str(parsed_data_actual['X']) + ' '\
                + str(parsed_data_actual['Y']) + ' '\
                + str(parsed_data_actual['S']) + ' '\
                + str(parsed_data_actual['F']) + ' '\
                + '\n'
                G1_completed += 1

            # Command = G2 or G3, padded with X, Y, I, J, F and S

            if (str(parsed_data_actual['command']) == 'G2') or (str(parsed_data_actual['command']) == 'G3'):
                if(parsed_data_actual['X'] == None):
                    parsed_data_actual['X'] = parsed_data_previous['X']   
                if(parsed_data_actual['Y'] == None):
                    parsed_data_actual['Y'] = parsed_data_previous['Y']   
                if(parsed_data_actual['I'] == None):
                    parsed_data_actual['I'] = parsed_data_previous['I']   
                if(parsed_data_actual['J'] == None):
                    parsed_data_actual['J'] = parsed_data_previous['J']  
                if(parsed_data_actual['F'] == None):
                    parsed_data_actual['F'] = parsed_data_previous['F']
                if(parsed_data_actual['S'] == None):
                    parsed_data_actual['S'] = parsed_data_previous['S'] 

                # build outline

                outline = \
                str(parsed_data_actual['command']) + ' '\
                + str(parsed_data_actual['X']) + ' '\
                + str(parsed_data_actual['Y']) + ' '\
                + str(parsed_data_actual['I']) + ' '\
                + str(parsed_data_actual['J']) + ' '\
                + str(parsed_data_actual['S']) + ' '\
                + str(parsed_data_actual['F']) + ' '\
                + '\n'
                G23_completed += 1

            # Write result
  
            outfile.write(outline)

            
            # Fill parsed previous with the last valid values

            # M3, M4 and M5 are not saved as previous, they are single commands

            if (parsed_data_actual['command'] not in ['M3', 'M4', 'M5']):

                # All G-commands are saved as previous

                if(parsed_data_actual['command'] != None):
                    parsed_data_previous['command'] = parsed_data_actual['command']

            # All parameters (non-commands) are saved as previous

            if(parsed_data_actual['X'] != None):
                parsed_data_previous['X'] = parsed_data_actual['X']

            if(parsed_data_actual['Y'] != None):
                parsed_data_previous['Y'] = parsed_data_actual['Y']

            if(parsed_data_actual['Z'] != None):
                parsed_data_previous['Z'] = parsed_data_actual['Z']

            if(parsed_data_actual['F'] != None):
                parsed_data_previous['F'] = parsed_data_actual['F']

            if(parsed_data_actual['S'] != None):
                parsed_data_previous['S'] = parsed_data_actual['S']

            if(parsed_data_actual['I'] != None):
                parsed_data_previous['I'] = parsed_data_actual['I']

            if(parsed_data_actual['J'] != None):
                parsed_data_previous['J'] = parsed_data_actual['J']

            if(parsed_data_actual['R'] != None):
                parsed_data_previous['R'] = parsed_data_actual['R']


            # Write result to logfile if logging is enabled

            if logging:
                logfile.write('\n')
                logfile.write('Parsed data actual corrected' + '\n')
                logfile.write(f"ENTRY: {str(parsed_data_actual)}\n")
                logfile.write('\n')
                logfile.write('Parsed data previous corrected' + '\n')            
                logfile.write(f"ENTRY: {str(parsed_data_previous)}\n")
                logfile.write('\n')
                logfile.write('Line ' + str(lines_processed) + ' out:' + '\n') 
                logfile.write(outline)
                logfile.write('\n')
                logfile.write("Empty lines:       " + str(empty_lines) + '\n')
                logfile.write("Comments:          " + str(comments) + '\n')
                logfile.write("Command added:     " + str(command_added) + '\n')
                logfile.write("M3 handled:        " + str(M3_handled) + '\n')
                logfile.write("M4 handled:        " + str(M4_handled) + '\n')
                logfile.write("M5 handled:        " + str(M5_handled) + '\n')
                logfile.write("G0 handled:        " + str(G0_completed) + '\n')
                logfile.write("G1 handled:        " + str(G1_completed) + '\n')
                logfile.write("G23 handled:       " + str(G23_completed) + '\n')
                logfile.write ("\n") 
                logfile.write ("_________________________________________________________________" + "\n")
                logfile.write ("\n")
                 

            # Publish result and trigger next line with Enter if tracking is enabled

            if tracking:
                print()
                print('Parsed data actual corrected')            
                print(parsed_data_actual)
                print()
                print('Parsed data previous corrected')            
                print(parsed_data_previous)
                print()
                print('Outline')
                print(outline)
                print()
                print("Lines processed:  ", lines_processed)
                print("Empty lines:      ", empty_lines)
                print("Comments:         ", comments)
                print("Command added:    ", command_added)
                print("M3 handled:       ", M3_handled)
                print("M4 handled:       ", M4_handled)
                print("M5 handled:       ", M5_handled)
                print("G0 handled:       ", G0_completed)
                print("G1 handled:       ", G1_completed)
                print("G23 handled:      ", G23_completed)
                print () 
                dummy = input('Hit Enter to continue...')


# Close files when everything is converted

infile.close()
outfile.close()
if logging:
    logfile.close()


# Feedback and correction statistics

print('**************** Report *********************')
print()
print("File was successfully copied.")
print()
print(f"Infile: {infile_path}")
print()
print(f"Outfile: {outfile_path}")
print()
print("Lines processed:  ", lines_processed)
print("Empty lines:      ", empty_lines)
print("Comments:         ", comments)
print("Command added:    ", command_added)
print("M3 handled:       ", M3_handled)
print("M4 handled:       ", M4_handled)
print("M5 handled:       ", M5_handled)
print("G0 handled:       ", G0_completed)
print("G1 handled:       ", G1_completed)
print("G23 handled:      ", G23_completed)
print ()
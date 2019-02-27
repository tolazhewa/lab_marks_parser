import sys, re, os, glob, zipfile, shutil
from subprocess import call

def get_grade(file_name, mark):
    with open(file_name) as file:
        # Read the content of the file
        file_content = file.read()

        # Parse for name, score, and percentage (all return lists of matches)
        name_list = re.findall(".*\s-\s(.*)\s-\s", file_name)
        student_num = re.findall("Student:\s.*\s\((\d*)\)\n", file_content)
        score_list = re.findall("Score:\s*(.*\/.*)\s\(\d*[\.|\,]\d*\%\)\s*\n", file_content)
        perc_list = re.findall("Score:\s*.*\/.*\s\((\d*[\.|\,]\d*\%)\)\s*\n", file_content)

        # If it ever encounters a case where all three of those are found, it will print error and ret
        if len(name_list) != 1 or len(score_list) != 1 or len(perc_list) != 1:
            print("ERROR OCCURED FOR:", file_name)
            print("\n----- RESULTS FILE CONTENTS -----")
            call(["tail", "-n", "5", file_name])
            print("---------------------------------\n\n")
            return None

        # Properly format the name
        name_list = name_list[0].split(" ")
        for n in name_list:
            if n != '':
                n = n[0].upper() + n.lower()[1:]

        first_name = name_list[0]
        last_name = " ".join(name_list[1:])

        mark = float("{0:.2f}".format(float(perc_list[0][:-1].replace(",","."))/100.0 * mark))

        
        # Return the current student's first name, last name(s), score, percentage, and adjusted mark
        return [first_name, last_name, student_num[0],score_list[0], perc_list[0], mark]

# Check multiple entries by the same student, return index 
def duplicate_index(arr, elem):
    for i in range(len(arr)):
        if arr[i][0] == elem[0] and arr[i][1] == elem[1]: # If the first and last names match return the index
            return i
    return -1 # Else return -1


def print_grades(arr):
    # Prints the list with proper formatting
    print("{:<30} {:<8} {:<12} {:<10} {:<8}".format("Last Name, First Name","Mark","Student #","Score","Percent"))
    print("------------------------------------------------------------------------")
    for first_name, last_name, student_num, score, grade, mark in arr:
        print('{:<30} {:<8} {:<12} {:<10} {:<8}'.format(last_name + ", " + first_name, '%.2f' % mark, student_num, score, grade))
    print("------------------------------------------------------------------------\n")
    print("Number of Valid Students Submissions:", len(arr))


################################# EXECUTION AREA ##########################$
# Zip file mode = 0
# Directory mode = 1
mode = 0
arg = sys.argv[1]

# Ensure the user inputs 2 arguments
if len(sys.argv) == 3:
    try:
        mark_value = float(sys.argv[2])
    except ValueError:
        print("mark_value must be a numerical value")
elif len(sys.argv) == 2:
    mark_value = 5.0
else:
    print('Please execute in this format: python3 lab_marker.py <zip file OR dir> (<mark_value>)')
    exit()

if arg[-4:] == ".zip":
    root_path = "marks"
    with zipfile.ZipFile(arg, "r") as zip_ref:
        zip_ref.extractall(root_path)
elif os.path.isdir(arg):
    root_path = arg
    mode = 1
else:
    print("Not zip file or directory... exiting.")
    exit(-1)

entries = []

# Go through every txt file in subdirectory
for dir_name,_,_  in os.walk(root_path):
    for filename in glob.glob(dir_name + "/*.txt"):
        entry = get_grade(filename, mark_value)

        # If multiple entries, take the higher mark, else add the entry
        if entry != None:
        
            dup = duplicate_index(entries, entry)
            if dup != -1:
                if entry[5] > entries[dup][5]:
                    entries[dup] = entry
            else:
                entries.append(entry)

# Sorts the students based off of last name
entries = sorted(entries, key=lambda x: x[1])

# Print the grades
print_grades(entries)

if mode == 0:
    shutil.rmtree(root_path)
############################################################################

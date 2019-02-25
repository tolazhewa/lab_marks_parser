import sys, re, os, glob, zipfile, shutil
from subprocess import call

def add_grade(arg, mark):
    with open(arg) as file:
        # Read the content of the file
        file_content = file.read()

        # Parse for name, score, and percentage (all return lists of matches)
        name_list = re.findall("Student:\s(.*)\s\(.*\)\s*\n", file_content)
        score_list = re.findall("Score:\s*(.*\/.*)\s\(\d*[\.|\,]\d*\%\)\s*\n", file_content)
        perc_list = re.findall("Score:\s*.*\/.*\s\((\d*[\.|\,]\d*\%)\)\s*\n", file_content)
        
        # If it ever encounters a case where all three of those are found, it will print error and ret
        if len(name_list) != 1 or len(score_list) != 1 or len(perc_list) != 1:
            print("ERROR OCCURED FOR:", arg)
            print("\n----- RESULTS FILE CONTENTS -----")
            call(["tail", "-n", "5", arg])
            print("---------------------------------\n\n")
            return None

        # Properly format the name
        name = ""
        for n in name_list[0].split(" "):
            if n != '':
                name += n[0].upper() + n.lower()[1:] + " "
        name = name[:-1]

        mark = float("{0:.2f}".format(float(perc_list[0][:-1].replace(",","."))/100.0 * mark))
        # Return the current student name, score, percentage
        return [name,score_list[0],perc_list[0],mark]

def print_grades(arr):
    # Prints the list with proper formatting
    print("\n")
    for student,score,grade,mark in arr:
        print('{:<25} {:<15} {:<10} {:<10}'.format(student, score, grade, '%.2f' % mark))


################################# EXECUTION AREA ##########################$
# Zip file mode = 0
# Directory mode = 1
mode = 0
arg = sys.argv[1]

# Ensure the user inputs 2 arguments
if len(sys.argv) == 3:
    try:
        mark = float(sys.argv[2])
    except ValueError:
        print("mark_value must be a numerical value")
elif len(sys.argv) == 2:
    mark = 5.0
else:
    print('Please execute in this format: python3 lab_marker.py <zip file OR dir> (<mark_value>)')
    exit()

if arg[-4:] == ".zip":
    dir_path = "marks"
    with zipfile.ZipFile(arg, "r") as zip_ref:
        zip_ref.extractall(dir_path)
elif os.path.isdir(arg):
    dir_path = arg;
    mode = 1
else:
    print("Not zip file or directory... exiting.")
    exit(-1)

students = []

# Go through every txt file in subdirectory
for filename in glob.glob(os.path.join(dir_path, '*/*.txt')):
    grade = add_grade(filename, mark)
    if grade != None:
        students.append(grade)

# Sorts the students based off of name
students = sorted(students, key=lambda x: x[0])
print_grades(students)

if mode == 0:
    shutil.rmtree(dir_path)
############################################################################
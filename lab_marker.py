import sys, re, os, glob

def add_grade(arg):
    with open(arg) as file:
        # Read the content of the file
        file_content = file.read()

        # Parse for name, score, and percentage (all return lists of matches)
        name_list = re.findall("Student:\s(.*)\s\(.*\)\s*\n", file_content)
        score_list = re.findall("Score:\s*(.*\/.*)\s\(\d*[\.|\,]\d*\%\)\s*\n", file_content)
        perc_list = re.findall("Score:\s*.*\/.*\s\((\d*[\.|\,]\d*\%)\)\s*\n", file_content)
        
        # If it ever encounters a case where all three of those are found, it will print error and ret
        if len(name_list) != 1 or len(score_list) != 1 or len(perc_list) != 1:
            print("ERROR OCCURED FOR:",arg)
            # print("name_list len:", len(name_list),name_list)
            # print("score_list len:", len(score_list),score_list)
            # print("perc_list len:", len(perc_list),perc_list)
            return None

        # Properly format the name
        name = ""
        for n in name_list[0].split(" "):
            if n != '':
                name += n[0].upper() + n.lower()[1:] + " "
        name = name[:-1]

        # Return the current student name, score, percentage
        return [name,score_list[0],perc_list[0]]

def print_grades(arr):
    # Prints the list with proper formatting
    print("\n")
    for student,score,grade in arr:
        print('{0: <25}'.format(student),"\t",score,"\t",grade)


################################# EXECUTION AREA ##########################$
# Ensure the user inputs 2 arguments
if len(sys.argv) != 2:
    print('Please execute in this format: python3 lab_marker.py <dir>')
    exit()

dir_path = sys.argv[1]
students = []

# Go through every txt file in subdirectory
for filename in glob.glob(os.path.join(dir_path, '*/*.txt')):
    grade = add_grade(filename)
    if grade != None:
        students.append(grade)

# Sorts the students based off of name
students = sorted(students, key=lambda x: x[0])
print_grades(students)
############################################################################
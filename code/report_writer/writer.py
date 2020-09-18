from ruamel import yaml
import os

HEADER = """\\noindent
{{\Large{{\\textbf{{{assignment_name}}}}} \\\\
Assigned: {assigned} \\\\
Due: {due}

"""

PROBLEM_TEMPLATE = '''\\noindent
\linia
\subsection*{{{problem_name}}}
\subsubsection*{{{file_name}}}
\par{{
{point_breakdown}
%%%%% notes go in the below section %%%%%
\\begin{{lstlisting}}[basicstyle=\itshape]
{comments}
\end{{lstlisting}}
}}
\\vspace{{0.5cm}}
\\begin{{flushright}}\\textbf{{Score}}: {student_score}/{total_score}\end{{flushright}}
'''

FOOTER = """\\noindent
\linia
\\begin{{flushright}}\hfill \\textbf{{Total Score}}: {}/{}\end{{flushright}}
"""

def create_tex(username, assignment_number, problem_data_folder):
    all_data = load_student_problem_data(username, assignment_number, problem_data_folder)
    overall_total = overall_score = 0
    try:
        assigned = all_data['assigned']
    except:
        assigned = ''
    try:
        due = all_data['due']
    except:
        due = ''
    res = HEADER.format(assignment_name="Assignment {}".format(assignment_number), assigned=assigned, due=due)
    #student_data = all_data["problems"] 
    #print(student_data)
    #student_data["autograder"] = all_data["autograder"]
    for problem in all_data["problems"]:
        #data = student_data[problem]

        #Set these variables mostly for clarity
        problem_name = problem["name"]
        file_name = problem["filename"]
        comments = problem["comments"]

        test_results = get_test_case_results(all_data["autograder"], file_name)

        student_score, total_score, point_breakdown = create_point_breakdown(problem["parts"], test_results)

        # if "test_cases" in data:
        #     student_score, total_score, point_breakdown = create_point_breakdown(data["point_breakdown"], data["test_cases"])
        # else: 
        #     student_score, total_score, point_breakdown = create_point_breakdown(data["point_breakdown"], {})

        prob = format_problem(problem_name, file_name, point_breakdown, comments, student_score, total_score)
        res += prob
        res += "\n\n"

        overall_score += student_score
        overall_total += total_score    
    f = FOOTER.format(overall_score, overall_total)
    res += f

    dest = problem_data_folder.split("fragments")[0] #Get location of data folder
    dest = dest + "reports/{}/Assignments/Assignment{}.tex".format(username, assignment_number)
    write_tex(res, dest, True)

def load_student_problem_data(username, assignment_number, problem_data_path):
    p = problem_data_path.format(username)
    main_data_path = p + "/Assignment{}.yaml".format(assignment_number)
    autograder_data_path = p + "/Assignment{}-autograder.yaml".format(assignment_number)
    
    student_data = {}
    try:
        with open(main_data_path) as f:
            student_data = yaml.safe_load(f)

        try: 
            with open(autograder_data_path) as f:
                student_data["autograder"] = yaml.safe_load(f)
        except:
            #TODO make this more specific
            #print("Didn't find autograder yaml file")
            student_data["autograder"] = {}
    except: 
        print("Error loading yaml file for: {}".format(username))
        student_data["autograder"] = {}


    return student_data

def get_test_case_results(data, file_name):
    if file_name in data.keys():
        return data[file_name]
    else: 
        return {}

def create_point_breakdown(problem_parts, test_cases):
    pts_total = 0
    earned_total = 0

    body = ""
    for item in problem_parts:
        body += "\n"
        earned, total, note = item["score"], item["point_value"], item["description"]
        pts_total += total
        earned_total += earned

        line = f"{earned}/{total} {note} \\\\"
        body += line

    for function, results_list in test_cases.items():
        body += "\n"

        earned, total = 0, 0
        for res in results_list:
            sub_earned, sub_total = 5 if res["passed"] else 0, 5
            
            total +=  sub_total
            earned += sub_earned

        pts_total += total
        earned_total += earned

        note = f"{function} Test Cases"
        line = f"{earned_total}/{total} {note} \\\\"
        body += line
    body = f"{pts_total} points total \\\\" + body
    return (earned_total, pts_total, body)
    

def format_problem(problem_name, file_name, point_breakdown, comments, student_score, total_score):
    return PROBLEM_TEMPLATE.format(**locals())

def write_tex(formatted_tex, dest, make_dest=False):
    if make_dest:
        folders = "/".join(dest.split("/")[0:-1])
        os.makedirs(folders, exist_ok=True)
    with open(dest, 'w') as f:
        print(formatted_tex, file=f)


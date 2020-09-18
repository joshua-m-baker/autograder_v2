import sys
import contextlib
import io
import importlib
from grader.newTestCase import NewTestCase
from grader.testResult import TestResult

#TODO: detect class tests type(x).__module__=='builtins'
#TODO: custom post-processing on equality values

def importModules(module_names, qualified_path=''):
    errorMessages = []
    imports = {}
    original_stdin = sys.stdin
    for name in module_names:
        printBuffer = io.StringIO()
        with contextlib.redirect_stdout(printBuffer): #supress any outputs while loading, but save them for later if needed
            sys.stdin = io.StringIO("") # this will cause input to hit an EOF error, which stops importing the file and gets caught by the importer
            try:
                full_name = "{}.{}".format(qualified_path, name) if qualified_path else name
                imports[name] = importlib.import_module(full_name) #solution files should end in _solution to prevent name conflicts

            except Exception as e:
                errorMessages.append({name: e})
                # TODO maybe put None or the exception in the imports dict so it can be added to the didn't run message
        #output = printBuffer.getvalue()
        #import_outputs[import_name] = last_print(printBuffer.getvalue())

    for error in errorMessages:
        key = next(iter(error)) #we know there's only one key pair, so grab that. https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary/39292086
        print("Error importing:", key)
        print(error[key])
    sys.stdin = original_stdin
    return imports

def runTests(test_values, studentModules, solutionModules):
    results = {}

    for module_name, function_dict in test_values.items():

        results[module_name] = {}
    
        #for function_name, tests_dict in function_dict.items():
        for function_name, test_list in function_dict.items():

            results[module_name][function_name] = []
            #for test_name, test_input in tests_dict.items():
            for test_input in test_list: 
                try:
                    student_function = getattr(studentModules[module_name], function_name)
                    solution_function = getattr(solutionModules[module_name+"_solution"], function_name)

                    testCase = NewTestCase("test_name", student_function, solution_function, test_input)
                    results[module_name][function_name].append(testCase.run_test())

                except Exception as e:
                    notRan = TestResult("test_name", False, test_input, f"Error running student code: {e}", None)

                    results[module_name][function_name].append(notRan)

    return results

def print_results(results_dict):
    print()
    print("Results")
    print("-"*10)
    any_failed = False
    for module_name, function_dict in results_dict.items():
        print(module_name)
        for function_name, results_list in function_dict.items():

            # for result in results_list:
            #     result.print_result() 

            print("{}{}".format("\t", function_name), end=': ')
            any_failed = any_failed or any([not t.test_passed() for t in results_list])
            
            score = sum(t.test_passed() == True for t in results_list) / len(results_list)
            score = str(sum(t.test_passed() == True for t in results_list)) + "/" + str(len(results_list))

            print(score)
    if not any_failed:
        return

    input("Press any key to see why cases failed")
    for module_name, function_dict in results_dict.items():

        # if all([t.test_passed() for r in function_dict.values() for t in r.values()]):
        #     continue

        print(module_name + ":")

        for function_name, results_list in function_dict.items():
            spaces = 2        
                
            if all([t.test_passed() for t in results_list]):
                continue
            print("{}Function {}:".format(" "*spaces, function_name))

            for result in results_list:
                if not result.test_passed():
                    spaces = 6
                    lines = result.get_result_lines()
                    for line in lines:
                        print("{}{}".format(" "*spaces, line))
                    print()

            # print("{}{}".format("\t", function_name), end=': ')

            # score = sum(t.test_passed() == True for t in results_list) / len(results_list)
            # score = str(sum(t.test_passed() == True for t in results_list)) + "/" + str(len(results_list))

            # print(score)

# def write_results(username, assignment_number, results_dict):
#     with open("")
#     for module_name, function_dict in results_dict.items():
#         for function_name, results_list in function_dict.items():
            
#             template_data = 

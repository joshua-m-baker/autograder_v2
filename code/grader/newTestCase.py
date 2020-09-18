from grader.testResult import TestResult
# from numpy import allclose

class NewTestCase():
    def __init__(self, test_name, student_function, solution_function, input_value):
        self.test_name = test_name
        self.student_function = student_function
        self.solution_function = solution_function
        self.input_value = input_value
        self.passed = False
        self.ran = False

class NewTestCase():
    def __init__(self, test_name, student_function, solution_function, input_value):
        self.test_name = test_name
        self.student_function = student_function
        self.solution_function = solution_function
        self.input_value = input_value
    
    @staticmethod
    def are_equal(student_result, solution_result):
        tau = .001
        #Start with naive comparison
        naive = student_result == solution_result

        if naive:
            return naive

        #Handle case of 0/1 for True/False
        elif (student_result in [0,1] or solution_result in [0,1]) and (student_result in [True, False] or solution_result in [True, False]):
            return bool(student_result) == bool(solution_result)

        #Handle case of similar numbers easier to just try and see if it works over testing types
        try:
            diff = abs(student_result - solution_result)
            return diff < tau
        except Exception as e:
            pass

        return False

    def run_test(self):
        student_result = self.student_function(*self.input_value)
        solution_result = self.solution_function(*self.input_value)

        result = NewTestCase.are_equal(student_result, solution_result)
        return TestResult(self.test_name, result, self.input_value, student_result, solution_result)

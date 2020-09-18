

class TestResult():

    def __init__(self, test_name, passed, input_value, student_result, solution_result):
        self.name = test_name
        self.passed = passed
        self.input_value = input_value
        self.student_result = student_result
        self.solution_result = solution_result

    #Provide a single test result, with relative indentation
    def get_result_lines(self):
        #Do it this way so something else can handle indentation
        return [f"Name: {self.name} Input value was: {self.input_value}", f"\t Student result: {self.student_result}", f"\t Grader result: {self.solution_result}"]

    def test_passed(self):
        return self.passed

    def write_result(self):
        pass

    #TODO Fix this hacky bs
    def dict_repr(self):
        return vars(self)

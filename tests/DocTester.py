import ast
from darglint.function_description import FunctionDescription, FunctionType
from darglint.integrity_checker import IntegrityChecker
import darglint.errors
from io import TextIOWrapper
from TesterUtils import *

class DocTester:
    def __init__(self):
        self.expected_docstrings = []
        self.defs = []
        self.results = {}
        self.ignored = (darglint.errors.EmptyTypeError,
                        darglint.errors.ExcessNewlineError,
                        darglint.errors.ExcessRaiseError,
                        darglint.errors.ParameterTypeMismatchError,
                        darglint.errors.ParameterTypeMissingError,
                        darglint.errors.ReturnTypeMismatchError
                       )

    def _is_ignored(self, err):
        return isinstance(err, self.ignored)


    def check_docstrings(self):
        for (fname, docstrings) in self.expected_docstrings:
            with open(fname, 'r') as file:
                tree = ast.parse(file.read())
            ic = IntegrityChecker()
            fun_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
            for f in fun_defs:
                if ast.get_docstring(f):
                    ic.errors = []
                    ic.run_checks(FunctionDescription(FunctionType.FUNCTION, f))
                    self.results[f.name] = [err for err in ic.errors if not self._is_ignored(err)]
            class_defs = [n for n in tree.body if isinstance(n, ast.ClassDef)]
            for c in class_defs:
                if ast.get_docstring(c):
                    self.results[f"class {c.name}"] = []
                methods = [n for n in c.body if isinstance(n, ast.FunctionDef)]
                for m in methods:
                    if ast.get_docstring(m):
                        ic.errors = []
                        name = f"{c.name}.{m.name}"
                        ic.run_checks(FunctionDescription(FunctionType.METHOD, m))
                        self.results[name] = [err for err in ic.errors if not self._is_ignored(err)]

    def get_result(self, fname, ex_name):
        try:
            errs = self.results[ex_name]
            if not errs:
                message = "PASS"
                marks = 1
            else:
                errs = self.results[ex_name]
                message = f"ISSUES"
                marks = 0.5
        except KeyError:
            message = "MISSING"
            marks = 0
            errs = []
        finally:
            message = f"{message:<10}: {ex_name} (in {fname})"
            if errs:
                for err in errs:
                    message += "\n" + 12*" " + err.description
                    message += "\n" + 12*" " + err.message()
            return (marks, message)

    def write_summary(self, outfile):
        double_line_centered("DOCUMENTATION", outfile)
        grade = 0
        total = 0
        for (fname, ds) in self.expected_docstrings:
            for d in ds:
                mark, msg = self.get_result(fname, d)
                print(msg, file=outfile)
                grade += mark
                total += 1
        double_line(outfile)
        final_grade = 10.0 * grade/total
        print(f"TOTAL DOCUMENTATION MARK: " +
              f"{final_grade:.1f}/10",file=outfile)
        double_line(outfile)
        return final_grade

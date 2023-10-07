import re
from Table import Table
        
class CommandParser:
    def __init__(self):
        self.tables = {}

    def execute(self, command):
        # unary operations like select and project
        unary_match = re.match(r"\((.*)\)(select|project)\[([^\]]+)\]", command)
        if unary_match:
            return self._handle_unary_operations(unary_match)
        
        # CARTESIAN PRODUCT
        cartesian_match = re.match(r"\((.*)\)(x)\((.*)\)", command)
        if cartesian_match:
            return self._handle_set_operations(cartesian_match) # this is a hacky way to reuse the unary method but cartesian product is not a unary operation
        
        # set operations like union, intersect, and difference
        set_match = re.match(r"\((.*)\)(U|-|&)\((.*)\)", command)
        if set_match:
            return self._handle_set_operations(set_match)

        # binary operations
        binary_match = re.match(r"\((.*)\)(join|-join|join-|-join-)\[(\w+)=(\w+)\]\((.*)\)", command)
        if binary_match:
            return self._handle_binary_operations(binary_match)

        # Base case: just a table name
        if command in self.tables:
            return self.tables[command]
    
    def _handle_create(self, command):
        table_name_match = re.search(r"create (\w+)", command)
        if not table_name_match:
            return "Invalid create command."

        table_name = table_name_match.group(1)
        content = command.split("{", 1)[1].rsplit("}", 1)[0].strip()

        # Split by lines and then split each line by comma to get attributes and data
        lines = content.split('\n')
        columns = [col.strip() for col in lines[0].split(",")]

        new_table = Table(table_name)
        for line in lines[1:]:
            values = [v.strip() for v in line.split(",")]
            row = dict(zip(columns, values))
            new_table.rows.append(row)

        # Add the new table to the parser's tables and return it
        self.tables[table_name] = new_table
        return new_table
            
    def _handle_unary_operations(self, match):
        inner_command, operation, args = match.groups()
        result_table = self.execute(inner_command)  # recursively handle inner command

        if operation == "select":
            return self._handle_select(result_table, args)            

        elif operation == "project":
            return self._handle_project(result_table, args)
        
    def _handle_set_operations(self, match):
        left_command, operation, right_command = match.groups()
        left_table = self.execute(left_command)
        right_table = self.execute(right_command)

        if operation == "U":
            return left_table.union(right_table)
        elif operation == "&":
            return left_table.intersection(right_table)
        elif operation == "-":
            return left_table.difference(right_table)
        elif operation == "x":
            return left_table.cartesian_product(right_table)

    
    def _handle_binary_operations(self, match):
        left_command, operation, left_column, right_column, right_command = match.groups()
        left_table = self.execute(left_command)
        right_table = self.execute(right_command)

        if operation == "join":
            return left_table.inner_join(right_table, left_column, right_column)
        elif operation == "-join":
            return left_table.left_join(right_table, left_column, right_column)
        elif operation == "join-":
            return left_table.right_join(right_table, left_column, right_column)
        elif operation == "-join-":
            return left_table.full_join(right_table, left_column, right_column)
        else:
            raise ValueError(f"Invalid join condition in command: {operation}")
        
    def _handle_select(self, table, args):
        column, op, value = re.match(r"(\w+)([><=!]+)([\w.]+)", args).groups()
        try:
            value = float(value)
            if value.is_integer():
                value = int(value)
        except ValueError:
            pass
        return table.select(column, op, value)

    def _handle_project(self, table, args):
        columns = [col.strip() for col in args.split(',')]
        return table.project(*columns)
    
    def print(self, table_name):
        if table_name in self.tables:
            print(self.tables[table_name])
    
    def print_tables(self):
        print(f"Table Count: {len(self.tables)}")
        for table in self.tables.values():
            print(table)

def main():
    # student table setup
    students_table = Table("Student")
    students_table.rows.append({"name": "John", "age": 18, "gpa": 3.5})
    students_table.rows.append({"name": "Jane", "age": 19, "gpa": 3.8})
    students_table.rows.append({"name": "Bob", "age": 20, "gpa": 3.2})
    students_table.rows.append({"name": "Alice", "age": 18, "gpa": 3.9})    
    students_table.rows.append({"name": "Joe", "age": 19, "gpa": 3.7})

    # student2 table setup
    students_table2 = Table("Student2")
    students_table2.rows.append({"name": "John", "age": 18, "gpa": 3.5})
    students_table2.rows.append({"name": "Jane", "age": 21, "gpa": 3.4})  
    students_table2.rows.append({"name": "Bob", "age": 20, "gpa": 3.2})   
    students_table2.rows.append({"name": "Eve", "age": 22, "gpa": 3.9})   
    students_table2.rows.append({"name": "Chris", "age": 19, "gpa": 3.1}) 

    # enrollment table setup
    enrollment_table = Table("Enrollment")
    enrollment_table.rows.append({"name": "John", "course": "Math101"})
    enrollment_table.rows.append({"name": "Jane", "course": "History202"})
    enrollment_table.rows.append({"name": "Alice", "course": "English105"})
    enrollment_table.rows.append({"name": "Bill", "course": "Math101"})
    enrollment_table.rows.append({"name": "Joe", "course": "Physics101"})
    parser = CommandParser()
    parser.tables["Student"] = students_table
    parser.tables["Student2"] = students_table2
    parser.tables["Enrollment"] = enrollment_table
    
    print("===============================================================================================================================================================")
    print("=====================================================WELCOME TO THE RELATIONAL ALGEBRA COMMAND LINE TOOL!======================================================")
    print("===============================================================================================================================================================")

    print("Example Unary Commands: ")
    print("(Student)project[name,age] --> PROJECTION")
    print("(Enrollment)select[name=John] --> SELECTION\n")

    print("Example Set Commands: ")
    print("(Student)U(Enrollment) --> UNION")
    print("(Student)&(Enrollment) --> INTERSECTION")
    print("(Student)-(Enrollment) --> DIFFERENCE\n")

    print("Example Binary Commands: ")
    print("(Student)join[name=name](Enrollment) --> INNER JOIN(NATURAL JOIN)")
    print("(Student)join-[name=name](Enrollment) --> RIGHT JOIN")
    print("(Student)-join[name=name](Enrollment) --> LEFT JOIN")
    print("(Student)-join-[name=name](Enrollment) --> FULL JOIN")
    print("(Student)x(Enrollment) --> CARTESIAN PRODUCT\n")


    print("Non Relational Algebra Commands: create, print_all, print(table_name)\n")

    print("Structure your create command like this:")
    print("create <table_name> {        <<ENTER>>")
    print("<column_name>, <column_name> <<ENTER>>")
    print("<value>, <value>             <<ENTER>>")
    print("}                            <<ENTER>>")

    while True:

        command = input("Enter your command (or type 'exit' to quit): \n")

        if command == 'exit':
            break

        elif command.startswith("create "):
            # gather all lines of the create command
            lines = [command]
        
            while not lines[-1].strip().endswith("}"):
                lines.append(input())
            command = '\n'.join(lines)
            result = parser._handle_create(command)
            print(result)
            continue

        elif command.startswith("print_all"):
            parser.print_tables()
            continue

        elif command.startswith("print"):
            table_name = command.split("(")[1].strip(")")
            parser.print(table_name)
            continue

        result = parser.execute(command)

        print(result)

if __name__ == "__main__":
    main()

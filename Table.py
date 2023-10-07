class Table:
    # Constructor (name of table, a list of rows(dictionaries))))
    def __init__(self, name = None, rows = None):
        self.name = name
        self.rows = rows if rows is not None else []
    
    # SELECTION(SIGMA (σ)) rows from table (this function returns a new table with rows that satisfy the condition(a lambda function))
    def select(self, column_name, operator, value):
        operators_map = {
            "=": lambda row_val: row_val == value,
            ">": lambda row_val: row_val > value,
            "<": lambda row_val: row_val < value,
            "!=": lambda row_val: row_val != value,
            "<=": lambda row_val: row_val <= value,
            ">=": lambda row_val: row_val >= value
        }

        if operator not in operators_map:
            print(f"Error: operator {operator} not supported")
            exit(1)

        table_select = Table(self.name + "_selected")

        for row in self.rows:
            if operators_map[operator](row[column_name]):
                table_select.rows.append(row)
            
        return table_select

    # PROJECTION(PI (π)) - returns selected columns - *columns basically allows you to pass multiple arguments
    def project(self, *columns):
        # Create a new list for the new table
        project_table = Table(self.name + "_projected")

        # Loop through each row in Table
        for row in self.rows:
            # Create a new dictionary to store the selected columns
            projected_row = {}

            # Loop through each column in columns
            for col in columns:
                # Add column to projected_row dictionary
                projected_row[col] = row[col]
            
            # Add the projected row(dictionary) to the table
            project_table.rows.append(projected_row)
        
        return project_table
    
    # Cartesian Product (X) - returns a new table with every row from this table combined with every row from the other table
    def cartesian_product(self, other_table):
        # create product table
        product_table = Table(self.name + "_x_" + other_table.name)
        
        # loop through each row(dictionary) in self_table
        for self_row in self.rows:
            # loop through each row in other_table
            for other_row in other_table.rows:
                # create a new dict to store the combined rows
                product_row_dict = {}
                # add each col(key value pair) from self_row
                for col in self_row:
                    product_row_dict[col] = self_row[col]
                # add each col(key value pair) from other_row only if it is not there yet(meaning the two tables have the same column name)
                for col in other_row:
                    if col not in product_row_dict:
                        product_row_dict[col] = other_row[col]
                    else:
                        product_row_dict[col + "_B"] = other_row[col]
                # add the combined row to the product table
                product_table.rows.append(product_row_dict)
        
        return product_table

    # Join (⋈) - uses cartesian product and selection to return a new table with unique rows that have a match in the other table
    # MAYBE SHOULD HAVE NOT USED CARTESIAN PRODUCT BUT TOO LATE NOW (GOT IT FROM THE LECTURES)
    def inner_join(self, other_table, self_column, other_column):
        # create a new table for the results
        join_table = Table(self.name + "_join_" + other_table.name)

        # loop through each row of self
        for row in self.rows:
            # loop through the rows in other_table
            for other_row in other_table.rows:
                # check if self_column and other_column have matching values
                if row[self_column] == other_row[other_column]:
                    # create a new dict to store the combined rows
                    join_row = dict(row)
                    
                    # Update the join row with the data from the other row
                    join_row.update(other_row)
                    
                    # add the new row to the join table
                    join_table.rows.append(join_row)

                    # Break out of the inner loop as we found a match
                    break

        return join_table

    # Left Join (⋉) - return a new table with all rows from self_table and only matching rows from other_table
    # this can handle if joining on same column name bc of the update function for dictionaries
    def left_join(self, other_table, self_column, other_column):
        # create a new table for the results
        join_table = Table(self.name + "_-join_" + other_table.name)
        
        # loop through each row of the product table
        for row in self.rows:

            #create a new dict to store the combined rows
            join_row = dict(row)

            #matched flag
            matched = False

            #loop through the rows in the other_table
            for other_row in other_table.rows:
                #check if self_column and other_column have matching values
                if row[self_column] == other_row[other_column]:
                    # set matched flag to true
                    matched = True
                    # add the other_row to the join_row
                    join_row.update(other_row)
                    break

            # if no match add None only to the 'other' columns
            if not matched:
                for col in other_table.rows[0]:
                    if col not in join_row:
                        join_row[col] = None

            # add the new row to the join table
            join_table.rows.append(join_row)
        
        return join_table

    # Right Join (⋊) - return a new table with all rows from other_table and only matching rows from self_table
    # USED LEFT JOIN AND SWITCHED THE TABLES
    def right_join(self, other_table, self_column, other_column):
        right_join_table = other_table.left_join(self, other_column, self_column)
        right_join_table.name = self.name + "_join-_" + other_table.name 
        return right_join_table

    # Full Join (⋈) - return a new table with all rows from both tables and NULL for any unmatched rows
    #USED LEFT JOIN AND ADDED THE REST FROM THE OTHER TABLE
    def full_join(self, other_table, self_column, other_column):
        left_join_table = self.left_join(other_table, self_column, other_column)
        right_join_table = self.right_join(other_table, self_column, other_column)

        # loop through each row in right joined table and add rows that are not in the left joined table
        for row in right_join_table.rows:
            # check if the dictionary is present in the list of dictionaries
            if row not in left_join_table.rows:
                left_join_table.rows.append(row) 

        left_join_table.name = self.name + "_-join-_" + other_table.name
        full_join_table = left_join_table # not necessary but just to be clear
        return full_join_table
    
    def intersection(self, other_table):
        #check if attrubutes(column names) are the same for compatibility issues
        if set(self.rows[0].keys()) != set(other_table.rows[0].keys()): # convert to sets because table might have the same column names but different order
            print("Error: tables are not compatible for intersection")
            return None

        # create new table for results
        intersection_table = Table(self.name + "_intersection_" + other_table.name)

        # loop through each row in self_table and check if it is in other_table
        for self_row in self.rows:
            for other_row in other_table.rows:
                if self_row == other_row:
                    #add it
                    intersection_table.rows.append(self_row)
                    break
        
        return intersection_table
    
    def union(self, other_table):
        # check for attribute compatibility
        if set(self.rows[0].keys()) != set(other_table.rows[0].keys()): # Convert to sets for column name order compatibility
            print("Error: tables are not compatible for union")
            return None

        # create new table for results
        union_table = Table(self.name + "_union_" + other_table.name)

        # add all rows from the self table
        for row in self.rows:
            union_table.rows.append(row)

        # add rows from the other table if they aren't in the union already
        for other_row in other_table.rows:
            if other_row not in union_table.rows:
                union_table.rows.append(other_row)

        return union_table

    def difference(self, other_table):
        # Check for attribute compatibility
        if set(self.rows[0].keys()) != set(other_table.rows[0].keys()):  # Convert to sets for column name order compatibility
            print("Error: tables are not compatible for minus operation")
            return None

        # Create new table for results
        difference_table = Table(self.name + "_minus_" + other_table.name)

        # Add rows from the self table if they aren't in the other table
        for self_row in self.rows:
            if self_row not in other_table.rows:
                difference_table.rows.append(self_row)

        return difference_table

    def __str__(self) -> str:
        if not self.rows:
            return f"Table: {self.name} (Empty)"

        # extract headers (assuming all rows have the same keys)
        headers = list(self.rows[0].keys())

        # determine the maximum width for each column
        col_widths = {}
        for header in headers:
            max_width = len(header)  # start with the header's length
            for row in self.rows:
                value = row[header]
                if value is None:
                    value_str = 'NULL'
                else:
                    value_str = str(value)
                max_width = max(max_width, len(value_str))
            col_widths[header] = max_width

        # create a formatting string for the rows
        format_strings = []
        for col in headers:
            format_strings.append("{:" + str(col_widths[col]) + "}")
        row_format = " | ".join(format_strings)

        # prepare header line
        table_str = f"Table: {self.name}\n"
        table_str += row_format.format(*headers) + "\n"
        separator = "-+-".join(["-" * col_widths[col] for col in headers])
        table_str += separator + "\n"

        # add each row
        for row in self.rows:
            formatted_values = []
            for col in headers:
                value = row[col]
                if value is None:
                    formatted_values.append('NULL')
                else:
                    formatted_values.append(str(value))
            table_str += row_format.format(*formatted_values) + "\n"

        return table_str
    

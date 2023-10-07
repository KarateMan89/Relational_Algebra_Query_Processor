Relational Algebra Query Processor
A command-line tool implemented in Python that allows users to perform relational algebra operations like set operations, projections, and joins on tables.

YouTube explanation:
https://youtu.be/qb_AOPo0_R4

Features
Unary Operations: Supports projection (project) and selection (select) operations.
Set Operations: Includes union (U), intersection (&), and difference (-) operations.
Binary Operations: Features Cartesian product (x), inner join, left join, right join, and full join.
Table Creation: Allows users to dynamically create tables.
Pretty Printing: Displays tables in a user-friendly format.

Getting Started

Navigate to the project directory:
cd RelationalAlgebraQueryProcessor

Run the program:
python CommandParser.py
Follow the on-screen prompts to input your commands and query tables.

Example Commands
(Student)project[name, age]
((Student)select[age=18])project[name]

For more examples, see the guide within the tool.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

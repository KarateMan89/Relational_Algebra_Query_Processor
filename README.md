# Relational Algebra Query Processor

## Description
The Relational Algebra Query Processor is a command-line tool written in Python. It enables users to perform relational algebra operations like set operations, projections, and joins on tables.

## Features
- **Unary Operations**: Supports projection (`project`) and selection (`select`).
- **Set Operations**: Perform union (`U`), intersection (`&`), and difference (`-`).
- **Binary Operations**: Includes Cartesian product (`x`), inner join, left join, right join, and full join.
- **Table Creation**: Dynamically create tables.
- **Pretty Printing**: User-friendly table display.

## Getting Started

### Prerequisites
- Python installed on your system.

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/RelationalAlgebraQueryProcessor.git
   ```
2. Navigate to the project directory:
   ```
   cd RelationalAlgebraQueryProcessor
   ```

### Usage
Run the program:
```
python CommandParser.py
```
Follow the on-screen prompts to input your commands and query tables.

### Example Commands
- Projection: `(Student)project[name, age]`
- Selection and Projection: `((Student)select[age=18])project[name]`

For more examples, check out the guide within the tool.

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## Resources
- [YouTube Explanation](https://youtu.be/qb_AOPo0_R4)

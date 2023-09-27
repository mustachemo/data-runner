# Data Clean-up Tool

## Table of Contents

- [Setup](#setup)
- [Featires](#features)
- [Problem(s)](#problem)
- [Objectives](#objectives)


## Setup

To set up and run the Data Clean-up Tool, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/mustachemo/data-runners.git
   ```

2. Change to the project directory:

  ```bash
  cd data-cleanup-tool
  ```

3. Create a conda environment from the provided environment.yml file:

  ```bash
  conda env create -f environment.yml
  ```

4. Activate the newly created conda environment:

  ```bash
  conda activate data_cleanup_env
  ```

5. **Run the Application:**

   - Open a terminal and execute the following command:
   
     ```bash
     python run.py
     ```

   - **OR**

   - Open the command palette by pressing `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac).

   - Type "Run Task" and select "Tasks: Run Task" from the dropdown list.

   - Alternatively, you can use the keyboard shortcut `Ctrl+Shift+B` (Windows/Linux) or `Cmd+Shift+B` (Mac).

## Features

  - [x] Upload button to upload various forms of data 
    - [ ] Style the button to make it look nice
  - [x] Display the data in a table
  - [x] All columns are displayed and are scrollable
  - [x] Up to 259 rows are displayed and are scrollable. Rest of data is cycled through pages system
  - [ ] Export data into various forms
    - [ ] We are able to export the data, but not the modified data. Must fix that
    - [ ] Also need to make a button that exports the data into the format specified by the radio buttons
## Problem

The presence of large amounts of bad data which does not comply with the required format, currently not relevant and that has been entered into the warehouse management system (WMS) incorrectly and cannot be utilized for any purpose. This data always causes hinderance in many daily activities, become hurdles when the company transitions to a new WMS and most importantly occupies huge amounts of memory in the server systems. A tool which can help identify this bad data, modify it to required format and delete gaps, if necessary, can help resolve many of the forementioned issues.

## Objectives 

Objective is to design and function tool that can help the company to identify and delete, modify, fix this bad data, gaps in data, and eliminate a large amount as per user requirement. This will reduce manual work related to fixing this bad data.

- Standard Features:

  - [x] Ability to read various formats of data (xml, csv, pdf etc.;) and display in rows and columns.
  - [ ] Give the user the ability to define each row or column of data according to the user’s preference. And modify or
display the data that is not according to the defined parameters. Preferably in GUI for a layman to use it.
  - [ ] Combine different sets of data of same format into one set and customize as per user requirements.
  - [x] Ability to export into different formats as per user needs.

- Bonus Features:

  - [ ] Identify duplicate data in different formats, errors such as wrong address format, punctuation, spellings, and
address styles. Filter the data and display the rows and columns with these discrepancies.
  - [ ] Creating visuals from the data.


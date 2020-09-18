
## Initial setup

1. Clone this repo and cd to the grading directory

2. Install the contents of requirements.txt
    - Run ```python3 -m pip install -r requirements.txt```
        - This command may be slightly different based on your system

3. Clone the data repository into `data/` (clone at this level and rename if needed).
    - For Summer 2020:
    ```
        git clone https://github.iu.edu/CSCI-C200-Support/summer_20_data.git data
    ```
    
4. Setup the personal configs
    - Run config_editor to create a config file and fill in appropriate values
    ``` 
        cd config       
        python3 config_editor.py
    ```
    - The name you enter for yourself should match the spelling in code/cloner/MasterListAssignments.xlsx
5. Run `main.py` in the gui folder. Further instructions can be found in the gui by clicking menu -> help
    ```
        cd ../gui
        python3 main.py
    ```

### TL;DR

1. cd gui
2. python3 main.py
3. Grade
4. Put scores in to Canvas
5. Commit and push grading reports

## Grading

Note: if you are grading for the second time, you will already have a repos folder from last week. In this case, what you should do is just delete the tempdata folder, and re- run getRepos.py (from the code/cloner or in the gui). This will get your new people to grade. 

To grade, simply cd to gui, and run main.py to use the GUI. Test each student's code, and fill out the .tex file on the right with their score and appropriate comments. If they got everything right, leave a positive message such as 'Good Job!' and if you take off points, explain why. Total up each section and their final grade. Once you are done with all your grading, you can press 'Export CSV' in the GUI to download the scores to your desktop. Either upload these scores (checking to be sure the result looks right) or enter the scores into canvas manually. Then commit and push your grade reports. 

``` 
    cd config
    python3 config_editor.py #Change to assignment number you are grading
    cd ../gui
    python3 main.py
    ... After finishing with the gui ...
    cd ../data
    git status #Check that you won't be committing anything besides the reports
    git add .
    git commit -m "finished grading" 
    git push
```

Note on committing. You will be committing the reports to this repository, not directly to the student's repos. 

## Helpful information

- The student repos are located in tempdata/repos/
- The tex files are locoated in data/fragments/{username}
- You can just delete the whole tempdata folder when you are done

## Writing test cases.

Some info [here](./docs/solutionFiles.md)

## TODO
- [ ] Report compilation process update
- [ ] make fragment template copy script pull assigned and due dates from metadata file
- [ ] Fix csv script
- [ ] Prevent old reports from getting overwritten? 
- [ ] Say done in idle window when cloning scripts are done
- [ ] Autogenerate correct section names - Logan
- [ ] Create framework for operating on all repos/ subfolders
- [ ] Specify test case points (also counts?) in assignment template file
- [ ] Better handling on setup section for grading report
- [ ] Take a look at autosaving scores when changed
- [ ] Put name of actual grader in assignment metadata file
- [ ] Show students directory contents in student code section of Structuring Problem
- [ ] Specify Custom handlers in testValues file to handle post run data gathering/ comparison
- [ ] autograder- provide more context to why stuff fails
- [ ] capture print statements
- [ ] Generate test values file (format) automatically (grab all functions, number of parameters from each solution file, create empty dictionaries)


- [x] Finish reprt writer
- [x] Test cases write results to fragments yaml file
- [x] Generate fragments yaml file off of reports yaml file
- [x] Update gui to have boxes for filling in info
- [x] Test cases output
- [x] Deploy report wrapper tex files
- [x] Add button to gui for generating tex/ compiling pdfs
- [x] Add button to open current student directory


## Issues
- [x] setup repos not starting scripts until you click okay (might be intended) (was intended, if popup is not blocking then it disappears under the idle windows; the popup must be shown and read once since it contains important information)
- [ ] Gui doesn't run the first time if the config file hasn't been edited

## UI stuff:
- Make tabs be spaces
- Verify that score calculation works
- Make 'Grader configuration' menu shortcut more clear
- Update help dialog
- Show solution file as tab between student submission and solution
- Run solution file separately to see output
- Show problem total points next to top 0/+ buttons
- Add grade fragment part for additional additions/deductions

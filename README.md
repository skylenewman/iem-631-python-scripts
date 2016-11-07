# IEM 631 Project

* **addDiffs.py** Added time diffs to the SANITIZED CSV file.
* **split.py** broke the large CSV into smaller files related to the workflow instance they represented.
* **buildUserGroupDict** read a users/groups file into a dictionary for use to add user information to other files.
* **buildTypeIndexes.py** built indexes of different categories of files. The categories include:
  * Workflow Type
  * Workflow Initiation/Completion Day/Month/Year
  * Duration
  * Users Assigned
  * Complete/Incomplete Workflows
* **buildJsonFromWorkflows.py** converted the smaller CSV files into JSON files and added relationships.
* **buildJsonFromIndices.py** looped through all the files referenced by index files, performed analysis, and wrote a JSON file with values.
* **step2.py** deprecated script that lists different columns in sanitized CSV.
* **printStatuses.py** helper script that was used (mostly) to view different columns of data. The current version is creating an index of *all* workflows.
* **splitAndIndex.py** (deprecated)

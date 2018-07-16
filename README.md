# M2- Test Analysis milestone

## Names:

- Bhushan Thakur (bvthakur)
- Kiran Krishnan Balakrishnan (kbalakr)
- Rohit Nambisan (rnambis)
- Vishal Kumar Seshagirirao Anil (vseshag)

## Screencasts

DevOps M2: Fuzzer, Useless tests, Test Coverage & Analysis Component: https://youtu.be/UuxY58LuYTA

DevOps M2 - 100 iterations of fuzzing: https://youtu.be/nPyrQJNt-z8

## Procedure:

#### Jenkins post installation setup

  Installing Jenkins and dependencies for the same was done using the ansible playbook from milestone M1. The additional thing we had to do was to install different jenkins plugin required for the projects. Plugins such as Jacoco, test-stability and text-finder installation is automated in the jenkins deployment .Once installation is done, jobs are setup in jenkins using the job.yml. The jobs setup in jenkins are as follows,
  - checkbox_build - Runs the checkbox analysis component
  - itrust_job1 - Clones the git repo containing iTrust application in the machine running jenkins and runs the fuzzer. The       post-commit hook triggers the itrust_job2 where tests are running.
  - itrust_job2 - Builds the itrust package and runs tests. Also, test coverage report is generated.


#### Checkbox - Analysis Component
We used javascript esprima parser for analyzing the source code and generate the abstract syntax tree. This AST generated was traversed using visitor pattern, essentially allowing us to get the necessary information required to compute the lines of code, bigO, messageChains and syncCalls. The following report shows the analysis for the server-side checkbox.io code.
The constraints were loc > 120 , syncCalls > 1, messageChains >3 and BigO >3.

```
../site/marqdown.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

loadJadeTemplates(): 32
============
LinesOfCode: 25	SyncCalls: 8	messageChains: 2	BigO: 0


testFile(): 59
============
LinesOfCode: 26	SyncCalls: 0	messageChains: 2	BigO: 0


ReadHeader(): 86
============
LinesOfCode: 13	SyncCalls: 0	messageChains: 2	BigO: 1


ReadBody(): 100
============
LinesOfCode: 19	SyncCalls: 0	messageChains: 2	BigO: 1


EscapeCode(): 120
============
LinesOfCode: 16	SyncCalls: 0	messageChains: 1	BigO: 0


ProcessTokens(): 137
============
LinesOfCode: 233	SyncCalls: 0	messageChains: 3	BigO: 3


processInnerText(): 371
============
LinesOfCode: 23	SyncCalls: 0	messageChains: 3	BigO: 1


../site/server.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

../site/routes/admin.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

../site/routes/create.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

basicCreate(): 73
============
LinesOfCode: 30	SyncCalls: 0	messageChains: 2	BigO: 0


sendStudyEmail(): 104
============
LinesOfCode: 8	SyncCalls: 0	messageChains: 2	BigO: 0


../site/routes/csv.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

formatJsonAsCSV(): 3
============
LinesOfCode: 72	SyncCalls: 0	messageChains: 3	BigO: 3


sizeOfRow(): 77
============
LinesOfCode: 48	SyncCalls: 0	messageChains: 3	BigO: 3


../site/routes/designer.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

../site/routes/live.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

../site/routes/study.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

commonSubmit(): 188
============
LinesOfCode: 16	SyncCalls: 0	messageChains: 2	BigO: 0


../site/routes/studyModel.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

surrogateCtor(): 4
============
LinesOfCode: 1	SyncCalls: 0	messageChains: 1	BigO: 0


extend(): 6
============
LinesOfCode: 8	SyncCalls: 0	messageChains: 3	BigO: 0


../site/routes/upload.js
~~~~~~~~~~~~
ImportCount 0	Strings 0

readFileStream(): 50
============
LinesOfCode: 32	SyncCalls: 0	messageChains: 2	BigO: 0


readFile(): 83
============
LinesOfCode: 9	SyncCalls: 0	messageChains: 3	BigO: 0


uploadFile(): 93
============
LinesOfCode: 32	SyncCalls: 0	messageChains: 3	BigO: 0

```

The tests failed at
```
loadJadeTemplates(): 32
============
LinesOfCode: 25	SyncCalls: 8	messageChains: 2	BigO: 0

ProcessTokens(): 137
============
LinesOfCode: 233	SyncCalls: 0	messageChains: 3	BigO: 3

```
#### Fuzzer (fuzzer.py)
  
  A python script to automate commit fuzzing. The following fuzzing operations were done.
  - change content of "strings" in code.
  - swap "<" with ">"
  - swap "==" with "!="
  - swap 0 with 1
  
  Initially, a branch called fuzzer was created. The python script does random fuzzing operations in this branch. Then the branch is committed which initiates a post commit hook. This inturn triggers the jenkins itrust_job2. After each build in jenkins, a rollback is effectively handled. Once required number of iterations are run, the useless test detector is called. 

#### Useless test detector (useless.py)

  A python script is used to implement the useless test detector. Once the fuzzing iterations are done, the build logs of each build are compared based on failed and passed tests. A test is rendered useless if a test passes in all the fuzzing iterations. All the tests within the main test suites are considered.
  
#### Coverage Report

Junit test reportting along with the Jacoco plugin is made use of to see the detailed test coverage report in jenkins. (It is explained in the screencast)

## Screenshots
#### Useless tests report (at the end of itrust_job1 for 100 iterations of fuzzing)
![useless_table](https://media.github.ncsu.edu/user/8297/files/87abc33a-b8fa-11e7-9e18-75be8bd3e047)

#### Useless tests report (showing useless test count for 100 iterations of fuzzing)
![useless_results_100](https://media.github.ncsu.edu/user/8297/files/a4dd5f90-b8fa-11e7-8a46-a49a0e2dab38)

#### One fuzzing run in itrust_job1
![explain_each_iteration_fuzzer](https://media.github.ncsu.edu/user/8297/files/d5ce1e00-b8fa-11e7-95a8-398b5f77421c)

#### Jacoco tests suite 
![jacoco](https://media.github.ncsu.edu/user/6283/files/6355a7ce-b906-11e7-9da4-4a028f6f64ba)
![jacoco1](https://media.github.ncsu.edu/user/6283/files/a9beba20-b906-11e7-9e48-6e46b5c4c5d6)

#### number of useless tests detected across 100 builds

![passing builds in 100 builds](https://media.github.ncsu.edu/user/6147/files/d7dbea74-c33b-11e7-8689-c91f5afb15d1)


## Contribution

  Bhushan Thakur - Analysis component for Checkbox.io and Jenkins Setup</br>
  Kiran Krishnan Balakrishnan - Fuzzer.py and git hook to trigger jenkins build </br>
  Rohit Nambisan - Fuzzer.py and git hook to trigger jenkins build </br>
  Vishal Kumar Seshigirirao Anil - Useless test detector and Jenkins Setup </br>





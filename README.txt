INSTRUCTIONS
-------------------------------------------------------------------------------------

1) Download and install Python from here :https://www.python.org/download/releases/3.4.1/
   Please note that DistAlgo works only for Python 3.4.1 and above. So, download and install Python 3.4.1 and above

2) Download and unzip DistAlgo from here: http://sourceforge.net/projects/distalgo/files/. The root folder is henceforth 	
   referred to as <DISTALGO_ROOT>

3) Install DistAlgo by opening a command prompt and forllowing the instructions in <DISTALGO_ROOT>

4) Navigate to the <PROJECT_ROOT>/src/ folder.
   Compile and execute the Bank Replication code by running the commands in command prompt:
	dac server.da
	dac client.da
	dac serverManager.da
	dar -f testApp.da <CONFIG_FILE_NAME>

The testcases are located in <PROJECT_ROOT>/config/ folder, namely chain_app_1.cfg,chain_app_2.cfg,etc. You can run the chain_app_1.cfg testcase by substituting the configuration file name in the last command above like this:
	dar -f testApp.da "chain_app_1.cfg"

MAIN FILES
--------------------------------------------------------------------------------------

Server: <PROJECT_ROOT>/src/server.da
Master: <PROJECT_ROOT>/src/master.da
Client: <PROJECT_ROOT>/src/client.da
TestApp:<PROJECT_ROOT>/src/testApp.da
ServerManager : <PROJECT_ROOT>/src/serverManager.da
ActionProcess : <PROJECT_ROOT>/src/actionprocess.da

BUGS AND LIMITATIONS
---------------------------------------------------------------------------------------


LANGUAGE COMPARISON
===================

Code Size Comparison:
---------------------
	Distalgo took relatively lesser code size to accomplish the same functionalities achieved in erlang
	In fact Distalgo took only 1/3rd of the code size of erlang

-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Erlang                           9            301            305           1867
-------------------------------------------------------------------------------
SUM:                             9            301            305           1867
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
DistAlgo                         6            117            114            655
-------------------------------------------------------------------------------
SUM:                             6            117            114            655
-------------------------------------------------------------------------------

Time and Effort to code:
------------------------
	Both erlang and distalgo follows similar flow patterns
	Erlang took relatively longer time to develop the initial code ( 5 days)
	With distalgo we were able to complete the modules faster ( 3 days) though initially we struggled in finding syntactic errors

Time and Effort to debug:
------------------------
	Erlang was better in terms of debugging ( due to the clarity of log prints and atomicity of print statements)
	Debugging was difficult with distalgo ( due to lack of IDE and noisy log prints)
	 
Strength and Weakness:
----------------------
	One of the major difficulty with erlang is its state management.
	Distalgo using the advantage of python has better state management
	Many complex operations in erlang was easily achieved in distalgo, thanks to python
	Yield points in distalgo made tasks easier for concurrently receiving msgs while looping
	
Readability of code:
--------------------
	Erlang is bit hard for new learners to adapt to its flows like state management, for loops with accumulators
	Distalgo using python makes code readable even for beginners
	
Similarity to pseudocode
------------------------
	Erlang and distalgo almost looks similar to the pseudocode we developed, as they have same paradigm and the pseudocode was
		written keeping erlang as reference
	Distaglo is again the winner here, as it resembles almost equivalent to our pseudocode


CONTRIBUTIONS
---------------------------------------------------------------------------------------
Ashwin Giridharan (109930400) - Developed the core DistAlgo modules (Server, Master, Client, Configurations, Testing, Validating)
								- Failure detection modules by master ( Head, Tail, Mid)
								- Failure handling modules by master ( Head, Tail, Mid, S- crash, S+ crash)
								- Chain Extension ( Normal, Old Tail Crash, New Tail Crash)
								- Propagation of sent requests, bank users map, transactions map
								- Message loss simulation in server
								- Configuration management ( Creating cfg files for all test scenarios)
								- Client failure handling and resend logics
								- Debugging, 
								- Testing, 
								- Logging, 
								- Code comments


Balaji Srinivasan (109969253) - Developed 
								- Message resending by client
								- Server - Master pinger
								- Timer module for checking failed servers
							  - Assisted
								- Verifying end to end flow for all the test cases
								- Failure detection by master
								- Failure handling of head and tail crashes
								- Server suffix list propagation
								- Configuration management ( creating test cfg files)

OTHER COMMENTS
---------------------------------------------------------------------------------------



	
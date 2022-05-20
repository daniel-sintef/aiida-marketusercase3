This is a very simple demo for the 'flame' model for Fluent. Formally known as model1 & model 2.

This plugin currently consists of the 'marketusercase3' CalcJob which takes in 4 inputs:
* Code [code]
* SingleFileData [cas_file]
* SingleFileData [dat_file]
* Dict [user_inputs]

In the ./examples/ directory we include everything for a trial run: 

* example_run.ipynb A jupyter notebook that works through a test example
* example_input A directory that contains cas/dat files, for input into the code, see example_run for how to import 
* exmaple_output A directory containing dummy output from a prior Fluent run, useful for testing
* run_model3.sh A very simple bash script suitable for using a 'dummy' code for installation 
                
Further details can be found in the example_run.ipynb ...



This code provides graphlet counts for all the edges for the given graph.

Compile: makefile is provided for compilation of the code. It needs c++ compiler and openMP support for the c++.
$ make

Run: make command creates output file "omp_graphlet_count_5".
$ ./omp_graphlet_count_5 -i input_graph_filename [-edgefile <edgelist_filename>] [-EdgeAtt] [-t #threads] [-local/-unique/-all]

options:
-i : With this option next argument should be input_graph_filename.
	Format: First row specify "#nodes #edges". 
		From the 2nd row, each row specify an edge in space delimited format: "node_id1 node_id2".
		Node_id need to be integer and starting node_id is 0.

-edgefile : With this option next argument should be edgelist_filename.	E-CLoG will return graphlet counts for this set of edges.
	Format: First row of the file specify #edges (number of edges in the file).
		From the 2nd row, each row specify an edge in space delimited format: "node_id1 node_id2".
		Node_id need to be integer and starting node_id is 0.
	Note: Order of the edges is not maintian in output file.



-EdgeAtt : This option specify the input format of the graph_file. If the "input_graph_file" has 3rd column specifying some edge attribute, with this flag it can read the file, however during graphlet counting our method ignore the value of the attribute.
	Format: First row specify "#nodes #edges #attribVals". 
		From the 2nd row, each row specify an edge in space delimited format: "node_id1 node_id2 attrib_val".
		Node_id need to be integer and starting node_id is 0.

-t : with '-t' flag provide number of threads (#threads (int)), program will try to get #threads based on availability on the host machine. 
-local : this option provide counts of all local graphlets. (Not Local: g3,g7,g12,g19) [Default]
-unique : this option provide counts of all graphlts structures (ignoring the orbit) only once to calculate global graphlet count.
-all: this option provide counts of all graphlts shown in the figures.




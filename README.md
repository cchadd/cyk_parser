### Use the parser
In order to use the parser, please launch 
`./run.sh`

The `run` file contains the command line `python script/main.py -s test_sentence.txt -p parser/cyk_parser -f parsed_sentences` which takes the following arguments

- `-s` the path to the set of sentences you want to parse (1 sentence per line with exactly 1 whitespace between each token)
- `-p` the path to the parser you want to use 
- `-f` the path to the file in which you want to store the parsed sentences (it will create a [`.txt`] file)

The output of the parser will take the following form:


`(SENT (NP|<NPP-Srel> (DET Le) (AP|<ADJ-PP> (ADJ petit) (NP (PRO chien) (AP|<VPpart-PONCT> (NP|<VN-NP> (VN|<V-VPP> (V est) (VPP parti)) (NP|<P-DET> (P sans) (NP|<DET-NC> (DET son) (NC maitre)))) (PONCT .))))))` 

for an given input sentence

`Le petit chien est parti sans son maitre .` 


### Other folders

- The `parser` folder contains the parser I created in `.pkl` format
- The `script` folder contains any piece of code to create, train and use the parser
- The `data` folder contains the sequoia treebanks on which the training and testing has been performed

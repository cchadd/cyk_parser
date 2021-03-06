### Use the parser
In order to use the parser, please launch 
`./run.sh`

The `run` file contains the command line `python script/main.py -s test_sentence.txt -p parser/cyk_parser -f parsed_sentences` which takes the following arguments

- `-s` the path to the set of sentences you want to parse (1 sentence per line with exactly 1 whitespace between each token). You can directly modify the (`test_sentence.txt file`)
- `-p` the path to the parser you want to use 
- `-f` the path to the file in which you want to store the parsed sentences (it will create a [`.txt`] file)
- `-t`if you want to display the corresponding tree (optional)

The output of the parser will take the following form:


`(SENT (NP|<NPP-Srel> (DET Le) (AP|<ADJ-PP> (ADJ petit) (NP (PRO chien) (AP|<VPpart-PONCT> (NP|<VN-NP> (VN|<V-VPP> (V est) (VPP parti)) (NP|<P-DET> (P sans) (NP|<DET-NC> (DET son) (NC maitre)))) (PONCT .))))))` 

for an given input sentence

`Le petit chien est parti sans son maitre .` 

![alt text](https://github.com/cchadd/cyk_parser/data/blob/master/sample.png)




### Other folders

- The `parser` folder contains the parser I created in `.pkl` format
- The `script` folder contains any piece of code to create, train and use the parser
- The `data` folder contains:
  - the sequoia treebanks on which the training and testing has been performed
  - a set of sentences to parse
  - the output of the parser on such a set of sentences
  - the output of the parser to validate the training `evaluation_data.parser_output.txt`
  - a sample of the parser outcome in case you request to build the tree

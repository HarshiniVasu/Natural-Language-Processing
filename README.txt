
Programming language - python 2.7
CADE machine used for testing 'lab1-15.eng.utah.edu'

FILES:

'infoextract.py' is the python file for the information extraction main code.

'victim.py' is a sub module file that is called in infoextract.py.

We need to have the zipped stanford core nlp dependency folder in the same directory as other files. Stanford core nlp's latest version can be downloaded from the Internet. This folder will be unzipped when we run the shell script <infoextract.sh>. Please make sure the unzipped folder of stanford Core NLP is in the same directory.

'victim.txt' contains the synonyms related to terrorism.

'weapon.txt' contains the extracted weapons.

'onestory.txt' is the input file that contains one story for reference.

Time taken to execute the program

PROCEDURE TO RUN AND COMPILE THE PROGRAM:

Give the following command:

	./infoextract.sh <input-file>

Example:    ./infoextract.sh onestory.txt


The above lines will generate the following files and a folder,

 	stanford-corenlp-full-2017-06-09 (folder)
	<input-file>.templates (output file)







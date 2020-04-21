# FineLocator

#### Description

Baseline approach implementation for BLESER.
FineLocator is an approach to method-level bug localization. This technique retrieve information from input of bug report and source code and output a list of suspicious buggy method relevant to the bug report. 
Each words in bug report and methods of source code are regarded as documents and transferred into numeric vectors by word embedding (word2vec). The vector representation of a document is calculated as the product of vectors of all words in the document and their corresponding TFIDF values, considering the influence of each single word.
To address the representation sparseness problem caused by short-length methods, the methods are augmented by each other using 3 weighted scores of query expansion, including semantic similarity, temporal proximity and call dependency. The semantic similarity is described as the cosine similarity of method vectors. The temporal proximity is described as the time difference between the latest modified time of methods. The call dependency is described as length of the shortest call path of methods. At last, suspicious buggy methods are ranked by the cosine similarity of vectors of bug report and vectors of augmented methods.

#### Installation

For MacOS:
1. install GCC@8 (8.3) to use deeplearning4j.

2. install Java Understand (use python API).
   API doc: 
   /Applications/Understand.app/Contents/Resources/doc/manuals/python/understand.html
   /Applications/Understand.app/Contents/Resources/doc/manuals/pdf/understand.pdf  (From Page 323)
   
   Problem1: Understand sometimes occurs API License problem. Need to Reinstrall.
   
   Problem2: Using Understand in ubuntu system with instuction "./und …" to creade '.udb' file directly in directory "~/xxx/FineLocator/expRes/…" may failed. By now, my solution is to create '.udb' file in a parent directory like "~/xxx/" and move it to "~/xxx/FineLocator/expRes/…" later.

#### Instructions

1. use `mvn package` to package jar for "pt" and "word2vec".

   Problem: it will contain a lot of redundant dependency.

2. xxxx

3. xxxx

#### Contribution

1. Fork the repository
2. Create Feat_xxx branch
3. Commit your code
4. Create Pull Request

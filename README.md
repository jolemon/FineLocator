# FineLocator

## Description

Baseline approach implementation for [BLESER](https://github.com/chinalienming/iBug).

[FineLocator](https://www.sciencedirect.com/science/article/pii/S0950584919300436) is an approach to method-level bug localization. This technique retrieve information from input of bug report and source code and output a list of suspicious buggy method relevant to the bug report. 

Each words in bug report and methods of source code are regarded as documents and transferred into numeric vectors by word embedding (word2vec). The vector representation of a document is calculated as the product of vectors of all words in the document and their corresponding TFIDF values, considering the influence of each single word.

To address the representation sparseness problem caused by short-length methods, the methods are augmented by each other using 3 weighted scores of query expansion, including semantic similarity, temporal proximity and call dependency. The semantic similarity is described as the cosine similarity of method vectors. The temporal proximity is described as the time difference between the latest modified time of methods. The call dependency is described as length of the shortest call path of methods. At last, suspicious buggy methods are ranked by the cosine similarity of vectors of bug report and vectors of augmented methods.

## Requirement

On MacOS:

- Python3 (>=3.6)
- Java (JDK>=1.8)

- GCC@8 (8.3) for deeplearning4j.

-  [Java Understand](https://scitools.com/)

    > Need to purchase and install . FineLocator use python API of Understand.
    > API doc in the installation path of Understand: 
    > `Contents/Resources/doc/manuals/python/understand.html`
    > `Contents/Resources/doc/manuals/pdf/understand.pdf  (From Page 323)`
    >
    > Problem1: API License problem. Need to purchase original software or reinstall it.
    >
    > Problem2: `./und [option]`  in Ubuntu to creade `.udb` file directly in directory "`PATH_TO/FineLocator/expRes/…`" may failed. By now, my solution is to create `.udb` file in a parent directory like `~` and move it to result directory (i.e., "`PATH_TO/FineLocator/expRes/…`") later.

- Prepare dataset. By default, we use [Defects4J](http://github.com/rjust/Defects4J)  dataset, which consists of 5 open source Java project (i.e.,  Closure compiler (156 defects), Apache commonsmath (85 defects), Apache commons-lang (56 defects), Joda-Time (23 defects) and Mockito (22 defects)). 

  > Follow instructions in [Defects4J](http://github.com/rjust/Defects4J) to get complete dataset.
  >
    > Note : Taking into account the storage size of the dataset, the [Defects4J-dataset](https://github.com/chinalienming/Defects4J-dataset) in my github is not complete to run FineLocator. The reason is that it only include:
  >
    > ​	1) bug reports
  >
    > ​	2) the linked-buggyMethods(i.e., The file labeling real buggy methods corresponding to bug reports) 
  >
    > ​	3) the source code for each buggy version corresponding to the bug report
  >
    > It DOES NOT include "`.git`" directory for check out the latest modification time for each method in the code, which is a necessary for calculate temporal proximity in the query expansion of FineLocator.

## Instructions
1. `mvn package` to make jar for "pt" (bug report preprocessor) and "word2vec" (embedding model) if not exist.

   Problem: the "word2vec" jar may contain a lot of redundant dependency component for various OS.

2. Edit "`input.properties`" and "`run.sh`" for your specific configuration.

3. `run.sh ${proj}` to run FineLocator.

4. Get result in "`${expResDir}/final/${proj}`".

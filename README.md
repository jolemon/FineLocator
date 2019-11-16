# FineLocator

#### Description

Baseline method implementation FineLocator for iBug.

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
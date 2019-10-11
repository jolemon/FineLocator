package model;

import common.Common;
import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.FileSentenceIterator;
import org.deeplearning4j.text.sentenceiterator.SentenceIterator;
import org.deeplearning4j.text.tokenization.tokenizer.preprocessor.CommonPreprocessor;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedWriter;
import java.io.File;

public class Word2VecModel {

    private static Logger log = LoggerFactory.getLogger(Word2VecModel.class);

    public static void initModel(String dataDir, String modelSavePath){
        log.info("Load & Vectorize Sentences....");
        SentenceIterator iter = new FileSentenceIterator(new File(dataDir));
        // Split on white spaces in the line to get words
        TokenizerFactory t = new DefaultTokenizerFactory();
        t.setTokenPreProcessor(new CommonPreprocessor());

        log.info("Building model....");

        //using 'Skip-gram' model
        Word2Vec vec = new Word2Vec.Builder()
                .minWordFrequency(1)
                .iterations(1)   // ?
                .layerSize(300)  // 200-500 is acceptable
                .windowSize(5)
                .iterate(iter)
                .tokenizerFactory(t)
                .build();


        log.info("Fitting Word2Vec model....");
        vec.fit();

        log.info("Writing word vectors to text file....");

        // The normal way to save models in Deeplearning4j is via the serialization utils
        // (Java serialization is akin to Python pickling, converting an object into a series of bytes).
        WordVectorSerializer.writeWord2VecModel(vec, modelSavePath);
    }

    public static Word2Vec loadModel(String modelSavePath) {
        return WordVectorSerializer.readWord2VecModel(modelSavePath) ;
    }



    public static void main(String[] args) {

        String dataDir = "~/FineLocator/expRes/afterPT" ;
        String modelSavePath = Common.modelSavePath;

        Word2Vec word2Vec = loadModel(modelSavePath) ;

        // try to get vector by python...
        File dir = new File("/Users/lienming/FineLocator/expRes/vec/br/Closure");

        if(!dir.exists()) {
            dir.mkdirs();
        }
        File file = new File("/Users/lienming/FineLocator/expRes/afterPT/br/Closure/Closure_1") ;
        File saveFile = new File(dir.getPath(), file.getName());
        BufferedWriter out ;
//        try {
//            out = new BufferedWriter(new FileWriter(saveFile)) ;
//            String content = new String(Files.readAllBytes(file.toPath()));
//            System.out.println(content);
//            for(String word : content.split(" ")) {
//                INDArray wordVectorMatrix =word2Vec.getWordVectorMatrix(word);
//                if (wordVectorMatrix == null) {
//                    System.out.println(word);
//                } else {
//                    out.write(wordVectorMatrix.toString() + " not in the vocabulary.");
//                }
////                System.out.println(wordVectorMatrix);
//            }
//            out.flush();
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        INDArray wordVectorMatrix = word2Vec.getWordVectorMatrix("compil");
//        System.out.println(wordVectorMatrix);
    }



}

package model;

import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.FileSentenceIterator;
import org.deeplearning4j.text.sentenceiterator.SentenceIterator;
import org.deeplearning4j.text.sentenceiterator.SentencePreProcessor;
import org.deeplearning4j.text.tokenization.tokenizer.preprocessor.CommonPreprocessor;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;

public class Word2VecModel {

    private static Logger log = LoggerFactory.getLogger(Word2VecModel.class);

    public static Word2Vec initModel(String dataDir){
        log.info("Load & Vectorize Sentences....");
        SentenceIterator iter = new FileSentenceIterator(new File(dataDir));
        iter.setPreProcessor(new SentencePreProcessor() {
            @Override
            public String preProcess(String sentence) {
                sentence = sentence.replace("分","").trim().toLowerCase();
//                System.out.println(sentence);
                return sentence;
            }
        });

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
//        WordVectorSerializer.writeWord2VecModel(vec, modelSavePath);
        return vec ;
    }

    public static void saveModel(Word2Vec vec, String modelSavePath) {
        WordVectorSerializer.writeWord2VecModel(vec, modelSavePath);
    }

    public static Word2Vec loadModel(String modelSavePath) {
        return WordVectorSerializer.readWord2VecModel(modelSavePath) ;
    }


    /*
        PLEASE NOTE:
            after model is restored,
            it's still required to set SentenceIterator and TokenizerFactory,
            if you're going to train this model
    */
    public static void continueFit(Word2Vec word2Vec, String dataDir) {
        SentenceIterator iter = new FileSentenceIterator(new File(dataDir));

        TokenizerFactory t = new DefaultTokenizerFactory();
        t.setTokenPreProcessor(new CommonPreprocessor());
        word2Vec.setTokenizerFactory(t);
        word2Vec.setSentenceIterator(iter);

        log.info("Word2vec uptraining...");
        word2Vec.fit();
    }



}

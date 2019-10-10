package model;

import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.FileSentenceIterator;
import org.deeplearning4j.text.sentenceiterator.SentenceIterator;
import org.deeplearning4j.text.tokenization.tokenizer.preprocessor.CommonPreprocessor;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;

public class Word2VecModel {

    private static Logger log = LoggerFactory.getLogger(Word2VecModel.class);

    public static void main(String[] args) {
        log.info("Load & Vectorize Sentences....");
        SentenceIterator iter = new FileSentenceIterator(new File("/Users/lienming/FineLocator/expRes"));
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

        WordVectorSerializer.writeWord2VecModel(vec, "word2vec.model");


        Word2Vec word2Vec = WordVectorSerializer.readWord2VecModel("word2vec.model");
        INDArray wordVectorMatrix = word2Vec.getWordVectorMatrix("compil");
        System.out.println(wordVectorMatrix);
    }



}

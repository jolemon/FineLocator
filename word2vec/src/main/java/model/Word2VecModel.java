package model;

import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.BasicLineIterator;
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

    public static String dataLocalPath;


    public static void main(String[] args) throws Exception {

        dataLocalPath = DownloaderUtility.NLPDATA.Download();
        // Gets Path to Text file
        String filePath = new File(dataLocalPath,"raw_sentences.txt").getAbsolutePath();

        log.info("Load & Vectorize Sentences....");
        // Strip white space before and after for each line
//        SentenceIterator iter = new BasicLineIterator(filePath);
        SentenceIterator iter = new BasicLineIterator(new File("raw_sentences.txt"));

        // Split on white spaces in the line to get words
        TokenizerFactory t = new DefaultTokenizerFactory();

        /*
            CommonPreprocessor will apply the following regex to each token: [\d\.:,"'\(\)\[\]|/?!;]+
            So, effectively all numbers, punctuation symbols and some special symbols are stripped off.
            Additionally it forces lower case for all tokens.
         */
        t.setTokenPreProcessor(new CommonPreprocessor());

        log.info("Building model....");

        //using 'Skip-gram' model
        Word2Vec vec = new Word2Vec.Builder()
                .minWordFrequency(1)
                .iterations(1)   // ?
                .layerSize(300)  // 200-500 is acceptable
//                .seed(42)      // ?
                .windowSize(5)
                .iterate(iter)
                .tokenizerFactory(t)
                .build();

        log.info("Fitting Word2Vec model....");
        vec.fit();

        log.info("Writing word vectors to text file....");
        /*
            at this moment we're supposed to have model built, and it can be saved for future use.
         */
        WordVectorSerializer.writeWord2VecModel(vec, "pathToSaveModel.txt");

        /*
            Let's assume that some time passed, and now we have new corpus to be used to weights update.
            Instead of building new model over joint corpus, we can use weights update mode.
         */
        Word2Vec word2Vec = WordVectorSerializer.readWord2VecModel("pathToSaveModel.txt");

        INDArray wordVectorMatrix = word2Vec.getWordVectorMatrix("compile");
        double[] wordVector = word2Vec.getWordVector("compile");
        System.out.println(wordVectorMatrix);
        for(double d:wordVector){
            System.out.print(d+" ");
        }

    }
}

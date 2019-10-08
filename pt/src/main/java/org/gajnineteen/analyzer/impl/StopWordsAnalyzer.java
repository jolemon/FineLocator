package org.gajnineteen.analyzer.impl;

import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.core.StopAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.gajnineteen.analyzer.TextAnalyzer;

import java.util.Arrays;
import java.util.HashSet;

/**
 * @author Wenqiang Fang
 */
public class StopWordsAnalyzer implements TextAnalyzer {
    private CharArraySet stopWordsSet = new CharArraySet(0, true);
    public static String[] NLTK_STOP_WORDS = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "you're", "you've", "you'll", "you'd", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "she's", "her", "hers", "herself", "it", "it's", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "that'll", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "don't", "should", "should've", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", "couldn't", "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", "hasn't", "haven", "haven't", "isn", "isn't", "ma", "mightn", "mightn't", "mustn", "mustn't", "needn", "needn't", "shan", "shan't", "shouldn", "shouldn't", "wasn", "wasn't", "weren", "weren't", "won", "won't", "wouldn", "wouldn't"};
    public static String[] JAVA_KEY_WORDS = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "null", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"};
    public static String[] LUCENE_STOP_WORDS = {"a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"};

    /**
     * Constructor
     *
     * @param stopWords stop word
     */
    public StopWordsAnalyzer(String[] stopWords) {
        this.addStopWords(stopWords);
    }

    /**
     * add some new stop word
     *
     * @param stopWords stop word
     */
    public void addStopWords(String[] stopWords) {
        this.stopWordsSet.addAll(new HashSet<>(Arrays.asList(stopWords)));
    }

    /**
     * replace old stop word by new stop word
     *
     * @param stopWords
     */
    public void replaceStopWords(String[] stopWords) {
        this.stopWordsSet = new CharArraySet(0, true);
        this.addStopWords(stopWords);
    }


    /**
     * Remove stop words in stopWordsSet from text
     *
     * @param content the text needed to remove stop word.
     * @return removed result
     */
    @Override
    public String analysis(String content) {
        StopAnalyzer stopAnalyzer = new StopAnalyzer(this.stopWordsSet);
        TokenStream tokenStream = stopAnalyzer.tokenStream("field", content);
        CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
        StringBuilder stringBuilder = new StringBuilder();
        try {
            tokenStream.reset();
            while (tokenStream.incrementToken()) {
                stringBuilder.append(charTermAttribute.toString()).append(" ");
            }
            tokenStream.end();
            tokenStream.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return stringBuilder.toString();
    }
}

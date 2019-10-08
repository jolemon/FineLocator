package org.gajnineteen.analyzer.impl;

import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.miscellaneous.WordDelimiterGraphFilter;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.util.CharTokenizer;
import org.gajnineteen.analyzer.TextAnalyzer;

import java.io.IOException;

import static org.apache.lucene.analysis.miscellaneous.WordDelimiterGraphFilter.GENERATE_WORD_PARTS;
import static org.apache.lucene.analysis.miscellaneous.WordDelimiterGraphFilter.SPLIT_ON_CASE_CHANGE;

public class CompoundWordsAnalyzer extends Analyzer implements TextAnalyzer {
    /**
     * Method of splitting compound words that can be used directly
     *
     * @param text the text include compound words need to split.
     * @return Split result
     */
    @Override
    public String analysis(String text) {
        CompoundWordsAnalyzer compoundWordsAnalyzer = new CompoundWordsAnalyzer();
        TokenStream tokenStream = compoundWordsAnalyzer.tokenStream("content", text);
        StringBuilder stringBuilder = new StringBuilder();
        CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
        try {
            tokenStream.reset();
            while (tokenStream.incrementToken()) {
                stringBuilder.append(charTermAttribute.toString()).append(" ");
            }
            tokenStream.end();
            tokenStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return stringBuilder.toString();
    }


    /**
     * Override createComponents method in Analyzer
     *
     * @param fieldName fieldName
     * @return TokenStreamComponents
     */
    @Override
    protected TokenStreamComponents createComponents(String fieldName) {
        Tokenizer tokenizer = new CharTokenizer() {
            @Override
            protected boolean isTokenChar(int c) {
                return Character.isLetter(c);
            }
        };
        TokenFilter tokenFilter = new WordDelimiterGraphFilter(tokenizer, (GENERATE_WORD_PARTS | SPLIT_ON_CASE_CHANGE), CharArraySet.EMPTY_SET);
        return new TokenStreamComponents(tokenizer, tokenFilter);
    }
}

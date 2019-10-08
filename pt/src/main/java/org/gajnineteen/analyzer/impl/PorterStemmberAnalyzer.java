package org.gajnineteen.analyzer.impl;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.en.PorterStemFilter;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.util.CharTokenizer;
import org.gajnineteen.analyzer.TextAnalyzer;

import java.io.IOException;

public class PorterStemmberAnalyzer extends Analyzer implements TextAnalyzer {

    @Override
    protected Analyzer.TokenStreamComponents createComponents(String fieldName) {
        Tokenizer tokenizer = new CharTokenizer() {
            @Override
            protected boolean isTokenChar(int c) {
                return Character.isLetter(c);
            }
        };
        TokenFilter tokenFilter = new PorterStemFilter(tokenizer);
        return new Analyzer.TokenStreamComponents(tokenizer, tokenFilter);
    }

    @Override
    public String analysis(String text) {
        PorterStemmberAnalyzer porterStemmberAnalyzer = new PorterStemmberAnalyzer();
        TokenStream tokenStream = porterStemmberAnalyzer.tokenStream("content", text);
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
}

package org.gajnineteen.analyzer.impl;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.gajnineteen.analyzer.TextAnalyzer;

import java.io.IOException;

/**
 * @author 方文强
 */
public class CompoundWordsSaver implements TextAnalyzer {
    private Analyzer whitespaceAnalyzer = new WhitespaceAnalyzer();

    @Override
    public String analysis(String content) {
        TokenStream tokenStream = whitespaceAnalyzer.tokenStream("content", content.replaceAll("[^a-zA-Z]", " "));
        StringBuilder stringBuilder = new StringBuilder();
        CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
        try {
            tokenStream.reset();
            while (tokenStream.incrementToken()) {
                String str = charTermAttribute.toString();
                if (isCamelCase(str)) {
                    stringBuilder.append(str).append(" ");
                }
            }
            tokenStream.end();
            tokenStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return stringBuilder.toString();
    }

    private boolean isCamelCase(String str) {
        char[] chars = str.toCharArray();
        int upperCaseLetterNumber = 0;
//        int lowercaseLettersNumber = 0;
        for (char c : chars) {
            if (c >= 'A' && c <= 'Z') {
                upperCaseLetterNumber++;
            }
//            if (c >= 'a' && c <= 'z') {
//                lowercaseLettersNumber++;
//            }
        }
        if (upperCaseLetterNumber == 1 && (chars[0] < 'A' || chars[0] > 'Z')) {
            return true;
        } else {
            return (upperCaseLetterNumber >= 2 && (chars[1] < 'A' || chars[1] > 'Z'));
        }
    }
}

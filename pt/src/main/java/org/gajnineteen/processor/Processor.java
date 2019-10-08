package org.gajnineteen.processor;

import org.gajnineteen.analyzer.TextAnalyzer;
import org.gajnineteen.analyzer.impl.CompoundWordsSaver;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Wenqiang Fang
 */
public class Processor {
    protected List<TextAnalyzer> textAnalyzers;

    public void setText(String text) {
        this.text = text;
    }

    private String text;

    /**
     * Constructor
     */
    public Processor() {
        this.textAnalyzers = new ArrayList<>();
    }

    /**
     * analysis step
     *
     * @return processed result
     */
    public String process() {
        String compoundWords = saveCompoundWords();
//        System.out.println(text);
        for (TextAnalyzer textAnalyzer : textAnalyzers) {
            this.text = textAnalyzer.analysis(this.text);
//            System.out.println(text);
        }
        return this.text + compoundWords;
//        return this.text;
    }

    private String saveCompoundWords() {
        TextAnalyzer textAnalyzer = new CompoundWordsSaver();
        String str = textAnalyzer.analysis(this.text);
        return str;
    }

    /**
     * Used to change textAnalyzers
     *
     * @param textAnalyzer Text Analyzers added.
     */
    public void addAnalyzer(TextAnalyzer textAnalyzer) {
        textAnalyzers.add(textAnalyzer);
    }
}

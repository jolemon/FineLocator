package org.gajnineteen.analyzer.impl;

import org.junit.Test;

public class CompoundWordsAnalyzerTest {
    private CompoundWordsAnalyzer compoundWordsAnalyzer = new CompoundWordsAnalyzer();
    @Test
    public void testAnalysis(){
        String text = "getAntEditorSourceViewerConfiguration's";
        System.out.println(compoundWordsAnalyzer.analysis(text));
    }
}

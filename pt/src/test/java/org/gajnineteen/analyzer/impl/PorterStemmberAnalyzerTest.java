package org.gajnineteen.analyzer.impl;

import org.junit.Test;

public class PorterStemmberAnalyzerTest {
    private PorterStemmberAnalyzer porterStemmberAnalyzer = new PorterStemmberAnalyzer();
    @Test
    public void testAnalysis(){
        System.out.println(porterStemmberAnalyzer.analysis("reading reads"));
    }
}

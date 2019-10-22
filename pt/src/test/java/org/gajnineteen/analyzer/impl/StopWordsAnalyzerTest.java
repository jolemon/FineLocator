package org.gajnineteen.analyzer.impl;

import org.gajnineteen.analyzer.TextAnalyzer;
import org.junit.Test;

public class StopWordsAnalyzerTest {
    private TextAnalyzer stopWordsAnalyzer;

    @Test
    public void testAnalysis() {
        stopWordsAnalyzer = new StopWordsAnalyzer(StopWordsAnalyzer.NLTK_STOP_WORDS);
        System.out.println(stopWordsAnalyzer.analysis("summary: check for duplicate ACLs in addACL() and create() "));
        System.out.println(stopWordsAnalyzer.analysis("actual result:[zk: (CONNECTED) 0] create /test2 'test2' digest:test:test:cdrwa,digest:test:test:cdrwaCreated /test2[zk: (CONNECTED) 1] getAcl /test2'digest,'test:test: cdrwa'digest,'test:test: cdrwa[zk: (CONNECTED) 2]"));
    }

}

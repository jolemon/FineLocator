package org.gajnineteen.processor.impl;

import org.gajnineteen.analyzer.impl.CompoundWordsAnalyzer;
import org.gajnineteen.analyzer.impl.PorterStemmberAnalyzer;
import org.gajnineteen.analyzer.impl.StopWordsAnalyzer;
import org.gajnineteen.processor.Processor;

public class CodeProcessor extends Processor {
    public CodeProcessor(){
        this.textAnalyzers.add(new CompoundWordsAnalyzer());
        this.textAnalyzers.add(new StopWordsAnalyzer(StopWordsAnalyzer.JAVA_KEY_WORDS));
        this.textAnalyzers.add(new PorterStemmberAnalyzer());
    }

}

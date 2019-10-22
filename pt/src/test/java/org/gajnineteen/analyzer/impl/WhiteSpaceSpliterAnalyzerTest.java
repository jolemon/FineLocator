//package org.gajnineteen.analyzer.impl;
//
//import org.junit.Test;
//
//public class WhiteSpaceSpliterAnalyzerTest {
//    private WhiteSpaceSpliterAnalyzer whiteSpaceSpliterAnalyzer =new WhiteSpaceSpliterAnalyzer();
//    @Test
//    public void testAnalysis(){
//        System.out.println(whiteSpaceSpliterAnalyzer.analysis("summary:  check for duplicate ACLs in addACL() and create()"));
//        System.out.println(whiteSpaceSpliterAnalyzer.analysis("actual result:" +
//                "" +
//                "[zk: (CONNECTED) 0] create /test2 'test2' digest:test:test:cdrwa,digest:test:test:cdrwa" +
//                "Created /test2" +
//                "[zk: (CONNECTED) 1] getAcl /test2" +
//                "'digest,'test:test" +
//                ": cdrwa" +
//                "'digest,'test:test" +
//                ": cdrwa" +
//                "[zk: (CONNECTED) 2]"));
//    }
//}

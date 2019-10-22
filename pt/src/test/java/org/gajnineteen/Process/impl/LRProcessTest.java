package org.gajnineteen.Process.impl;

import org.gajnineteen.processor.impl.LRProcessor;
import org.junit.Test;

public class LRProcessTest {
    LRProcessor lrProcessor = new LRProcessor();

    @Test
    public void testProcess() {
        lrProcessor.setText("summary:  check for duplicate ACLs in addACL() and create()");
        System.out.println(lrProcessor.process());
        lrProcessor.setText("actual result:\n" +
                "\n" +
                "[zk: (CONNECTED) 0] create /test2 'test2' digest:test:test:cdrwa,digest:test:test:cdrwa\n" +
                "Created /test2\n" +
                "[zk: (CONNECTED) 1] getAcl /test2\n" +
                "'digest,'test:test\n" +
                ": cdrwa\n" +
                "'digest,'test:test\n" +
                ": cdrwa\n" +
                "[zk: (CONNECTED) 2]");
        System.out.println(lrProcessor.process());
    }
}

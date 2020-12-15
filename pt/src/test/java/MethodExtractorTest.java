import org.gajnineteen.extractor.Method;
import org.gajnineteen.extractor.MethodExtractor;
import org.junit.Test;

import java.io.File;
import java.util.List;

public class MethodExtractorTest {
    @Test
    public void testExtractMethod() {
        File file = new File("/Users/lienming/JIRA-dataset/org.aspectj/org.aspectj.ajdt.core/testsrc/org/aspectj/ajdt/internal/compiler/batch/BasicCommandTestCase.java");
        List<Method> methods = MethodExtractor.extract(file.toPath());
        for (Method method: methods) {
            method.print();
        }
    }
}

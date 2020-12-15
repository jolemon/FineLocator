import org.gajnineteen.extractor.TimeExtractor;
import org.junit.Test;

import java.util.Date;

public class TimeExtractorTest {
    @Test
    public void testGit() {
        TimeExtractor te;
        try {
            te = new TimeExtractor("/Users/lienming/JIRA-dataset/zookeeper/.git",
                    "src/java/jmx/org/apache/zookeeper/jmx/MBeanRegistry.java",
//                    "zookeeper/src/contrib/zooinspector/src/java/org/apache/zookeeper/inspector/manager/ZooInspectorManagerImpl.java",
                    "dcb4215e8");
            System.out.println(te.extract(143, 152));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testDate() {
        try {
            Date date = new TimeExtractor("/Users/lienming/Downloads/bugcode/Lang_1/.git",
                    "src/main/java/org/apache/commons/lang3/AnnotationUtils.java",
                    "2c454a4ce3fe771098746879b166ede2284b94f4" )
                    .extract(0, 370) ;
            System.out.println(date);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}

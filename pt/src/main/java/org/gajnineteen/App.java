package org.gajnineteen;

import org.gajnineteen.common.CommandLineValues;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.Option;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class App {

    private static CommandLineValues s_CommandLineValues;

    public static void main(String[] args) {
        try {
            s_CommandLineValues = new CommandLineValues(args);
        } catch (CmdLineException e) {
            e.printStackTrace();
            return;
        }


        if (s_CommandLineValues.type.equals("br")) {

        } else if (s_CommandLineValues.type.equals("code")) {
            extractDir();
        }
    }

    public static void extractDir(){
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(s_CommandLineValues.NumThreads);
        LinkedList<CodeTask> tasks = new LinkedList<>();
        try {
            Files.walk(Paths.get(s_CommandLineValues.source_dir)).filter(Files::isRegularFile)
                    .filter(p -> p.toString().toLowerCase().endsWith(".java")).forEach(f -> {
                CodeTask task = new CodeTask(s_CommandLineValues, f);
                tasks.add(task);
            });
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        try {
            executor.invokeAll(tasks);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
    }


    @Option(name = "-f", usage = "a")
    private String fileName;
    @Option(name = "-brs", usage = "a")
    private String bugReports = "";
    @Option(name = "-cols", required = true, usage = "a")
    private String cols = "";
    @Option(name = "-s",  usage = "a")
    private String stopWordsFilePath = "";

    private final static String COL_SPLITER = ",";
    private final static String ANALYZER_SPLITER = "-";

//    public static void main(String[] args) {
//        App app = new App();
//        CmdLineParser cmdLineParser = new CmdLineParser(app);
//        try {
//            cmdLineParser.parseArgument(args);
//        } catch (CmdLineException e) {
//            System.out.println("ERROR: Failed to parser argument.");
//            e.printStackTrace();
//        }
//
//        Processor processor = new Processor();
//        if (app.fileName != null && app.bugReports == null) {
//            System.out.println("Analysing Source Code...");
//            for (String col : app.cols.split(COL_SPLITER)) {
//                for (String analyzer : col.split(ANALYZER_SPLITER)) {
//                    switch (analyzer) {
//                        case "PorterStemmer":
//                            processor.addAnalyzer(new PorterStemmberAnalyzer());
//                            break;
//                        case "NLTKStopWord":
//                            processor.addAnalyzer(new StopWordsAnalyzer(StopWordsAnalyzer.JAVA_KEY_WORDS));
//                            break;
//                        case "CamelCaseSplitting":
//                            processor.addAnalyzer(new CompoundWordsAnalyzer());
//                            break;
//                        default:
//                            System.out.println("ERROR: Invalid analyzer.");
//                    }
//                }
//
//            }
//        } else if (app.bugReports != null && app.fileName == null) {
//            System.out.println("Analysing Bug Reports...");
//            for (String col : app.cols.split(COL_SPLITER)) {
//                for (String analyzer : col.split(ANALYZER_SPLITER)) {
//                    switch (analyzer) {
//                        case "PorterStemmer":
//                            processor.addAnalyzer(new PorterStemmberAnalyzer());
//                            break;
//                        case "NLTKStopWord":
//                            processor.addAnalyzer(new StopWordsAnalyzer(StopWordsAnalyzer.NLTK_STOP_WORDS));
//                            break;
//                        case "CamelCaseSplitting":
//                            processor.addAnalyzer(new CompoundWordsAnalyzer());
//                            break;
//                        default:
//                            System.out.println("ERROR: Invalid analyzer.");
//                    }
//                }
//
//            }
//        }else{
//            System.out.println("ERROR: Unsupported analysis type.");
//        }
//
//        System.out.println(processor.process());
//
//    }
}

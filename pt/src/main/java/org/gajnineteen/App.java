package org.gajnineteen;

import org.gajnineteen.common.CommandLineValues;
import org.gajnineteen.common.Common;
import org.kohsuke.args4j.CmdLineException;

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
            extractDir(Common.bugReport);
        } else if (s_CommandLineValues.type.equals("extract")) {
            extractDir(Common.extract);
        } else if (s_CommandLineValues.type.equals("code")) {
            extractDir(Common.code);
        }
    }

    public static void extractDir(String type){
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(s_CommandLineValues.NumThreads);
        LinkedList<PreprocessTask> tasks = new LinkedList<>();
        try {
            if(type.equals(Common.bugReport)){
                Files.walk(Paths.get(s_CommandLineValues.source_dir)).filter(Files::isRegularFile)
                        .filter(p -> !p.toString().endsWith(".DS_Store")).forEach(f -> {
                    PreprocessTask task = new PreprocessTask(s_CommandLineValues, f);
                    tasks.add(task);
                });
            } else if (type.equals(Common.extract) || type.equals(Common.code)) {

                Files.walk(Paths.get(s_CommandLineValues.source_dir)).filter(Files::isRegularFile)
                        .filter(p -> p.toString().endsWith(".java")).forEach(f -> {
                    PreprocessTask task = new PreprocessTask(s_CommandLineValues, f);
                    tasks.add(task);
                });
            }
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

}

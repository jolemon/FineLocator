package org.gajnineteen;

import org.gajnineteen.common.CommandLineValues;
import org.gajnineteen.common.Common;
import org.gajnineteen.extractor.Method;
import org.gajnineteen.extractor.MethodExtractor;
import org.gajnineteen.processor.Processor;
import org.gajnineteen.processor.impl.CodeProcessor;
import org.gajnineteen.processor.impl.LRProcessor;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.Callable;

public class PreprocessTask implements Callable<Void> {

    public static MethodExtractor methodExtractor = new MethodExtractor() ;

    private CommandLineValues commandLineValues;
    private Path filePath;

    public PreprocessTask(CommandLineValues commandLineValues, Path filePath){
        this.commandLineValues = commandLineValues ;
        this.filePath = filePath ;
    }

    @Override
    public Void call() throws IOException{
        if (this.commandLineValues.type.equals("br")){
            processFile(new LRProcessor());
        } else if (this.commandLineValues.type.equals("code")) {
            processFile(new CodeProcessor());
        } else if (this.commandLineValues.type.equals("extract")) {
            extractMethod();
        }

        return null;
    }

    private Path createSavePath() throws IOException {
        String filePathStr = filePath.toString() ;
        if (filePathStr.contains(commandLineValues.source_dir)) {
            filePathStr = filePathStr.replace(commandLineValues.source_dir, commandLineValues.target_dir) ;
        }

        Path toSavePath = Paths.get(filePathStr) ;

        if (!Files.exists(toSavePath)) {
            if (!Files.exists(toSavePath.getParent())) {
                Files.createDirectories(toSavePath.getParent());
            }
            Files.createFile(toSavePath) ;
        }
        return toSavePath;
    }

    public void processFile(Processor processor) throws IOException {
        BufferedWriter out= null ;
        String content ;

        Path toSavePath = null;
        toSavePath = createSavePath();
        // read original code

        try {
            content = new String(Files.readAllBytes(this.filePath)) ;
        } catch (IOException e) {
            e.printStackTrace();
            content = Common.EmptyString;
        }

        if (toSavePath == null) {
            System.out.println("toSavePath is null.");
            return ;
        } else {// write processed code to file
            out = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(toSavePath.toString()), "utf-8"));
        }

        processor.setText(content);
        String result = processor.process() ;

        out.write(result);
        out.close() ;
    }

    public void extractMethod() throws IOException {
        BufferedWriter out= null ;
        Path toSavePath = null;

        List<Method> list = methodExtractor.extract(this.filePath);
        toSavePath = createSavePath();
        if (toSavePath == null) {
            System.out.println("toSavePath is null.");
            return ;
        } else {
            out = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(toSavePath.toString()), "utf-8"));
        }

        for (Method method : list) {
            out.write(method.methodStr);
            out.newLine();
        }
        out.flush();
        out.close();
    }

}


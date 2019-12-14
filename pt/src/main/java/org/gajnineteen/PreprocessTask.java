package org.gajnineteen;

import org.eclipse.jgit.api.errors.GitAPIException;
import org.gajnineteen.common.CommandLineValues;
import org.gajnineteen.common.Common;
import org.gajnineteen.extractor.Method;
import org.gajnineteen.extractor.MethodExtractor;
import org.gajnineteen.extractor.TimeExtractor;
import org.gajnineteen.processor.Processor;
import org.gajnineteen.processor.impl.CodeProcessor;
import org.gajnineteen.processor.impl.LRProcessor;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;

public class PreprocessTask implements Callable<Void> {

    public static MethodExtractor methodExtractor = new MethodExtractor() ;
    public TimeExtractor timeExtractor ;

    private CommandLineValues commandLineValues;
    private Path filePath;

    public PreprocessTask(CommandLineValues commandLineValues, Path filePath) {
        this.commandLineValues = commandLineValues ;
        this.filePath = filePath ;
    }

    @Override
    public Void call() throws IOException, GitAPIException {
        if (this.commandLineValues.type.equals("br")){
            processFile(new LRProcessor());
        } else if (this.commandLineValues.type.equals("extract")) {
            extractMethod();
        } else if (this.commandLineValues.type.equals("code")) {
            processFile(new CodeProcessor());
        }

        return null;
    }

    private Path createSavePath(String fromDirPath, String toDirPath) throws IOException {
        String filePathStr = filePath.toString() ;
        if (filePathStr.contains(commandLineValues.source_dir)) {
            filePathStr = filePathStr.replace(fromDirPath, toDirPath) ;
        }

        Path toSavePath = Paths.get(filePathStr) ;
        if (!Files.exists(toSavePath)) {
            if (!Files.exists(toSavePath.getParent())) {
                Files.createDirectories(toSavePath.getParent());
            }
            Files.createFile(toSavePath) ;
        } else if (Files.isDirectory(toSavePath)){
            System.out.println(toSavePath.toString() + " has been created but it is a directory.");
        }

        return toSavePath;
    }

    public void processFile(Processor processor) throws IOException {
        BufferedWriter out ;
        String content     ;
        Path toSavePath    ;
        toSavePath = createSavePath(commandLineValues.source_dir, commandLineValues.target_dir);

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

        if (processor instanceof CodeProcessor) {
            StringBuilder stringBuilder = new StringBuilder();
            String[] methods = content.split("分"+System.getProperty("line.separator"));
            for (String method : methods) {
                if (method.length() == 0) {
                    continue;
                }
                processor.setText(method);
                String result = processor.process() ;
                result = result.concat("分"+System.getProperty("line.separator")) ;
                stringBuilder.append(result);
            }
            out.write(stringBuilder.toString());
        } else {
            processor.setText(content);
            String result = processor.process() ;
            out.write(result);

        }

        out.close() ;
    }

    public void extractMethod() throws IOException {
        BufferedWriter extractOut ;
        Path toSaveExtractPath    ;
        BufferedWriter correspondOut  ;
        Path toSaveCorrespondPath     ;

        List<Method> list = methodExtractor.extract(this.filePath);

        if (list.size() == 0 ) {
            return;
        }

        toSaveExtractPath    = createSavePath(commandLineValues.source_dir, commandLineValues.target_dir);
        toSaveCorrespondPath = createSavePath(commandLineValues.source_dir, commandLineValues.correspond_dir);

        if (toSaveExtractPath == null) {
            System.out.println("toSaveExtractPath is null.");
            return ;
        } else if (toSaveCorrespondPath == null) {
            System.out.println("toSaveCorrespondPath is null.");
            return ;
        } else {
            extractOut = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(toSaveExtractPath.toString()), StandardCharsets.UTF_8));    //"utf-8"
            correspondOut = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(toSaveCorrespondPath.toString()), StandardCharsets.UTF_8)); //"utf-8"
        }

        this.timeExtractor = new TimeExtractor(commandLineValues.git_dir,
                                filePath.toString().replace(commandLineValues.source_dir+"/", "")) ;

        for (Method method : list) {
            extractOut.write(method.methodStr);
            extractOut.write("分");
            extractOut.newLine();
//            method.print();
            Date latestModifyTime = null ;
            try {
                latestModifyTime = timeExtractor.extract(method.startLineNum, method.endLineNum);
            } catch (Exception e) {
                e.printStackTrace();
                method.print();
                latestModifyTime = new Date();
            } finally {
                correspondOut.write(method.signature + "$" + method.startLineNum
                        + "$" + method.endLineNum + "$" + latestModifyTime);
                correspondOut.newLine();
            }

        }
        extractOut.flush();
        extractOut.close();
        correspondOut.flush();
        correspondOut.close();
    }

}


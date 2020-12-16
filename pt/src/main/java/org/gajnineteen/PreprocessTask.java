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

    private final Path filePath;
    private final String type;
    private final String sourceDir;
    private final String targetDir;
    private final String correspondDir;
    private final String commitID;
    private final String gitDir;

    public PreprocessTask(CommandLineValues commandLineValues, Path filePath) {
        this.filePath = filePath ;
        this.type = commandLineValues.type;
        this.sourceDir = commandLineValues.source_dir;
        this.targetDir = commandLineValues.target_dir;
        this.correspondDir = commandLineValues.correspond_dir;
        this.commitID = commandLineValues.commitID;
        this.gitDir = commandLineValues.git_dir;
    }

    @Override
    public Void call() throws IOException, GitAPIException {
        switch (this.type) {
            case "br":
                processFile(new LRProcessor());
                break;
            case "extract":
                extractMethod();
                break;
            case "code":
                processFile(new CodeProcessor());
                break;
            default:
                break;
        }

        return null;
    }

    private Path createSavePath(String fromDirPath, String toDirPath) throws IOException {
        String filePathStr = filePath.toString() ;
        if (filePathStr.contains(this.sourceDir)) {
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
        toSavePath = createSavePath(this.sourceDir, this.targetDir);

        try {
            content = new String(Files.readAllBytes(this.filePath)) ;
        } catch (IOException e) {
            e.printStackTrace();
            content = Common.EmptyString;
        }

        // write processed code to file
        out = new BufferedWriter(new OutputStreamWriter
                (new FileOutputStream(toSavePath.toString()), StandardCharsets.UTF_8));

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

        List<Method> methods = MethodExtractor.extract(this.filePath);

        if (methods.isEmpty()) {
            return;
        }

        toSaveExtractPath    = createSavePath(this.sourceDir, this.targetDir);
        toSaveCorrespondPath = createSavePath(this.sourceDir, this.correspondDir);

        extractOut = new BufferedWriter(new OutputStreamWriter
                (new FileOutputStream(toSaveExtractPath.toString()), StandardCharsets.UTF_8));
        correspondOut = new BufferedWriter(new OutputStreamWriter
                (new FileOutputStream(toSaveCorrespondPath.toString()), StandardCharsets.UTF_8));

        for (Method method : methods) {
            extractOut.write(method.methodStr);
            extractOut.write("分");
            extractOut.newLine();
//            method.print();
            Date latestModifyTime = null ;
            try {
                latestModifyTime = TimeExtractor.getInstance(this.gitDir, this.commitID)
                        .extract(this.filePath.toString().substring(this.sourceDir.length()+1), method.startLineNum, method.endLineNum);
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println(this.filePath.toString());
                method.print();
//                latestModifyTime = new Date();
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


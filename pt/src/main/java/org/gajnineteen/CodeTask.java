package org.gajnineteen;

import org.gajnineteen.common.CommandLineValues;
import org.gajnineteen.common.Common;
import org.gajnineteen.processor.impl.CodeProcessor;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.Callable;

public class CodeTask implements Callable<Void> {
    CommandLineValues commandLineValues;
    Path filePath;

    public CodeTask(CommandLineValues commandLineValues, Path filePath){
        this.commandLineValues = commandLineValues ;
        this.filePath = filePath ;
    }

    @Override
    public Void call() throws Exception {
        processFile();
        return null;
    }

    private void processFile(){
        CodeProcessor codeProcessor = new CodeProcessor() ;
        BufferedWriter out= null ;

        String code = null;
        try {
            code = new String(Files.readAllBytes(this.filePath));
        } catch (IOException e) {
            e.printStackTrace();
            code = Common.EmptyString;
        }

        codeProcessor.setText(code);
        String result = codeProcessor.process() ;
        String filePathStr = filePath.toString() ;
        if (filePathStr.contains(commandLineValues.source_dir)) {
            filePathStr = filePathStr.replace(commandLineValues.source_dir, commandLineValues.target_dir) ;
        }
        Path toSavePath = Paths.get(filePathStr) ;
        try {
            // create dir and file
            if (!Files.exists(toSavePath)) {
                if (!Files.exists(toSavePath.getParent())) {
                    Files.createDirectories(toSavePath.getParent());
                }
                Files.createFile(toSavePath) ;
            }

            // write processed code to file
            out = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(filePathStr), "utf-8"));
            out.write(result);

            out.close(); // >= out.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}

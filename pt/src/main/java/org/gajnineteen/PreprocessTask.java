package org.gajnineteen;

import org.gajnineteen.common.CommandLineValues;
import org.gajnineteen.common.Common;
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
import java.util.concurrent.Callable;

public class PreprocessTask implements Callable<Void> {
    private CommandLineValues commandLineValues;
    private Path filePath;

    public PreprocessTask(CommandLineValues commandLineValues, Path filePath){
        this.commandLineValues = commandLineValues ;
        this.filePath = filePath ;
    }

    @Override
    public Void call(){
        if(this.commandLineValues.type.equals("br")){
            processFile(new LRProcessor());
        } else if(this.commandLineValues.type.equals("code")) {
            processFile(new CodeProcessor());
        }
        return null;
    }

    private void processFile(Processor processor){
        BufferedWriter out= null ;
        String content ;

        String filePathStr = filePath.toString() ;
        if (filePathStr.contains(commandLineValues.source_dir)) {
            filePathStr = filePathStr.replace(commandLineValues.source_dir, commandLineValues.target_dir) ;
        }
        Path toSavePath = Paths.get(filePathStr) ;

        try {
            // read original code
            content = new String(Files.readAllBytes(this.filePath)) ;

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
        } catch (IOException e) {
            e.printStackTrace();
            content = Common.EmptyString;
        }

        processor.setText(content);
        String result = processor.process() ;

        try {
            out.write(result);
            out.close() ;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


//        List<String> lines ;
//  exception about : encoding
//            StringBuilder stringBuilder = new StringBuilder();
//            lines = Files.readAllLines(this.filePath) ;
//            for(String line : lines){
//                codeProcessor.setText(line);
//                String processed_line = codeProcessor.process();
//                stringBuilder.append(processed_line).append(System.getProperty("line.separator")) ;
//            }
//            // delete additional line separator
//            stringBuilder = stringBuilder.deleteCharAt(stringBuilder.lastIndexOf(System.getProperty("line.separator"))) ;
//            out.write(stringBuilder.toString()) ;
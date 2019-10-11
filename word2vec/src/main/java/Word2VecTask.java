import common.CommandLineValues;
import common.Common;
import model.Word2VecModel;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.nd4j.linalg.api.ndarray.INDArray;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.Callable;

public class Word2VecTask implements Callable<Void> {

    private static Word2Vec model = Word2VecModel.loadModel(Common.modelSavePath);

    private CommandLineValues commandLineValues;
    private Path filePath;


    public Word2VecTask(CommandLineValues commandLineValues, Path filePath){
        this.commandLineValues = commandLineValues ;
        this.filePath = filePath ;
    }

    @Override
    public Void call(){
        processFile();
        return null;
    }

    private void processFile() {
        BufferedWriter out= null ;
        String content ;

        String filePathStr = filePath.toString() ;
        if (filePathStr.contains(commandLineValues.source_dir)) {
            filePathStr = filePathStr.replace(commandLineValues.source_dir, commandLineValues.target_dir) ;
        }
        Path toSavePath = Paths.get(filePathStr) ;

        try {
            content = new String(Files.readAllBytes(this.filePath)) ;

            if (!Files.exists(toSavePath)) {
                if (!Files.exists(toSavePath.getParent())) {
                    Files.createDirectories(toSavePath.getParent());
                }
                Files.createFile(toSavePath) ;
            }

            out = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(filePathStr), "utf-8"));
            for (String word : content.split(" ")) {
                INDArray wordVectorMatrix = model.getWordVectorMatrix(word.toLowerCase()) ;
                if (wordVectorMatrix == null) {
                    System.out.println(word + " not in the vocabulary.");
                } else {
                    out.write(wordVectorMatrix.toString());
                }
            }
            out.flush();
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

}

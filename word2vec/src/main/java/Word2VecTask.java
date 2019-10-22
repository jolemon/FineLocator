import common.CommandLineValues;
import common.Common;
import model.Word2VecModel;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
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

            StringBuilder stringBuilder = new StringBuilder();

//            System.out.println(filePath.toString());
            for (String method : content.split("分")) {
                method = method.trim();
                if (method.length() == 0) {
                    continue;
                }

                List<INDArray> vecList = new ArrayList<>();

                for (String word : method.split(" ")) {
                    if (word.length() == 0) {
                        continue;
                    }
                    INDArray wordVectorMatrix = model.getWordVectorMatrix(word.toLowerCase()) ;


                    wordVectorMatrix.amax();
                    if (wordVectorMatrix == null) {
                        System.out.println(word + " not in the vocabulary.");
                    } else {
                        vecList.add(wordVectorMatrix);
                    }
                }


                INDArray array = Nd4j.create(vecList, vecList.size(), Common.dimension);
                INDArray array1 = Nd4j.zeros(1, Common.dimension) ;
                for (int i=0 ; i<Common.dimension; i++) {
                    Number number = array.getColumns(i).maxNumber() ;
                    array1.put(0, i, number);
                }

//                stringBuilder.append(array.toString()).append(System.getProperty("line.separator"));
//                stringBuilder.append("内").append(System.getProperty("line.separator"));
                stringBuilder.append(array1).append(System.getProperty("line.separator")) ;
                stringBuilder.append("分").append(System.getProperty("line.separator"));
            }
            out.write(stringBuilder.toString());
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

}

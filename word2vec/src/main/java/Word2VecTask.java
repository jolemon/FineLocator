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
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
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
        BufferedWriter out ;
        String content ;
        List<String> tfidfContent ;
        String filePathStr = filePath.toString() ;
        String tfidfPathStr = filePathStr;
        String correspondPathStr = filePathStr ;
        if (filePathStr.contains(commandLineValues.source_dir)) {
            filePathStr  = filePathStr.replace(commandLineValues.source_dir, commandLineValues.target_dir) ;
            tfidfPathStr = tfidfPathStr.replace(commandLineValues.source_dir, commandLineValues.tfidf_dir) ;
        }
        if (commandLineValues.type.equals(Common.CodeType)) {
            correspondPathStr = correspondPathStr.replace(commandLineValues.source_dir, commandLineValues.correspond_dir) ;
        }
        Path toSavePath = Paths.get(filePathStr) ;
        Path tfidfPath = Paths.get(tfidfPathStr) ;
        Path correspondPath = Paths.get(correspondPathStr) ;
        try {
            content = new String(Files.readAllBytes(this.filePath)) ;

            if (!Files.exists(toSavePath)) {
                if (!Files.exists(toSavePath.getParent())) {
                    Files.createDirectories(toSavePath.getParent());
                }
                Files.createFile(toSavePath) ;
            }
            out = new BufferedWriter(new OutputStreamWriter
                    (new FileOutputStream(filePathStr), StandardCharsets.UTF_8));

            StringBuilder stringBuilder ;
            if (commandLineValues.type.equals(Common.CodeType)) {
                Map<String, Map<String, Double>> methodsDictionary = getMethodDictionary(tfidfPath) ;
                List<String> signatures = getMethodSignature(correspondPath) ;
                stringBuilder = constructMethodVecString(content, methodsDictionary, signatures) ;
                out.write(stringBuilder.toString());
            } else if (commandLineValues.type.equals(Common.BRType)) {
                Map<String, Double> brDictionary = getBRDictionary(tfidfPath) ;
                stringBuilder = constructBrVecString(content, brDictionary) ;
                out.write(stringBuilder.toString());
            }
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    private Map<String, Map<String, Double>> getMethodDictionary(Path tfidfPath) throws IOException{
        List<String> tfidfContent = Files.readAllLines(tfidfPath);
        Map<String, Map<String, Double>> fileMap = new HashMap<>() ;
        for (String line : tfidfContent) {
            line = line.trim() ;
            if (line.length() <= 0 ) {
                continue;
            }
            String[] parts = line.split("分");

            Map<String, Double> tfidfMap = new HashMap<>();
            if (parts.length > 1) {
                for (String tfidfMapStr : parts[1].split("内")) {
                    String[] tfidfParts = tfidfMapStr.split("\\$") ;
                    String word = tfidfParts[0] ;
                    double tfidfValue = Double.parseDouble(tfidfParts[1]) ;
                    tfidfMap.put(word, tfidfValue);
                }
            }

            String signature = parts[0];
            fileMap.put(signature, tfidfMap);

        }
        return fileMap;
    }

    private List<String> getMethodSignature(Path correspondPath) throws IOException {
        List<String> lines = Files.readAllLines(correspondPath);
        List<String> signatures = new ArrayList<>() ;
        for (String line : lines) {
            line = line.trim() ;
            String[] parts = line.split("\\$") ;
            signatures.add(parts[0].trim()) ;
//            for (int i=parts.length-1; i>=parts.length-3 ; i--) {
//                line = line.replace(","+parts[i], "") ;
//            }
//            signatures.add(line.trim()) ;
        }
        return signatures;
    }

    private StringBuilder constructMethodVecString(String content, Map<String, Map<String, Double>> methodsDictionary, List<String> signatures) {
        StringBuilder stringBuilder = new StringBuilder();
        content = content.trim() ;
        String[] methods = content.split(System.getProperty("line.separator")) ;
        for (int k=0 ; k<methods.length; k++) {
            String methodDoc = methods[k] ;
            methodDoc = methodDoc.trim();
            String signature = signatures.get(k) ;
            if (methodDoc.length() == 0) {
                continue;
            }
            if (methodDoc.equals("分")) {
                INDArray array1 = Nd4j.zeros(1, Common.dimension) ;
                stringBuilder.append(array1).append(System.getProperty("line.separator")) ;
                stringBuilder.append("#").append(signature).append("分").append(System.getProperty("line.separator"));
            } else {
                methodDoc = methodDoc.replace("分", "") ;
            }

            List<INDArray> vecList = new ArrayList<>();

            if ( !methodsDictionary.containsKey(signature) ) {
                System.out.println(this.filePath.toString() + "#" + signature + ": cannot find corresponding tfidf dictionary.");
                continue;
            }
            Map<String, Double> methodDictionary = methodsDictionary.get(signature) ;

            // vec multiply tfidf value
            if (methodDoc.contains(" ")) {
                for (String word : methodDoc.split(" ")) {
                    word = word.trim();
                    if (word.length() == 0) {
                        continue;
                    }

                    if (!methodDictionary.containsKey(word)) {
                        System.out.println(this.filePath.toString() + "#" + signature + "#" + word + ": not in tfidf dictionary.");
                        continue;
                    }

                    INDArray wordVectorMatrix = model.getWordVectorMatrix(word.toLowerCase());

                    if (wordVectorMatrix == null) {
                        System.out.println(word + " not in the word2vec model's vocabulary.");
                        continue;
                    } else {
                        // query dictionary for tf*idf of word and multiply vector
                        Double tfidfValue = methodDictionary.get(word);
                        wordVectorMatrix = wordVectorMatrix.mul(tfidfValue);
                        vecList.add(wordVectorMatrix);
                    }
                }
            }

            INDArray array = Nd4j.create(vecList, vecList.size(), Common.dimension);
            INDArray array1 = Nd4j.zeros(1, Common.dimension) ;
            for (int i=0 ; i<Common.dimension; i++) {
//                Number number = array.getColumns(i).maxNumber() ;
                Number number = array.getColumns(i).maxNumber() ;
                array1.put(0, i, number);
            }

            stringBuilder.append(array1).append(System.getProperty("line.separator")) ;
            stringBuilder.append("#").append(signature).append("分").append(System.getProperty("line.separator"));
        }
        return stringBuilder ;
    }

    private Map<String, Double> getBRDictionary(Path tfidfPath) throws IOException {
        List<String> tfidfContent = Files.readAllLines(tfidfPath);
        Map<String, Double> fileMap = new HashMap<>() ;
        for (String line : tfidfContent) {
            line = line.trim() ;
            if (line.length() <= 0 ) {
                continue;
            }
            String[] tfidfParts = line.split("\\$");
            if (tfidfParts.length == 1) {
                continue;
            }

            String word = tfidfParts[0] ;
            double tfidfValue = Double.parseDouble(tfidfParts[1]) ;
            fileMap.put(word, tfidfValue);
        }
        return fileMap;
    }

    private StringBuilder constructBrVecString(String content, Map<String, Double> brDictionary) {
        StringBuilder stringBuilder = new StringBuilder();

        List<INDArray> vecList = new ArrayList<>();
        for (String word : content.split(" ")) {
            word = word.trim();
            if (word.length() == 0) {
                continue;
            }

            if ( !brDictionary.containsKey(word) ) {
                System.out.println(word + " word : not in tfidf dictionary..");
                continue;
            }

            INDArray wordVectorMatrix = model.getWordVectorMatrix(word.toLowerCase()) ;
            if (wordVectorMatrix == null) {
                System.out.println(word + " not in the vocabulary.");
                continue;
            } else {
                // query dictionary for tf*idf of word and multiply vector
                Double tfidfValue = brDictionary.get(word) ;
                wordVectorMatrix = wordVectorMatrix.mul(tfidfValue) ;
                vecList.add(wordVectorMatrix);
            }

        }

        INDArray array = Nd4j.create(vecList, vecList.size(), Common.dimension);
        INDArray array1 = Nd4j.zeros(1, Common.dimension) ;
        for (int i=0 ; i<Common.dimension; i++) {
//            Number number = array.getColumns(i).maxNumber() ;
            Number number = array.getColumns(i).maxNumber() ;
            array1.put(0, i, number);
        }

        stringBuilder.append(array1) ;

        return stringBuilder ;
    }

}

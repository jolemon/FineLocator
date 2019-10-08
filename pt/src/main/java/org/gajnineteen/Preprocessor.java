package org.gajnineteen;

import org.gajnineteen.processor.impl.CodeProcessor;
import org.gajnineteen.processor.impl.LRProcessor;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

import java.io.*;

public class Preprocessor {

    @Option(name = "-source", usage = "a")
    private String source_dir ;
    @Option(name = "-target", usage = "a")
    private String target_dir ;
    @Option(name = "type")
    private String type ;

    /**
     *  LRProcessor 预处理步骤
     *  1. 从bug报告中提取summary+description
     *  2. 按capital letters断开复合词，原来的也保留
     *  3. 移除标点，数字，标准IR停用词(NLTK stopwords list)
     *  4. use Porter stemmer to stemize words
     */
    public void doProcess(String source_path,String target_path) throws IOException {
        LRProcessor lrp = new LRProcessor();

        File file = new File(source_path);		//获取其file对象
        File[] files = file.listFiles();	//遍历path下的文件和目录，放在File数组中

        BufferedReader in = null ;
        BufferedWriter out= null ;
        createDir(target_path);
        for(File f : files){					//遍历File[]数组
//            System.out.println(f.getName());
            if(f.isDirectory()) {
                continue;
            } else if(f.getName().equals(".DS_Store")){
                continue;
            } else {
                String file_name = f.getName() ;
                String file_path = f.getPath() ;
                in = new BufferedReader(new InputStreamReader(new FileInputStream(file_path), "utf-8"));
                String toFilePath = target_path + "/" + file_name ;
                createFile(toFilePath);
                out = new BufferedWriter(new OutputStreamWriter
                        (new FileOutputStream(toFilePath), "utf-8"));
                String str = null;
                while ((str = in.readLine()) != null) {
                    lrp.setText(str);
                    String result = lrp.process();
                    out.write(result);
                    out.newLine();
                }
                out.flush();
            }
        }
        //关闭流
        in.close();
        out.close();
    }

    public void doProcessForCode(String source_dir,String target_dir) throws Exception {
       CodeProcessor cp = new CodeProcessor();

       BufferedReader in = null ;
       BufferedWriter out= null ;

//       try {
//            Files.walk(Paths.get(source_dir)).filter(Files::isRegularFile)
//                    .filter(p -> p.toString().toLowerCase().endsWith(".java")).forEach(f -> {
//
////                ExtractFeaturesTask task = new ExtractFeaturesTask(s_CommandLineValues, f);
////                tasks.add(task);
//            });
//        } catch (Exception e) {
//            e.printStackTrace();
//            return;
//        }
    }

    public static void main(String[] args) throws Exception {
        Preprocessor preprocessor = new Preprocessor() ;
        CmdLineParser cmdLineParser = new CmdLineParser(preprocessor);
        try {
            cmdLineParser.parseArgument(args);
        } catch (CmdLineException e) {
            System.out.println("ERROR: Failed to parser argument.");
            e.printStackTrace();
        }


//        String source_path = "/Users/lienming/Downloads/istDat4exp/bugReport4Vector/ant";		//要遍历的路径
//        String target_path = "/Users/lienming/Downloads/ant" ;
//        Preprocessor preprocessor = new Preprocessor();
//        preprocessor.source_dir=source_path;
//        preprocessor.target_dir=target_path;
        if(preprocessor.type.equals("br")) {
            preprocessor.doProcess(preprocessor.source_dir, preprocessor.target_dir);
        } else if(preprocessor.type.equals("code")) {
            preprocessor.doProcessForCode(preprocessor.source_dir, preprocessor.target_dir);
        }
    }


    static void createDir(String path) {
        File dir = new File(path);
        if(!dir.exists()){
            dir.mkdirs();
        }
    }

    static void createFile(String path)  {
        File f = new File(path);

        if(!f.exists()){
            try {
                f.createNewFile();
            } catch (IOException e) {
                System.out.println(path);
                e.printStackTrace();
            }
        }
    }



}




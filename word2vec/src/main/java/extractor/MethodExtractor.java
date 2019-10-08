package extractor;

import common.Common;
import org.eclipse.jdt.core.dom.*;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Extract Method from Java Files
 * Input : project path
 * Output : files in same structure as project, and each line of which is a method,
 *          including method declaration and body.
 */
public class MethodExtractor {

    public MethodExtractor(){ }


    public List<String> extract(Path filePath){
        String content ;
        try {
            content = new String(Files.readAllBytes(filePath)) ;
        } catch (Exception e) {
            e.printStackTrace();
            content = Common.EmptyString;
        }

        ASTParser parser = ASTParser.newParser(AST.JLS3);
        parser.setKind(ASTParser.K_COMPILATION_UNIT);     //to parse compilation unit
        parser.setSource(content.toCharArray());          //content is a string which stores the java source
        parser.setResolveBindings(true);

        CompilationUnit result = (CompilationUnit) parser.createAST(null);
        List types = result.types();
        if(types.size()==0){
            System.out.println("ASTParser.createAST().types().size()=0. Extract Failed.");
            return null;
        }
        TypeDeclaration typeDec = (TypeDeclaration) types.get(0);
        System.out.println("className:" + typeDec.getName());

        List<String> methodList = new ArrayList<>();

        //show methods
        MethodDeclaration[] methodDeclarations = typeDec.getMethods();

        for (MethodDeclaration methodDeclaration : methodDeclarations) {
            methodList.add(getMethod(methodDeclaration));
        }

        return methodList;
    }

    /**
     * @param methodDeclaration
     * @return
     */
    public String getMethodName(MethodDeclaration methodDeclaration){
        String res = "" ;
        SimpleName methodName = methodDeclaration.getName();
        if(methodDeclaration.isConstructor()) {
            res = res.concat(methodName.toString()) ;
        } else {
            Type returnType = methodDeclaration.getReturnType2();
            res = returnType + " " + methodName.toString();
        }
        res = res.concat("(");
        List parameters = methodDeclaration.parameters();
        if(parameters.size()==0) {
            res = res.concat(")");
            return res;
        }
        for(int i=0;i<parameters.size()-1;i++){
            res = res.concat(parameters.get(i).toString()).concat(", ") ;
        }
        res = res.concat(parameters.get(parameters.size()-1).toString()).concat(")");
        return res ;
//        return methodDeclaration.toString().replace(methodDeclaration.getBody().toString(), "");  //will remain comment!
    }

    /**
     * get the whole method block.
     * @param methodDeclaration
     * @return
     */
    public String getMethod(MethodDeclaration methodDeclaration) {
        return methodDeclaration.toString();
    }

    public static void main(String[] args) {
        File file = new File("src/main/java/extractor/MethodExtractor.java") ;
        MethodExtractor methodExtractor = new MethodExtractor() ;
        List<String> methods = methodExtractor.extract(file.toPath());
        for(String method:methods) {
            System.out.println(method);
        }
    }
}

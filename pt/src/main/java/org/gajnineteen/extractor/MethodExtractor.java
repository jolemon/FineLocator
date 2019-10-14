package org.gajnineteen.extractor;

import org.eclipse.jdt.core.dom.*;
import org.gajnineteen.common.Common;

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

    public List<Method> extract(Path filePath){
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

        CompilationUnit compilationUnit = (CompilationUnit) parser.createAST(null);

        List types = compilationUnit.types();
        if(types.size()==0){
//            System.out.println(filePath.toString() + " ASTParser.createAST().types().size()=0. Extract Failed.");
            return null;
        }
        TypeDeclaration typeDec = (TypeDeclaration) types.get(0);

        List<Method> methodList = new ArrayList<>();

        //show methods
        MethodDeclaration[] methodDeclarations = typeDec.getMethods();

        for (MethodDeclaration methodDeclaration : methodDeclarations) {
            int startLineNum = getMethodStartLineNum(compilationUnit, methodDeclaration) ;
            int endLineNum = getMethodEndLineNum(compilationUnit, methodDeclaration) ;

            String methodSignature = getMethodSignature(methodDeclaration) ;
            String methodStr = getMethodWithoutJavadoc(methodDeclaration) ;
            Method method = new Method(methodSignature, startLineNum, endLineNum, methodStr) ;

            methodList.add(method);
        }
        return methodList;
    }


    /**
     * get start line of method without comment
     * TODO  : the blank lines between javadoc and methodSignature(if have) are not
     * included in methodDeclaration. So it will cause problem if there are such blank lines!
     * @param compilationUnit
     * @param methodDeclaration
     * @return
     */
    int getMethodStartLineNum(CompilationUnit compilationUnit, MethodDeclaration methodDeclaration) {
        Javadoc javaDoc = methodDeclaration.getJavadoc();
        if (javaDoc == null) {
            return compilationUnit.getLineNumber(methodDeclaration.getStartPosition());
        } else {
            int javaDocStartPosition = javaDoc.getStartPosition();
            int methodStartPosition = javaDocStartPosition + javaDoc.getLength() + 1 ;
//            System.out.println(compilationUnit.getLineNumber(methodStartPosition));
            return compilationUnit.getLineNumber(methodStartPosition) ;
        }
    }

    public int lstripLength(String value) {
        int len = value.length();
        int st = 0;
        char[] val = value.toCharArray();    /* avoid getfield opcode */

        while ((st < len) && (val[st] <= ' ')) {
            st++;
        }
        return st ;
    }


    int getMethodEndLineNum(CompilationUnit compilationUnit, MethodDeclaration methodDeclaration) {
        return compilationUnit.getLineNumber(
                methodDeclaration.getStartPosition() + methodDeclaration.getLength());
    }

    List getModifiers(MethodDeclaration methodDeclaration){
        return methodDeclaration.modifiers() ;
        // methodDeclaration.getModifiers() returns a flag of int type
    }


    public String getMethodSignature(MethodDeclaration methodDeclaration) {
        String res = getMethodWithoutJavadoc(methodDeclaration) ;
        return res.replace(methodDeclaration.getBody().toString(), "").trim();  //will remain comment!
    }

    /**
     * get the whole method without javadoc
     * @param methodDeclaration
     * @return
     */
    public String getMethodWithoutJavadoc(MethodDeclaration methodDeclaration) {
        if (methodDeclaration.getJavadoc() !=null ) {
            String docStr = methodDeclaration.getJavadoc().toString();
            return methodDeclaration.toString().replace(docStr, "");
        }
        return methodDeclaration.toString();
//        return methodDeclaration.toString().trim();
    }

//    public static void main(String[] args) {
//        MethodExtractor methodExtractor = new MethodExtractor();
//        File file = new File("/Users/lienming/FineLocator/pt/src/main/java/org/gajnineteen/extractor/MethodExtractor.java");
//
//        List<Method> list = methodExtractor.extract(file.toPath());
//        for (Method method:list) {
//            method.print();
//        }
//
//    }


}

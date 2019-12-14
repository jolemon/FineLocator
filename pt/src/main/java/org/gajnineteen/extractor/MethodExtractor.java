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


        //get main class name
        String mainClassName = typeDec.getName().toString() ;
//        System.out.println("MainClass Name : " + mainClassName);

        //get methods in main class
        MethodDeclaration[] methodDeclarations = typeDec.getMethods();
        addToList(methodList, mainClassName, methodDeclarations, compilationUnit);

        //get methods in inner classes
//        recursiveSearchSubclass(typeDec, methodList, mainClassName, compilationUnit);
        TypeDeclaration[] subclasses = typeDec.getTypes();
        if(subclasses.length>0){
            for (TypeDeclaration subclass:subclasses) {
                // Method to get subclass name as follow :
                String subclassName =  subclass.getName().toString() ;
//                System.out.println("Subclass Name : " + subclassName);
                MethodDeclaration[] subclassMethods = subclass.getMethods();
                addToList(methodList, subclassName, subclassMethods, compilationUnit);
            }
        }

        return methodList;
    }

    // try to search subclass recursively
    void recursiveSearchSubclass(TypeDeclaration typeDeclaration, List<Method> methodList,
                                 String className, CompilationUnit compilationUnit) {
        TypeDeclaration[] subclasses = typeDeclaration.getTypes() ;
        if(subclasses.length>0){
            for (TypeDeclaration subclass:subclasses) {
                // Method to get subclass name as follow :
                String subclassName =  subclass.getName().toString() ;
                String subclassPath = className.concat("#"+subclassName) ;
                MethodDeclaration[] subclassMethods = subclass.getMethods();
                addToList(methodList, subclassPath, subclassMethods, compilationUnit);
                recursiveSearchSubclass(subclass, methodList, subclassPath, compilationUnit);
            }
        }
    }

    void addToList(List<Method> list, String className, MethodDeclaration[] methodDeclarations, CompilationUnit compilationUnit){
        for (MethodDeclaration methodDeclaration : methodDeclarations) {
            int startLineNum = getMethodStartLineNum(compilationUnit, methodDeclaration) ;
            int endLineNum = getMethodEndLineNum(compilationUnit, methodDeclaration) ;

            String methodSignature = getMethodSignature(methodDeclaration) ;
            methodSignature = className.concat("#").concat(methodSignature) ;
            String methodStr = getMethodWithoutJavadoc(methodDeclaration) ;
            Method method = new Method(methodSignature, startLineNum, endLineNum, methodStr) ;
            list.add(method);
        }
    }


    /**
     * get start line of method without comment
     * the blank lines between javadoc and methodSignature(if have) are not
     * included in methodDeclaration. So it will cause problem if there are such blank lines!
     * Solution : compare returnTypeLineNum with the JavadocNextLineNum
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
            int javadocNextLineNum = compilationUnit.getLineNumber(methodStartPosition) ;
            return javadocNextLineNum;
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
        String res = "" ;
        Type returnType = methodDeclaration.getReturnType2() ;
        if (returnType != null) {
            res = res.concat(returnType.toString() + " ");
        }
        String methodName = methodDeclaration.getName().toString() ;
        res = res.concat(methodName) ;
        List paras = methodDeclaration.parameters();
        String parameters = constructParams(paras) ;
        res = res.concat(parameters) ;
        return res ;
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

    String constructParams(final List paras) {
        int parasLength = paras.size() ;
        if (parasLength == 0) {
            return "()";
        } else {
            String para0 = paras.get(0).toString().replace("final ", "") ;
            if (parasLength == 1) {
                return "(" + para0 + ")" ;
            } else {
                String result = "(" + para0 ;
                for (int i=1 ; i<parasLength ; i++) {
                    String paraString = paras.get(i).toString().replace("final ", "");
                    result = result.concat(","+paraString)  ;
                }
                result = result.concat(")") ;
                return result ;
            }
        }

    }

//    public static void main(String[] args) {
//        MethodExtractor methodExtractor = new MethodExtractor();
////        File file = new File("/Users/lienming/FineLocator/pt/src/main/java/org/gajnineteen/extractor/MethodExtractor.java");
//        File file = new File("/Users/lienming/Downloads/final_defects4j/allMethods/Time/Time_6/src/main/java/org/joda/time/chrono/GJChronology.java");
//        List<Method> list = methodExtractor.extract(file.toPath());
//        for (Method method:list) {
//            method.print();
//        }
//
//    }


}

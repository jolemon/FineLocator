package org.gajnineteen.extractor;

import org.eclipse.jdt.core.dom.*;
import org.gajnineteen.common.Common;

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
            System.out.println("ASTParser.createAST().types().size()=0. Extract Failed.");
            return null;
        }
        TypeDeclaration typeDec = (TypeDeclaration) types.get(0);
//        System.out.println("className: " + typeDec.getName());

        List<Method> methodList = new ArrayList<>();

        //show methods
        MethodDeclaration[] methodDeclarations = typeDec.getMethods();

        for (MethodDeclaration methodDeclaration : methodDeclarations) {
            int nameStartPosition = methodDeclaration.getName().getStartPosition();
            int startLineNum = compilationUnit.getLineNumber(nameStartPosition) ;
            int methodLength = getMethodLengthWithoutJavadoc(methodDeclaration) ;
            int modifierLength = getModifierLength(methodDeclaration);
            int returnStrLength = getReturnStrLength(methodDeclaration);

            int methodEndPosition = computeEndLinePosition(nameStartPosition, modifierLength, returnStrLength, methodLength) ;
            int endLineNum = compilationUnit.getLineNumber(methodEndPosition) ;

            String methodSignature = getMethodSignature(methodDeclaration) ;
            String methodStr = getMethod(methodDeclaration) ;
            Method method = new Method(methodSignature, startLineNum, endLineNum, methodStr) ;
//            method.print();

            methodList.add(method);
        }

        return methodList;
    }

    int computeEndLinePosition(int nameStartPosition, int modifierLength, int returnStrLength, int methodLength) {
        int methodEndPosition = nameStartPosition ;
        if (modifierLength > 0) {
            methodEndPosition = methodEndPosition - modifierLength - 1 ;
        }
        if (returnStrLength > 0 ) {
            methodEndPosition = methodEndPosition - returnStrLength - 1 ;
        }
        return methodEndPosition + methodLength ;
    }

    int getMethodLengthWithoutJavadoc(MethodDeclaration methodDeclaration){
        Javadoc javadoc = methodDeclaration.getJavadoc();
        if (javadoc == null) {
            return methodDeclaration.getLength() ;
        }
        return methodDeclaration.getLength() - javadoc.getLength() - 5 ;  // Note : line.separator + 4 * blank space
    }

    int getReturnStrLength(MethodDeclaration methodDeclaration){
        Type returnType = methodDeclaration.getReturnType2();
        return returnType != null ? returnType.toString().length() : 0 ;
    }


    int getModifierLength(MethodDeclaration methodDeclaration){
        int length = 0 ;
        List modifiers = methodDeclaration.modifiers() ;

        if(modifiers == null) {
            return 0 ;
        } else {
            for (Object o : modifiers) {
                if (o instanceof Modifier) {
                    String keyWord = ((Modifier) o).getKeyword().toString();
                    length += keyWord.length() + 1 ;  //Note : default blank space length always == 1
                }
            }
            return length - 1 ;
        }
    }

    /**
     * @param methodDeclaration
     * @return
     */
    public String getMethodSignature(MethodDeclaration methodDeclaration){
        String res = getMethod(methodDeclaration) ;
        return res.replace(methodDeclaration.getBody().toString(), "").trim();  //will remain comment!
    }

    /**
     * get the whole method without javadoc
     * @param methodDeclaration
     * @return
     */
    public String getMethod(MethodDeclaration methodDeclaration) {
        if (methodDeclaration.getJavadoc() !=null) {
            String docStr = methodDeclaration.getJavadoc().toString();
            String str = methodDeclaration.toString().replace(docStr, "");
//            str = str.trim();
            return str;
        }
        return methodDeclaration.toString();
//        return methodDeclaration.toString().trim();
    }

    public static void main(String[] args) {
        File file = new File("src/main/java/model/Word2VecModel.java") ;
        MethodExtractor methodExtractor = new MethodExtractor() ;
        List<Method> methods = methodExtractor.extract(file.toPath());
    }


}

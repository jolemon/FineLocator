package extractor;

import org.eclipse.jdt.core.dom.*;

import java.util.List;

/**
 * Extract Method from Java Files
 * Input : project path
 * Output : files in same structure as project, and each line of which is a method,
 *          including method declaration and body.
 */
public class MethodExtractor {


    public static void main(String[] args) {
        String content="method body";

        ASTParser parser = ASTParser.newParser(AST.JLS3);
        parser.setKind(ASTParser.K_COMPILATION_UNIT);     //to parse compilation unit
        parser.setSource(content.toCharArray());          //content is a string which stores the java source
        parser.setResolveBindings(true);

        CompilationUnit result = (CompilationUnit) parser.createAST(null);

        //show class name
        List types = result.types();
        TypeDeclaration typeDec = (TypeDeclaration) types.get(0);
        System.out.println("className:" + typeDec.getName());

        //show methods
        MethodDeclaration methodDec[] = typeDec.getMethods();
        System.out.println("Method:");
        for (MethodDeclaration method : methodDec) {
            //get method name
            SimpleName methodName = method.getName();
            System.out.println("method name:" + methodName);

            //get method parameters
            List param = method.parameters();
            System.out.println("method parameters:" + param);

            //get method return type
            Type returnType = method.getReturnType2();
            System.out.println("method return type:" + returnType);
        }


    }
}

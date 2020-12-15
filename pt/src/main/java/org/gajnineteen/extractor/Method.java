package org.gajnineteen.extractor;

public class Method {

    public String signature ;
    public int startLineNum ;
    public int endLineNum ;
    public String methodStr ;

    public Method(String signature, int startLineNum, int endLineNum, String methodStr){
        this.signature = signature;
        this.startLineNum = startLineNum ;
        this.endLineNum = endLineNum ;
        this.methodStr = methodStr ;
    }

    public void print(){
        System.out.println(signature);
        System.out.println("StartLineNum :" + startLineNum);
        System.out.println("EndLineNum :" + endLineNum);
        System.out.println(methodStr);
    }



}

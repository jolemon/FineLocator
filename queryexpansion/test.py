
ori_name = [
    # 'Math/Math_57/src/main/java/org/apache/commons/math/stat/clustering/KMeansPlusPlusClusterer.java#KMeansPlusPlusClusterer#List<Cluster<T>> chooseInitialCenters(final Collection<T> points, final int k, final Random random)',
    'Closure/Closure_47/src/com/google/javascript/jscomp/SourceMap.java#void addMapping(Node node,FilePosition outputStartPosition,FilePosition outputEndPosition)',
    'Closure/Closure_41/src/com/google/javascript/jscomp/FunctionTypeBuilder.java#FunctionTypeBuilder inferFromOverriddenFunction(@Nullable FunctionType oldType,@Nullable Node paramsParent)',
    'Closure/Closure_41/src/com/google/javascript/jscomp/FunctionTypeBuilder.java#FunctionTypeBuilder inferParameterTypes(@Nullable Node argsParent,@Nullable JSDocInfo info)',
    'Closure/Closure_61/src/com/google/javascript/jscomp/NodeUtil.java#boolean functionCallHasSideEffects(Node callNode,@Nullable AbstractCompiler compiler)',
    'Closure/Closure_144/src/com/google/javascript/jscomp/FunctionTypeBuilder.java#FunctionTypeBuilder inferReturnType(@Nullable JSDocInfo info)',
    'Closure/Closure_144/src/com/google/javascript/jscomp/TypedScopeCreator.java#FunctionType getFunctionType(String name,Node rValue,JSDocInfo info,@Nullable Node lvalueNode)'
]


res_name = [
    # 'Math/Math_57/src/main/java/org/apache/commons/math/stat/clustering/KMeansPlusPlusClusterer.java#KMeansPlusPlusClusterer#List<Cluster<T>> chooseInitialCenters(Collection<T> points,int k,Random random)'
]


# ss_dic_path = '/Users/lienming/FineLocator/expRes/ss/Closure/Closure_41.dic'
# tp_dic_path = '/Users/lienming/FineLocator/expRes/tp/Closure/Closure_41.dic'
#
# from methods_dic import load_dic
# ss_dic = load_dic(ss_dic_path)
# tp_dic = load_dic(tp_dic_path)
#
# for key in tp_dic:
#     if key not in ss_dic:
#         break
#     if tp_dic[key] != ss_dic[key]:
#         print(key)
#         print(tp_dic[key])
#         print(ss_dic[key])
#         print()

res1 = '/src/com/google/javascript/jscomp/FunctionTypeBuilder.java#FunctionTypeBuilder#FunctionTypeBuilder inferParameterTypes(@Nullable Node argsParent,@Nullable JSDocInfo info)'
from handle_cd_method import trim_method
print(res1)
print(trim_method(res1))

from rank import load_link_dic
for proj in ['Closure']: #['Time', 'Mockito', 'Lang', 'Math', 'Closure']:
    file = '/Users/lienming/Downloads/final_defects4j/linked-bugMethods/' + proj + '_bugId_buggyMethodsName'
    dic = load_link_dic(file)
    for item in dic['Closure_41']:
        print(item)
        print(item==trim_method(res1))


import re
import json

function_modifier_list = ['public', 'private', 'final', 'static', 'abstract',
                          'protected', 'synchronized', 'native', 'transient', 'volatie']


def trim_method(ori_method_str):
    return re.sub(r'(@(\w+) )|(public )|(private )|(final )|(static )|(abstract )|(protected )|(synchronized )|(native )|(transient)|(volatie )|( throws(.*))', "", ori_method_str)


def trim_comma_in_paras(method_str):
    return re.sub(r'(,(\s*))', ',', method_str)

def trim_template_T(method_str):
    return re.sub(r'(#<T>)', '#', method_str)

def trim_ss_signature(method_str):
    match_obj = re.search(r'(#(\w+)<\S*>) ', method_str)
    if match_obj is None:
        # 不存在<>，无需修改
        return method_str

    # 存在<>，找到匹配项，用正则表达式去除其中的<>获得替换项，然后在原字符串中把匹配项替换成替换项
    match_str = match_obj.group()
    replace_str = re.sub(r'(<.*>)', '', match_str)
    method_str = method_str.replace(match_str, replace_str)
    return method_str

# def _test_():
#     str1 = '/src/main/java/org/joda/time/MutablePeriod.java#public MutablePeriod(ReadableDuration duration,ReadableInstant endInstant)分/src/main/java/org/joda/time/base/AbstractDateTime.java#public String toString(String pattern,Locale locale) throws IllegalArgumentException'
#     print(trim_method(str1))

# with open('/Users/lienming/FineLocator/expRes/cd/Time/Time_3', 'r') as cd_file:
#     cd_dic = json.loads(cd_file.read())
#     key = "/src/main/java/org/joda/time/chrono/BasicYearDateTimeField.java#BasicYearDateTimeField(BasicChronology chronology)分/src/main/java/org/joda/time/field/ImpreciseDateTimeField.java#ImpreciseDateTimeField(DateTimeFieldType type,long unitMillis)"
#     print(cd_dic[key])
#
# str = 'int[] add(ReadablePartial partial, int fieldIndex, int[] values, int valueToAdd)'
# a = trim_comma_in_paras(str)
# print(a)

# print(trim_ss_signature('/src/main/java/org/apache/commons/lang3/tuple/Pair.java#Pair#Pair<L,R> of(L left,R right)'))
# s = 'stat.StatUtils'
# ent_name_parts = s.split('.')
# class_name = ent_name_parts[0]
# class_method = ent_name_parts[1]
# if class_name.islower(): # is package name
#     class_name = class_method
#     print(class_method)

# print(trim_ss_signature('/src/org/mockito/internal/invocation/finder/AllInvocationsFinder.java#AllInvocationsFinder#List find(List<?> mocks)'))
# print(trim_method('/JodaTime/src/main/java/org/joda/time/Minutes.java#Minutes#Minutes minutes(int minutes)'))
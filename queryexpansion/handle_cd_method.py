import re
import json

function_modifier_list = ['public', 'private', 'final', 'static', 'abstract',
                          'protected', 'synchronized', 'native', 'transient', 'volatie']


def trim_method(ori_method_str):
    return re.sub(r'(@(\w+) )|(public )|(private )|(final )|(static )|(abstract )|(protected )|(synchronized )|(native )|(transient)|(volatie )|( throws(.*))', "", ori_method_str)


def trim_comma_in_paras(method_str):
    return re.sub(r'(,(\s*))', ',', method_str)




def _test_():
    str1 = '/src/main/java/org/joda/time/MutablePeriod.java#public MutablePeriod(ReadableDuration duration,ReadableInstant endInstant)分/src/main/java/org/joda/time/base/AbstractDateTime.java#public String toString(String pattern,Locale locale) throws IllegalArgumentException'
    print(trim_method(str1))

# with open('/Users/lienming/FineLocator/expRes/cd/Time/Time_3', 'r') as cd_file:
#     cd_dic = json.loads(cd_file.read())
#     key = "/src/main/java/org/joda/time/chrono/BasicYearDateTimeField.java#BasicYearDateTimeField(BasicChronology chronology)分/src/main/java/org/joda/time/field/ImpreciseDateTimeField.java#ImpreciseDateTimeField(DateTimeFieldType type,long unitMillis)"
#     print(cd_dic[key])
#
# str = 'int[] add(ReadablePartial partial, int fieldIndex, int[] values, int valueToAdd)'
# a = trim_comma_in_paras(str)
# print(a)
import re

function_modifier_list = ['public', 'private', 'final', 'static', 'abstract',
                          'protected', 'synchronized', 'native', 'transient', 'volatie']


def trim_method(ori_method_str):
    return re.sub(r'(@(\w+) )|(public )|(private )|(final )|(static )|(abstract )|(protected )|(synchronized )|(native )|(transient)|(volatie )|( throws(.*))', "", ori_method_str)


str1 = '/src/main/java/org/joda/time/MutablePeriod.java#public MutablePeriod(ReadableDuration duration,ReadableInstant endInstant)分/src/main/java/org/joda/time/base/AbstractDateTime.java#public String toString(String pattern,Locale locale) throws IllegalArgumentException'
print(trim_method(str1))
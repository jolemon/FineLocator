from methods_dic import load_dic

ss = load_dic('/Users/lienming/FineLocator/expRes/ss/Mockito/Mockito_35.dic')
tp = load_dic('/Users/lienming/FineLocator/expRes/tp/Mockito/Mockito_35.dic')

for key in ss:
    print(key, ss[key], tp[key])
    if ss[key] != tp[key]:
        break
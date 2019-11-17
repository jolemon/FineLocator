import os
for root,dirs,files in os.walk('/Users/lienming/Downloads/test'):
    for file in files:
        if file.endswith('_res'):
            newname = file.replace('_res', '_300_10_811_res')
            ori = os.path.join(root, file)
            new = os.path.join(root, newname)
            os.rename(ori, new)
        else:
            ori = os.path.join(root, file)
            new = os.path.join(root, file+'_300_10_811')
            os.rename(file,file+'_300_10_811')


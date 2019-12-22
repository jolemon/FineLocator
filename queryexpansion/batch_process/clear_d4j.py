from rank import load_link_dic
import os
import shutil

projs = ['Time', 'Mockito', 'Lang', 'Math', 'Closure']
linked_dir = '/Users/lienming/Downloads/final_defects4j/linked-bugMethods/'
linked_postfix = '_bugId_buggyMethodsName'
bugcode_dir = '/Users/lienming/Downloads/final_defects4j/allMethods'
br_dir = '/Users/lienming/Downloads/final_defects4j/bugReport4Vector'


def clear_allMethods():
    for proj in projs:
        link_dic = load_link_dic(linked_dir + proj + linked_postfix)
        for file in os.listdir(os.path.join(bugcode_dir, proj)):
            if file not in link_dic:
                print(os.path.join(bugcode_dir, proj, file))
                shutil.rmtree(os.path.join(bugcode_dir, proj, file))


def clear_br():
    for proj in projs:
        link_dic = load_link_dic(linked_dir + proj + linked_postfix)
        proj_dir = os.path.join(br_dir, proj)
        for br in os.listdir(proj_dir):
            if br not in link_dic:
                print(os.path.join(proj_dir, br))
                os.remove(os.path.join(proj_dir, br))

clear_br()
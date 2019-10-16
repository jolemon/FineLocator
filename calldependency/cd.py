#!/usr/local/bin/python3.7
import sys
sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')
import understand as us
from argparse import ArgumentParser


def add_paras_for_method(method_name, paras):
    if paras is None:
        return str(method_name) + "()"
    else:
        return str(method_name) + "(" + str(paras) + ")"


def get_cd(udb, save_path, filter_file_type = ".java", filter_ref_type = "Call"):
    save_file = open(save_path, 'w')

    for f in udb.ents("File"):
        from_file_name = f.longname(True) # get abs path
        if not str(from_file_name).endswith(filter_file_type):
            continue

        # print("filename : " + fromFileName)
        if filter_ref_type == "Call":
            dic = f.depends()
        else:
            dic = f.dependsby()


        for entKey in dic:
            ref_list = dic[entKey]
            to_file_name = entKey.longname(True)  # get abs path
            for ref in ref_list:
                kindname = ref.kindname()
                if kindname == "Call":   # no matter "Call" or "Callby"
                    line_num = ref.line()

                    from_ent = ref.scope()
                    from_method_paras = from_ent.parameters()
                    from_method_name = add_paras_for_method(method_name = from_ent.simplename(), paras = from_method_paras)

                    to_ent = ref.ent()
                    to_method_paras = to_ent.parameters()
                    to_method_name = add_paras_for_method(method_name = to_ent.simplename(), paras = to_method_paras)
                    if filter_ref_type == "Call":
                        line = from_file_name + '内' + from_method_name + '调用' + to_file_name + '内' + to_method_name + '行' + str(line_num)
                        save_file.write(line+'\n')
                        # print(from_file_name, '内', from_method_name, '调用', to_file_name, '内', to_method_name, '行', line_num)
                    else:
                        line = from_file_name + '内' + from_method_name + '被调' + to_file_name + '内' + to_method_name + '行' + str(line_num)
                        save_file.write(line + '\n')
                        # print(from_file_name, '内', from_method_name, '被调', to_file_name, '内', to_method_name, '行', line_num)

    save_file.close()
    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--udb_path", dest = "udb_path", required = True)
    parser.add_argument("-s", "--save_path", dest = "save_path", required = True)
    args = parser.parse_args()
    udb_path = args.udb_path
    save_path = args.save_path
    print(udb_path)
    db = us.open(udb_path)
    get_cd(udb = db, filter_ref_type = "Call", save_path = save_path)
    # get_cd(udb = db, filter_ref_type = "Callby")
    db.close()
#!/usr/local/bin/python3.7
import sys
sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')
import understand as us


def add_paras_for_method(method_name, paras):
    if paras is None:
        return str(method_name) + "()"
    else:
        return str(method_name) + "(" + str(paras) + ")"


def get_cd(db, filter_file_type = ".java", filter_ref_type = "Call"):
    for f in db.ents("File"):
        fromFileName = f.longname()
        if not str(fromFileName).endswith(filter_file_type):
            continue

        # print("filename : " + fromFileName)
        if filter_ref_type == "Call":
            dic = f.depends()
        else:
            dic = f.dependsby()
        for entKey in dic:
            refList = dic[entKey]
            toFileName = entKey.longname()
            for ref in refList:
                kindname = ref.kindname()
                if kindname == "Call":   # no matter "Call" or "Callby"
                    lineNum = ref.line()

                    fromEnt = ref.scope()
                    fromMethodParas = fromEnt.parameters()
                    fromMethodName = add_paras_for_method(method_name = fromEnt.simplename(), paras = fromMethodParas)

                    toEnt = ref.ent()
                    toMethodParas = toEnt.parameters()
                    toMethodName = add_paras_for_method(method_name = toEnt.simplename(), paras = toMethodParas)
                    if filter_ref_type == "Call":
                        print(fromFileName, '内', fromMethodName, '调用', toFileName, '内', toMethodName, '行', lineNum)
                    else:
                        print(fromFileName, '内', fromMethodName, '被调', toFileName, '内', toMethodName, '行', lineNum)
    return


if __name__ == "__main__":
    db = us.open('Time_3.udb')
    get_cd(db, filter_ref_type = "Call")
    # get_cd(db, filter_ref_type = "Callby")
    db.close()
def add_class(file_path):

    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        new_lines = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            parts = line.split('\t')
            if len(parts) == 1:
                print('length of parts == 1')
                continue

            if '外' not in parts[1]:
                method = parts[1]
                res_method = handle_method(method)
                new_line = parts[0] + '\t' + res_method
                new_lines.append(new_line)
            else:
                methods = parts[1].split('外')
                new_methods = []
                for method in methods:
                    res_method = handle_method(method)
                    new_methods.append(res_method)
                new_line = parts[0] + '\t' + '外'.join(new_methods)
                new_lines.append(new_line)
        f.write('\n'.join(new_lines))




def handle_method(method):
    if '#' in method:
        return method
    else:
        path_and_name = method.split('内')
        javafilename = path_and_name[0].split('/')[-1]
        if '.java' not in javafilename:
            print(javafilename, ' is not .java')
            return method
        else:
            classname = javafilename.replace('.java', '')
            return  path_and_name[0] + '内' + classname + '#' + path_and_name[1]



for proj in ['Time', 'Mockito', 'Lang', 'Math', 'Closure']:
    file = '/Users/lienming/Downloads/final_defects4j/linked-bugMethods/' + proj + '_bugId_buggyMethodsName'
    add_class(file)
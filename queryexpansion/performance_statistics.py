import os
import xlsxwriter

# 一个工作簿是一个项目. 命名 $proj
# 工作簿中，一个表记录一个版本. 命名格式：$dim_$epochs_$abr
# 一个表横向记录该项目下所有$proj_id的结果，


def process_result(output_dir, res_dir, proj_name, dim, epochs, abr):
    output_path = os.path.join(output_dir,proj_name) + '.xlsx'
    workbook = xlsxwriter.Workbook(output_path)
    version = str(dim) + '_' + str(epochs) + '_' + str(abr)
    file_postfix = version + '_res'

    worksheet = workbook.add_worksheet(version)  # 创建工作表

    print('begin calulate performance for :', proj_name + '_*_' + version , '...')
    print('input  dir : ' + res_dir)
    print('output dir : ' + output_path)

    MAP_dic = {}
    MRR_dic = {}
    HIT1_dic = {}
    HIT5_dic = {}
    HIT10_dic = {}
    HIT20_dic = {}

    if not os.path.isdir(res_dir):
        print(str(res_dir) + 'is not a dir')
        return

    # collect
    for file in os.listdir(res_dir):
        if not file.endswith(file_postfix):
            continue

        # print(file)
        file_path = os.path.join(res_dir, file)
        res_file = open(file_path, 'r')

        file_name = file.replace("_"+file_postfix, "")
        while True:
            line = res_file.readline()

            line = line.strip()
            if not line:
                break
            if len(line) > 0:
                line = line.strip()
                if ':' not in line:
                    print(': not in this line.')
                    continue

                parts = line.split(':')
                if len(parts) < 2:
                    print('not a valid line.')
                    continue

                name = parts[0]
                res = parts[1]
                if name == 'MAP':
                    MAP_dic[file_name] = res
                elif name == 'MRR':
                    MRR_dic[file_name] = res
                elif name == 'Hit-1':
                    HIT1_dic[file_name] = res
                elif name == 'Hit-5':
                    HIT5_dic[file_name] = res
                elif name == 'Hit-10':
                    HIT10_dic[file_name] = res
                elif name == 'Hit-20':
                    HIT20_dic[file_name] = res
                else:
                    print('name : ' + name + ' not found in dic!')

        res_file.close()

    begin_row = 0
    # write file

    worksheet.write(begin_row + 0, 0, 'proj_id')
    worksheet.write(begin_row + 1, 0, 'MAP')
    worksheet.write(begin_row + 2, 0, 'MRR')
    worksheet.write(begin_row + 3, 0, 'HIT-1')
    worksheet.write(begin_row + 4, 0, 'HIT-5')
    worksheet.write(begin_row + 5, 0, 'HIT-10')
    worksheet.write(begin_row + 6, 0, 'HIT-20')

    max_dic = {"MAP": [[], 0.0],
               "MRR": [[], 0.0],
               "HIT1": [[], 0.0],
               "HIT5": [[], 0.0],
               "HIT10": [[], 0.0],
               "HIT20": [[], 0.0]
               }

    def update_max(dic, k, v):
        if dic[k][1] < v[1]:
            dic[k][0] = [v[0]]
            dic[k][1] = v[1]
        elif dic[k][1] == v[1]:
            dic[k][0].append(v[0])


    for dic_key in MAP_dic:
    # for column in range(1, len(MAP_dic) + 1):
        dic_key_parts = dic_key.split('_')
        id = dic_key_parts[1]
        column = int(id)
        try:
            worksheet.write(begin_row + 0, column, (str)(dic_key))
            worksheet.write(begin_row + 1, column, (float)(MAP_dic[dic_key]))
            update_max(max_dic, "MAP", [column, (float)(MAP_dic[dic_key])])
            worksheet.write(begin_row + 2, column, (float)(MRR_dic[dic_key]))
            update_max(max_dic, "MRR", [column, (float)(MRR_dic[dic_key])])
            worksheet.write(begin_row + 3, column, (float)(HIT1_dic[dic_key]))
            update_max(max_dic, "HIT1", [column, (float)(HIT1_dic[dic_key])])
            worksheet.write(begin_row + 4, column, (float)(HIT5_dic[dic_key]))
            update_max(max_dic, "HIT5", [column, (float)(HIT5_dic[dic_key])])
            worksheet.write(begin_row + 5, column, (float)(HIT10_dic[dic_key]))
            update_max(max_dic, "HIT10", [column, (float)(HIT10_dic[dic_key])])
            worksheet.write(begin_row + 6, column, (float)(HIT20_dic[dic_key]))
            update_max(max_dic, "HIT20", [column, (float)(HIT20_dic[dic_key])])
        except KeyError:
            print('can not find key!', dic_key)

    bold = workbook.add_format()
    bold.set_bold()
    bold.set_font_color('red')
    if len(max_dic["MAP"][0]) > 0:
        for index in max_dic["MAP"][0]:
            worksheet.write_number(begin_row + 1, index, max_dic["MAP"][1], bold)
    if len(max_dic["MRR"][0]) > 0:
        for index in max_dic["MRR"][0]:
            worksheet.write_number(begin_row + 2, index, max_dic["MRR"][1], bold)
    if len(max_dic["HIT1"][0]) > 0 and max_dic["HIT1"][1] > 0:
        for index in max_dic["HIT1"][0]:
            worksheet.write_number(begin_row + 3, index, max_dic["HIT1"][1], bold)
    if len(max_dic["HIT5"][0]) > 0 and max_dic["HIT5"][1] > 0:
        for index in max_dic["HIT5"][0]:
            worksheet.write_number(begin_row + 4, index, max_dic["HIT5"][1], bold)
    if len(max_dic["HIT10"][0]) > 0 and max_dic["HIT10"][1] > 0:
        for index in max_dic["HIT10"][0]:
            worksheet.write_number(begin_row + 5, index, max_dic["HIT10"][1], bold)
    if len(max_dic["HIT20"][0]) > 0 and max_dic["HIT20"][1] > 0:
        for index in max_dic["HIT20"][0]:
            worksheet.write_number(begin_row + 6, index, max_dic["HIT20"][1], bold)

    workbook.close()

process_result('/Users/lienming',
               '/Users/lienming/Math',
               'Math', 300, 10, 811)

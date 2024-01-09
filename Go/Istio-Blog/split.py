# 将当前路径下名为 01.01.md 按照以 "### " 开头的三级标题拆分成多个 markdown 文件
# 文件按照 01.01.xx.md 递增命名

import os

def split_file(file_name, format_str='### ', prefix_num=2):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        file_num = 0
        for line in lines:
            if line.startswith(format_str):
                file_num += 1
        print('共拆分成 %d 个文件' % file_num)
        file_num = 0
        file_path = os.path.abspath(file_name)
        file_base_name = os.path.basename(file_path)
        file_base_name = file_base_name.split('.')[:prefix_num]
        file_base_name = '.'.join(file_base_name)
        file_base_name = file_base_name + '.'
        if file_num < 10:
            file_name = file_base_name + '0' + str(file_num) + '.md'
        else:
            file_name = file_base_name + str(file_num) + '.md'
        with open(file_name, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith(format_str):
                    file_num += 1
                    if file_num < 10:
                        file_name = file_base_name + '0' + str(file_num) + '.md'
                    else:
                        file_name = file_base_name + str(file_num) + '.md'
                    f.close()
                    f = open(file_name, 'w', encoding='utf-8')
                f.write(line)
        f.close()

if __name__ == '__main__':
    split_file('01.流量管理/01.01.md', format_str='### ', prefix_num=2)
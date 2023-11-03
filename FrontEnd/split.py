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
        file_real_name = '.' + '.'.join(os.path.basename(file_path).split('.')[prefix_num:])
        file_base_name = '.'.join(file_base_name)
        file_base_name = file_base_name + '.'
        if file_num < 10:
            file_name = file_base_name + '0' + str(file_num) + file_real_name
        else:
            file_name = file_base_name + str(file_num) + file_real_name
        with open(file_name, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith(format_str):
                    file_num += 1
                    if file_num < 10:
                        file_name = file_base_name + '0' + str(file_num) + file_real_name
                    else:
                        file_name = file_base_name + str(file_num) + file_real_name
                    f.close()
                    f = open(file_name, 'w', encoding='utf-8')
                f.write(line)
        f.close()

# 将 markdown 文档中的 "标题\n======" 转换成 "# 标题"
# 将 markdown 文档中的 "标题\n------" 转换成 "## 标题"
def convert_title(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('======'):
                lines[i-1] = '# ' + lines[i-1]
                lines[i] = ''
            elif lines[i].startswith('------'):
                lines[i-1] = '## ' + lines[i-1]
                lines[i] = ''
        f.close()
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
        f.close()

if __name__ == '__main__':
    #split_file('MyNote/FrontEnd/VueDoc/guide/01.essentials/01.08.event-handling.md', format_str='## ', prefix_num=2)
    #split_file('MyNote/FrontEnd/ES6/10/10.object.md', format_str='## ', prefix_num=1)
    #os.chdir('MyNote/FrontEnd/JavaScript/06.oop/06.02')
    #split_file('06.02.this.md', format_str='## ', prefix_num=2)
    #split_file('MyNote/FrontEnd/HTML/13/13.form.md', format_str='## ', prefix_num=1)
    
    os.chdir('MyNote/AI/Pytorch速通/01/01.03')
    convert_title('01.03.neural_networks_tutorial.md')
    split_file('01.03.neural_networks_tutorial.md', format_str='## ', prefix_num=2)

    #os.chdir('MyNote/FrontEnd/CSS/10')
    #os.chdir('MyNote/FrontEnd/CSS/02.selectors/02.03')
    #split_file('10.grid.md', format_str='## ', prefix_num=2)
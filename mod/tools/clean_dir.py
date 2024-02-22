import os


def clean_dir(path, filetype):
    file_list = [i for i in os.listdir(path) if i.endswith(filetype)]
    if len(file_list)!=0:
        for i in file_list:
            file = os.path.abspath(os.path.join(path,i))
            print("删除",file,".....")
            os.remove(file)
if __name__ == '__main__':
    clean_dir('../../bin','.out')
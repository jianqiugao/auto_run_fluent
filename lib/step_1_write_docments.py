from docx import Document
import os
from mod.docfun.write_title import write_title
from mod.read_config import _load_yaml
from mod.docfun.write_ref import write_ref
from mod.docfun.write_post_frame import write_post_frame
from mod import parents_path

promts = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))
work_condition_params = {'壁面参数': None, "入口参数": None, "出口参数": None, "加速度参数": None, "液位参数": None, "时间参数": None}
order_params = {'名称参数':None,"编号参数":None}

def write_docments(run_dir:str):
    # 创建一个新的Word文档对象
    document = Document()
    num = write_title(promts['title'],document)
    num = write_ref(document,num,parents_path)
    write_post_frame(document,num,work_condition_params,order_params,parents_path,run_dir)

    document.save(os.path.abspath(os.path.join(parents_path,f'run/{run_dir}/output_file/{run_dir}.docx')))


if __name__ == '__main__':
    write_docments('20240201_215030')

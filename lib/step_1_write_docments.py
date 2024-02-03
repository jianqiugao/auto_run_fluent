from docx import Document
import os

from mod.docfun.write_results import write_results
from mod.docfun.write_sumary import write_summary
from mod.docfun.write_title import write_title
from mod.read_config import _load_yaml
from mod.docfun.write_ref import write_ref
from mod.docfun.write_post_frame import write_post_frame
from mod import parents_path
import pandas as pd

promts = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))
work_condition_params = {'壁面参数': None, "入口参数": None, "出口参数": None, "加速度参数": None, "液位参数": None, "时间参数": None}
order_params = {'名称参数': None, "编号参数": None}
df = pd.DataFrame({'截面平均升压速率Pa/s': [1, 2, 3,5]},index=[f'截面1','截面2','截面3','截面4'])
sus_t = pd.DataFrame({'维持时间t': [1, 2, 3,5],'初始时刻截面平均压力Pa': [1, 2, 3,5]},index=[f'截面1','截面2','截面3','截面4'])

time_cost = 12

def write_docments(run_dir: str):
    # 创建一个新的Word文档对象
    document = Document()
    num = write_title(promts['title'], document)
    num = write_ref(document, num, parents_path)
    num = write_post_frame(document, num, work_condition_params, order_params, parents_path, run_dir)
    num = write_results(document,num,df,sus_t,time_cost)
    write_summary(document,run_dir,num,promts)

    document.save(os.path.abspath(os.path.join(parents_path, f'run/{run_dir}/output_file/{run_dir}.docx')))


if __name__ == '__main__':
    write_docments('20240201_215030')

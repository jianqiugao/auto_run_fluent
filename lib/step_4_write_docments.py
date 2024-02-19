from docx import Document
import os

from mod.docfun.write_results import write_results
from mod.docfun.write_sumary import write_summary
from mod.docfun.write_title import write_title
from mod.tools.read_config import _load_yaml
from mod.docfun.write_ref import write_ref
from mod.docfun.write_post_frame import write_post_frame
from mod import parents_path
import pandas as pd
import numpy as np

promts = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))
config = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/config.yaml')))
promts.update({"DateFormate": config["DateFormate"]})



def write_docments(run_dir: str,work_condition_params,pressure_up_rate,sus_t):
    # 创建一个新的Word文档对象
    sus_time = sus_t['维持时间t'].mean()
    document = Document()
    num = write_title(promts['title'], document)
    num = write_ref(document, num, parents_path)
    num = write_post_frame(document, num, work_condition_params, order_params, parents_path, run_dir)
    num = write_results(document, num, pressure_up_rate, sus_t, run_time_cost)
    write_summary(document, run_dir, num, promts, press_up, temp_diff, average_press, sus_time, run_time_cost)

    document.save(os.path.abspath(os.path.join(parents_path, f'run/{run_dir}/output_file/{run_dir}.docx')))


if __name__ == '__main__':
    work_condition_params = {'壁面参数': None, "入口参数": None, "出口参数": None, "加速度参数": None, "液位参数": None,"时间参数": None}
    order_params = {'名称参数': None, "编号参数": None}
    #
    # # -----------------------这下面逻辑有一些混乱，一定是有一些是一件事------------------------------------
    #
    # data = np.random.random((5, 20))
    # gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间
    # # xz 平面的温度/压力时间图
    # averge_press_on_xz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
    #                                        columns=[f't{i}' for i in range(data.shape[1])])
    # averge_temp_on_xz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
    #                                       columns=[f't{i}' for i in range(data.shape[1])])
    # # yz 平面的温度/压力时间图
    # averge_press_on_yz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
    #                                        columns=[f't{i}' for i in range(data.shape[1])])
    # averge_temp_on_yz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
    #                                       columns=[f't{i}' for i in range(data.shape[1])])
    # gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
    #                                columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])
    #
    # # =======================》由前面的参数计算得到 todo
    pressure_up_rate = pd.DataFrame({'截面平均升压速率Pa/s': [1, 2, 3, 5]}, index=[f'截面1', '截面2', '截面3', '截面4'])
    sus_t = pd.DataFrame({'维持时间t': [1, 2, 3, 5], '初始时刻截面平均压力Pa': [1, 2, 3, 5]},
                         index=[f'截面1', '截面2', '截面3', '截面4'])
    #
    # # 液体体积/质量 -时间图
    #
    # press_up = [0.1, 0.3, 0.5, 0.6]
    # temp_diff = [0.1, 0.3, 0.5, 0.6]
    # average_press = [0.1, 0.3, 0.5, 0.6]
    # sus_time = 20  # 维持时间
    run_time_cost = 99

    write_docments('20240201_215030',work_condition_params,pressure_up_rate,sus_t,run_time_cost)

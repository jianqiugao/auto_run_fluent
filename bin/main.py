import datetime
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0,os.path.abspath(os.getcwd()+'/..'))
from lib import promts, config
from lib.step_0_check_file_system import make_dirs
from lib.step_1_run_fluent import run_fluent_get_picture_and_data, fluent_data_to_pandas
from lib.step_3_draw_picture import draw_picture_by_fluent_data
from lib.step_4_write_docments import write_docments


work_condition_params = {'壁面参数': None, "入口参数": None, "出口参数": None, "加速度参数": None, "液位参数": None,
                         "时间参数": None}
order_params = {'名称参数': None, "编号参数": None}


def main(date, mesh, gas_liquid_time):
    run_dir = make_dirs(date=date)
    run_time_cost = run_fluent_get_picture_and_data(run_dir, mesh)
    averge_press_on_xz_clip, averge_temp_on_xz_clip, averge_press_on_yz_clip, averge_temp_on_yz_clip = fluent_data_to_pandas()
    draw_picture_by_fluent_data(averge_press_on_xz_clip,
                                averge_temp_on_xz_clip,
                                averge_press_on_yz_clip,
                                averge_temp_on_yz_clip,
                                gas_liquid_time,
                                run_dir)
    columns = averge_press_on_yz_clip.columns
    run_time_model = config['time_step_size'] * (len(averge_press_on_yz_clip.columns) - 1)
    data = {'截面平均升压速率Pa/s': ((averge_press_on_yz_clip.iloc[:, -1] - averge_press_on_yz_clip.iloc[:,
                                                                            -2]).values / run_time_model).tolist()}
    index = [f'截面{i}' for i in range(1, len(averge_press_on_yz_clip.index) + 1)]
    pressure_up_rate = pd.DataFrame(data=data, index=index)

    res = [
        len(columns) - 1 if np.where(averge_press_on_yz_clip.loc[i, :].values > config['sus_p'])[0].shape[0] == 0 else
        np.where(averge_press_on_yz_clip.loc[i, :].values > config['sus_p'])[0][0] for i in
        averge_press_on_yz_clip.index]
    data = {'维持时间t': [i * config['time_step_size'] for i in res],
            '初始时刻截面平均压力Pa': averge_press_on_yz_clip.iloc[:, 0].values.tolist()}

    sus_t = pd.DataFrame(data=data, index=index)
    temp_diff = averge_temp_on_yz_clip.iloc[:, -1].values.tolist()  # 最后一个时刻的温度
    average_press = averge_press_on_yz_clip.iloc[:, -1].values.tolist()  # 最后一个时刻的压力
    write_docments(run_dir, work_condition_params, order_params, pressure_up_rate, sus_t, run_time_cost, temp_diff, average_press)


if __name__ == '__main__':
    date = datetime.datetime(year=2024, month=2, day=12, hour=12, minute=10, second=20)
    mesh = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"
    # 液体体积/质量 -时间图
    gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间
    gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
                                   columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])
    main(date, mesh=mesh, gas_liquid_time=gas_liquid_time)

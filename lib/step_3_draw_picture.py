import numpy as np
import pandas as pd
from mod import parents_path
from mod.tools.plot_figure import plot_gas_liquid_time, plot_temp_pres


def draw_picture_by_fluent_data(averge_press_on_xz_clip,
                                averge_temp_on_xz_clip,
                                averge_press_on_yz_clip,
                                averge_temp_on_yz_clip,
                                gas_liquid_time,
                                run_dir
                                ):
    temp_press_dict = {'averge_press_on_xz_clip': averge_press_on_xz_clip,
                       'averge_temp_on_xz_clip': averge_temp_on_xz_clip,
                       'averge_press_on_yz_clip': averge_press_on_yz_clip,
                       'averge_temp_on_yz_clip': averge_temp_on_yz_clip}
    plot_temp_pres(temp_press_dict, f'{parents_path}/run/{run_dir}/')
    plot_gas_liquid_time(gas_liquid_time, f'{parents_path}/run/{run_dir}/')
    pass


if __name__ == '__main__':
    data = np.random.random((5, 20))
    gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间
    # 液体体积/质量 -时间图
    gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
                                   columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])
    # xz 平面的温度/压力时间图
    averge_press_on_xz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                           columns=[f't{i}' for i in range(data.shape[1])])
    averge_temp_on_xz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                          columns=[f't{i}' for i in range(data.shape[1])])
    # yz 平面的温度/压力时间图
    averge_press_on_yz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                           columns=[f't{i}' for i in range(data.shape[1])])
    averge_temp_on_yz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                          columns=[f't{i}' for i in range(data.shape[1])])

    draw_picture_by_fluent_data(averge_press_on_xz_clip,
                                averge_temp_on_xz_clip,
                                averge_press_on_yz_clip,
                                averge_temp_on_yz_clip,
                                gas_liquid_time,
                                '20240201_215030')
    print(parents_path)

import datetime
import pandas as pd
import numpy as np
from lib import promts, config
from lib.step_0_check_file_system import make_dirs
from lib.step_1_run_fluent import run_fluent_get_picture_and_data, fluent_data_to_pandas
from lib.step_3_draw_picture import draw_picture_by_fluent_data


def main(date,run_dir,mesh,gas_liquid_time):
    make_dirs(date=date)
    run_fluent_get_picture_and_data(run_dir, mesh)
    averge_press_on_xz_clip, averge_temp_on_xz_clip, averge_press_on_yz_clip, averge_temp_on_yz_clip = fluent_data_to_pandas()
    draw_picture_by_fluent_data(averge_press_on_xz_clip,
                                averge_temp_on_xz_clip,
                                averge_press_on_yz_clip,
                                averge_temp_on_yz_clip,
                                gas_liquid_time,
                                run_dir)
    pass


if __name__ == '__main__':
    date = datetime.datetime(year=2024, month=2, day=12, hour=12, minute=10, second=20)
    run_dir = '20240201_215030'
    mesh = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"
    # 液体体积/质量 -时间图
    gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间
    gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
                                   columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])
    main(date,run_dir=run_dir,mesh=mesh,gas_liquid_time=gas_liquid_time)

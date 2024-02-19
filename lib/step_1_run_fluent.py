import pandas as pd
import numpy as np
import time

from mod import parents_path
from lib import config
from mod.fluntapi.fluentapi import initial_fluent, read_mesh_or_case, define_boundary_and_models, initial_and_calculate, \
    define_data_query_and_post

def fluent_out_file_to_pandas(path):
    xz_clip_pressure_data = []
    with open(path, 'r') as f:
        res = f.readlines()
        for item in res:
            if item[0].isdigit():
                xz_clip_pressure_data.append(item.strip().split(" "))
    xz_clip_pressure_data = np.array(xz_clip_pressure_data).astype(np.float32)[:, 1:].transpose()
    averge_press_on_xz_clip = pd.DataFrame(xz_clip_pressure_data,
                                           index=[f'clip{i + 1}' for i in range(xz_clip_pressure_data.shape[0])],
                                           columns=[f't{i}' for i in range(xz_clip_pressure_data.shape[1])])  # 平均压力on y
    return averge_press_on_xz_clip


def run_fluent_get_picture_and_data(run_dir, import_filename):
    t1 = time.perf_counter()
    solver = initial_fluent(config)
    coordinate_content = read_mesh_or_case(import_filename, solver)
    walls = define_boundary_and_models(config, solver)
    initial_and_calculate(config, solver, coordinate_content)
    define_data_query_and_post(config, solver, coordinate_content, walls, parents_path, run_dir)
    t2 = time.perf_counter()
    print("用时", t2 - t1, "s")


def fluent_data_to_pandas():
    averge_press_on_xz_clip = fluent_out_file_to_pandas('yclip_file_pre.out')  # 平均温度 on y
    averge_temp_on_xz_clip = fluent_out_file_to_pandas('yclip_file_temp.out')  # 平均温度 on y
    averge_press_on_yz_clip = fluent_out_file_to_pandas('xclip_file_pre.out')  # 平均压力 on x
    averge_temp_on_yz_clip = fluent_out_file_to_pandas('xclip_file_temp.out')  # 平均温度 on x

    return averge_press_on_xz_clip, averge_temp_on_xz_clip, averge_press_on_yz_clip, averge_temp_on_yz_clip


# 读取参数配置文件的数据

# solver.tui.solve.report_definitions.add('bbb','lift','thread-names', 'wing_up','wing_down','()','force-vector','0.2', '0.6')
# solver.file.read(file_type="case", file_name=import_filename)

# #定义残差检测
# solver.tui.solve.monitors.residual.check_convergence('yes','no','no','no','no','no')
# solver.tui.solve.monitors.residual.convergence_criteria('1e-7')
# solver.tui.solve.monitors.residual.monitor('yes','yes','yes','yes','yes','yes')
# solver.tui.solve.monitors.residual.plot("yes")
# solver.tui.solve.monitors.residual.print("yes")

# solver.solution.run_calculation.iterate(iter_count=5)


if __name__ == '__main__':
    run_dir = '20240201_215030'
    mesh = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"
    run_fluent_get_picture_and_data(run_dir, mesh)
    averge_press_on_xz_clip, averge_temp_on_xz_clip, averge_press_on_yz_clip, averge_temp_on_yz_clip = fluent_data_to_pandas()

from mod import parents_path
from lib import config
from mod.fluntapi.fluentapi import initial_fluent, read_mesh_or_case, define_boundary_and_models,initial_and_calculate,define_data_query_and_post

import time

run_dir = '20240201_215030'
# 读取参数配置文件的数据
t1 = time.perf_counter()
data_all = []
solver = initial_fluent(config)

import_filename = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"
coordinate_content = read_mesh_or_case(import_filename, solver)
walls = define_boundary_and_models(config, solver)
initial_and_calculate(config, solver,coordinate_content)
define_data_query_and_post(config, solver,coordinate_content,walls,parents_path,run_dir)
# solver.tui.solve.report_definitions.add('bbb','lift','thread-names', 'wing_up','wing_down','()','force-vector','0.2', '0.6')
# solver.file.read(file_type="case", file_name=import_filename)

# #定义残差检测
# solver.tui.solve.monitors.residual.check_convergence('yes','no','no','no','no','no')
# solver.tui.solve.monitors.residual.convergence_criteria('1e-7')
# solver.tui.solve.monitors.residual.monitor('yes','yes','yes','yes','yes','yes')
# solver.tui.solve.monitors.residual.plot("yes")
# solver.tui.solve.monitors.residual.print("yes")

# solver.solution.run_calculation.iterate(iter_count=5)
t2 = time.perf_counter()

print("用时", t2 - t1, "s")

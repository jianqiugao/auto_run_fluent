from mod import parents_path
from lib import config
from mod.fluntapi.fluentapi import initial_fluent, read_mesh_or_case, define_boundary_and_models

import time
# import ansys.fluent.core as pyfluent\
# session = pyfluent.launch_fluent()
# print(session.__dict__)
# # session.check_health()
# print(parents_path)
# import_filename = "chao54-DUIBI01417.cas"
# # fluent启动界面，2d双精度，4核，mode="solver"求解模式，show_gui=True同步显示fluent

# # 读入网格
# solver.file.read(file_type="case", file_name=import_filename)
# # 检查网格
# res = solver.tui.mesh.check()
#
# print(type(res))

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from matplotlib import pyplot
import os, sys
import csv
import math
import pandas as pd
import numpy as np

# 读取参数配置文件的数据
t1 = time.perf_counter()
data_all = []
solver = initial_fluent(config)

import_filename = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"
read_mesh_or_case(import_filename, solver)
define_boundary_and_models(config, solver)
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

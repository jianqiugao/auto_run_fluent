from mod import parents_path

# import ansys.fluent.core as pyfluent

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

#读取参数配置文件的数据
data_all=[]
# with open('data.csv','r',encoding='utf-8') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         data_all.append(row)

solver = pyfluent.launch_fluent(version="3d", precision="double",processor_count=4, show_gui=True, mode="solver")
import_filename = "chao54-DUIBI01417.cas"
# solver.tui.solve.report_definitions.add('bbb','lift','thread-names', 'wing_up','wing_down','()','force-vector','0.2', '0.6')
solver.file.read(file_type="case", file_name=import_filename)

# #定义残差检测
# solver.tui.solve.monitors.residual.check_convergence('yes','no','no','no','no','no')
# solver.tui.solve.monitors.residual.convergence_criteria('1e-7')
# solver.tui.solve.monitors.residual.monitor('yes','yes','yes','yes','yes','yes')
# solver.tui.solve.monitors.residual.plot("yes")
# solver.tui.solve.monitors.residual.print("yes")

solver.solution.run_calculation.iterate(iter_count=20)
import os
import numpy as np
import ansys.fluent.core as pyfluent
from ansys.fluent.core.solver.settings_231.piecewise_polynomial_child import piecewise_polynomial_child, minimum_cls, \
    maximum_cls, number_of_coefficients_cls, coefficients_cls
import subprocess


def initial_fluent(config):
    solver = pyfluent.launch_fluent(version=config["fluent_version"], precision=config["precision"],
                                    processor_count=config['processor_count'],
                                    show_gui=config["show_gui"], mode=config["mode"])
    return solver


# /display/hardcopy pressure_contour-123.jpg

def read_mesh_or_case(path: str, solver):
    if path.endswith('msh'):
        solver.file.read(file_type="mesh", file_name=path)
    else:
        solver.file.read(file_type="case", file_name=path)

    solver.mesh.check()  # 确保检查网格的日志打印了出来
    file_folder = [file for file in os.listdir() if file.endswith('trn')]
    coordinate_content = {}
    try:
        with open(file_folder.pop(-1), "r") as f:
            i = 0
            while True:
                res = f.readline()
                if 'x-coordinate' in res:
                    res = res.split('=')[1:]
                    min_x = float(res[0].split(',')[0].strip())
                    max_x = float(res[1].strip())
                    coordinate_content.update({'min_x': min_x})
                    coordinate_content.update({'max_x': max_x})
                if 'y-coordinate' in res:
                    res = res.split('=')[1:]
                    min_y = float(res[0].split(',')[0].strip())
                    max_y = float(res[1].strip())
                    coordinate_content.update({'min_y': min_y})
                    coordinate_content.update({'max_y': max_y})
                if 'z-coordinate' in res:
                    res = res.split('=')[1:]
                    min_z = float(res[0].split(',')[0].strip())
                    max_z = float(res[1].strip())
                    coordinate_content.update({'min_z': min_z})
                    coordinate_content.update({'max_z': max_z})
                    break
                if i > 200:
                    break
                i = i + 1
    except:
        print("无法获取模型的尺寸信息。。。。。")
    return coordinate_content


def define_boundary_and_models(config, solver):
    solver.setup.models.energy.enabled = config['energy_equation']
    solver.setup.models.viscous.k_omega_model = config['viscous']
    solver.setup.models.viscous.k_omega_options.kw_low_re_correction = False
    solver.setup.models.viscous.options.viscous_heating = False
    solver.setup.general.gravity.enable = config['gravity']
    solver.setup.general.gravity.components = config['gravity_value']
    solver.setup.general.solver.time = config['time']
    # solver.setup.materials.list_materials()
    solver.setup.materials.fluid['air'].density.option = 'real-gas-peng-robinson'
    para_dict = config['cp']
    solver.setup.materials.fluid['air'].specific_heat.option = 'piecewise-polynomial'
    solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial.resize(para_dict['num'])
    solver.execute_tui('define/operating-conditions/operating-density? yes 0')

    for i in range(para_dict['num']):
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].minimum = para_dict['minimum'][i]
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].maximum = para_dict['maximum'][i]
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].number_of_coefficients = \
            para_dict['number_of_coefficients'][i]
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].coefficients = \
            para_dict['coefficients'][i]
    solver.setup.materials.fluid['air'].thermal_conductivity.value = config['thermal_conductivity']
    solver.setup.materials.fluid['air'].viscosity.value = config['viscosity']
    solver.setup.materials.fluid['air'].molecular_weight.value = config['molecular_weight']
    solver.setup.materials.fluid['air'].formation_entropy.value = config['formation_entropy']
    solver.setup.materials.fluid['air'].reference_temperature.value = config['reference_temperature']
    solver.setup.materials.fluid['air'].critical_temperature.value = config['critical_temperature']
    solver.setup.materials.fluid['air'].critical_pressure.value = config['critical_pressure']
    solver.setup.materials.fluid['air'].critical_volume.value = config['critical_volume']
    solver.setup.materials.fluid['air'].acentric_factor.value = config['acentric_factor']

    walls = solver.setup.boundary_conditions.wall.get_object_names()  # 找到所有的壁面

    solver.setup.boundary_conditions.wall['wall-feng-l'].q.value = config['wall-feng-l']
    solver.setup.boundary_conditions.wall['wall-feng-l:004'].q.value = config['wall-feng-l:004']
    solver.setup.boundary_conditions.wall['wall-feng-r'].q.value = config['wall-feng-r']
    solver.setup.boundary_conditions.wall['wall-inpipe'].q.value = config['wall-inpipe']
    solver.setup.boundary_conditions.wall['wall-l'].q.value = config['wall-l']
    solver.setup.boundary_conditions.wall['wall-outpipe-inner'].q.value = config['wall-outpipe-inner']

    solver.setup.boundary_conditions.wall['wall-pipe-outter'].q.value = config['wall-pipe-outter']
    solver.setup.boundary_conditions.wall['wall-pipe-top'].q.value = config['wall-pipe-top']
    solver.setup.boundary_conditions.wall['wall-r'].q.value = config['wall-r']
    solver.setup.reference_values.zone = 'tankgas'
    return walls


def initial_and_calculate(config, solver,coordinate_content):
    solver.solution.initialization.set_defaults['pressure'] = config['initial_press']
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.transient_controls.time_step_count = config['time_step_count']
    solver.solution.run_calculation.transient_controls.time_step_size = config['time_step_size']

    # 获取关键时刻的数据，也就是做几个切面然后再把每个切面上的压力这些给统计一下
    # 统计yz平面
    num_of_plane = 6
    space_x = (coordinate_content['max_x'] - coordinate_content['min_x']) / num_of_plane
    space_x = np.linspace(coordinate_content['min_x'] + space_x, coordinate_content['max_x'] - space_x,
                          num_of_plane).tolist()
    for num, item in enumerate(space_x):
        solver.tui.surface.iso_surface("x-coordinate", f"xclip{num}", (), "fluid-1", (), f"{item}", (), 'q')
        # 定义这个切面的类型
        # solver.solution.report_definitions.surface[f'xclip{num}'].report_type = "surface_facetavg"
        # solver.solution.report_definitions.surface[f'xclip{num}'] = {"field": "pressure",
        #                                                                     "surface_names": [f"xclip{num}"]}

        solver.tui.solve.report_definitions.add(f"xclip{num}_pre", "surface-areaavg", "field", "pressure",
                                                "surface-names", [f"xclip{num}"], "q")
        solver.tui.solve.report_definitions.add(f"xclip{num}_temp", "surface-areaavg", "field", "temperature",
                                                "surface-names", [f"xclip{num}"], "q")
        # # 定义这个切面的文件
    solver.solution.monitor.report_files[f'xclip_file_pre'] = {"report_defs": [f'xclip{i}_pre' for i in range(len(space_x))]}
    solver.solution.monitor.report_files[f'xclip_file_pre'].file_name = "xclip_file_pre.out"

    solver.solution.monitor.report_files[f'xclip_file_temp'] = {"report_defs": [f'xclip{i}_temp' for i in range(len(space_x))]}
    solver.solution.monitor.report_files[f'xclip_file_temp'].file_name = "xclip_file_temp.out"

    # 统计xz平面
    space_y = (coordinate_content['max_y'] - coordinate_content['min_y']) / num_of_plane
    space_y = np.linspace(coordinate_content['min_y'] + space_y, coordinate_content['max_y'] - space_y,
                          num_of_plane).tolist()
    for num, item in enumerate(space_y):
        solver.tui.surface.iso_surface("y-coordinate", f"yclip{num}", (), "fluid-1", (), f"{item}", (), 'q')
        solver.tui.solve.report_definitions.add(f"yclip{num}_pre", "surface-areaavg", "field", "pressure",
                                                "surface-names", [f"yclip{num}"], "q")
        solver.tui.solve.report_definitions.add(f"yclip{num}_temp", "surface-areaavg", "field", "temperature",
                                                "surface-names", [f"yclip{num}"], "q")

    solver.solution.monitor.report_files[f'yclip_file_pre'] = {"report_defs": [f'yclip{i}_pre' for i in range(len(space_y))]}
    solver.solution.monitor.report_files[f'yclip_file_pre'].file_name="yclip_file_pre.out"

    solver.solution.monitor.report_files[f'yclip_file_temp'] = {"report_defs": [f'yclip{i}_temp' for i in range(len(space_y))]}
    solver.solution.monitor.report_files[f'yclip_file_temp'].file_name = "yclip_file_temp.out"
    # solver.tui.file
    solver.solution.run_calculation.calculate()


def define_data_query_and_post(config, solver, coordinate_content, walls,parents_path,run_dir):
    solver.results.graphics.contour['contour-temp'] = {"field": "pressure",
                                                       "surfaces_list": walls}
    solver.results.graphics.contour['contour-temp'].display()
    picture = os.path.abspath(os.path.join(parents_path, f'run/{run_dir}/last_pre_conture.png'))
    # 保存最后一个时刻的压力云图
    if os.path.exists(picture):
        os.remove(picture)
    solver.tui.display.save_picture(picture)
    print('hello')


import os
import re
import ansys.fluent.core as pyfluent
from ansys.fluent.core.solver.settings_231.piecewise_polynomial_child import piecewise_polynomial_child, minimum_cls, \
    maximum_cls, number_of_coefficients_cls, coefficients_cls
import subprocess


def initial_fluent(config):
    solver = pyfluent.launch_fluent(version=config["fluent_version"], precision=config["precision"],
                                    processor_count=config['processor_count'],
                                    show_gui=config["show_gui"], mode=config["mode"])
    return solver


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
    # solver.tui.define("operating_conditions","operating_density?",'yes',"0.1")

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


def define_data_query():
    pass


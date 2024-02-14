import ansys.fluent.core as pyfluent
from ansys.fluent.core.solver.settings_231.piecewise_polynomial_child import piecewise_polynomial_child,minimum_cls,maximum_cls,number_of_coefficients_cls,coefficients_cls




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
    solver.tui.mesh.check()


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
    for i in range(para_dict['num']):
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].minimum = para_dict['minimum'][i]
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].maximum = para_dict['maximum'][i]
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].number_of_coefficients = para_dict['number_of_coefficients'][i]
        solver.setup.materials.fluid['air'].specific_heat.piecewise_polynomial[i].coefficients = para_dict['coefficients'][i]
    solver.setup.materials.fluid['air'].thermal_conductivity.value = config['thermal_conductivity']
    solver.setup.materials.fluid['air'].viscosity.value = config['viscosity']
    solver.setup.materials.fluid['air'].molecular_weight.value = config['molecular_weight']
    solver.setup.materials.fluid['air'].formation_entropy.value = config['formation_entropy']
    solver.setup.materials.fluid['air'].reference_temperature.value = config['reference_temperature']
    solver.setup.materials.fluid['air'].critical_temperature.value = config['critical_temperature']
    solver.setup.materials.fluid['air'].critical_pressure.value = config['critical_pressure']
    solver.setup.materials.fluid['air'].critical_volume.value = config['critical_volume']
    solver.setup.materials.fluid['air'].acentric_factor.value = config['acentric_factor']

    walls = solver.setup.boundary_conditions.wall.get_object_names()

    solver.setup.boundary_conditions.wall['wall-feng-l'].q.value = 1.5
    solver.setup.boundary_conditions.wall['wall-feng-l:004'].q.value = 1.5
    solver.setup.boundary_conditions.wall['wall-feng-r'].q.value = 1.5
    solver.setup.boundary_conditions.wall['wall-inpipe'].q.value = 0.45
    solver.setup.boundary_conditions.wall['wall-l'].q.value = 1.5
    solver.setup.boundary_conditions.wall['wall-outpipe-inner'].q.value = 0.45

    solver.setup.boundary_conditions.wall['wall-pipe-outter'].q.value = 0.45
    solver.setup.boundary_conditions.wall['wall-pipe-top'].q.value = 0.45
    solver.setup.boundary_conditions.wall['wall-r'].q.value = 1.5









    print('hello')

    pass

import time

import fastapi
import uvicorn
from fastapi import FastAPI
import numpy as np
import pandas as pd
import datetime
from pydantic import BaseModel
import os

from main import main
from mod.tools.clean_dir import clean_dir
from lib import config,promts


class Params(BaseModel):
    fluent_version: str = "3d"
    precision: str = "double"
    processor_count: int = 6
    show_gui: bool = True
    mode: str = "solver"
    energy_equation: bool = True
    viscous: str = 'sst'
    gravity: bool = True
    time: str = 'unsteady-1st-order'  # ['steady', 'unsteady-1st-order', 'unsteady-2nd-order', 'unsteady-2nd-order-bounded']

    thermal_conductivity: float = 0.152
    viscosity: float = 1.99e-05
    molecular_weight: float = 4.0026
    formation_entropy: float = 126029.4
    reference_temperature: float = 298.15
    critical_temperature: float = 5.3
    critical_pressure: float = 229000
    critical_volume: float = 0.014441
    acentric_factor: float = -0.39

    wall_feng_l: float = 1.5
    wall_feng_l__004: float = 1.5
    wall_feng_r: float = 1.5
    wall_inpipe: float = 0.45
    wall_l: float = 1.5
    wall_outpipe_inner: float = 0.45
    wall_pipe_outter: float = 0.45
    wall_pipe_top: float = 0.45
    wall_r: float = 1.5

class GeoParams(BaseModel):
    Save_Path:str =  "C:/Users/tianp/Desktop/show"
    radius: float = 4600
    The_radius_of_the_left_fillet_of_the_transition_segment: float = 460
    The_radius_of_the_right_fillet_of_the_transition_segment: float =460
    Total_length_of_barrel_including_head: float = 15000
    Barrel_diameter: float = 4600
    Bore_diameter: float = 311
    Inner_bore_length: float = 2500
    Return_trachea_coordinates: str = "1800 500"
    Inner_diameter_of_the_return_tube: float = 70
    Outer_diameter_of_the_return_tube: float = 90
    Return_tube_length: float = 7940
    Return_pipe_elbow_radius: float = 100
    Return_tube_jacking_length: float =100
    Intake_pipe_coordinates: str = "-1800 -200"
    Inner_diameter_of_the_inlet_pipe: float =43.1
    Outer_diameter_of_the_intake_tube: float = 50.1
    Intake_pipe_length: float= 5700
    The_height_of_the_anti_wave_plate: float = 400
    Thickness_of_the_wave_proof_plate: float = 8
    Diameter_of_the_inner_hole_of_the_wave_protection_plate: float = 800
    Boss_height: float = 39
    Cone_outer_diameter: float = 2000,
    Inner_ring_diameter: float = 3800,
    Incision_height_one_side: float =900,
    Position_of_the_shield_plate: float = 3560,
    Boss_direction: float = 180,
    Spherical_radius_of_the_left_head_of_the_shell: float = 4716,
    Spherical_spherical_center_of_the_left_head_of_the_shell: float = 100,
    Spherical_radius_of_the_right_head_of_the_shell: float = 4716,
    Spherical_spherical_center_of_the_right_head_of_the_shell: float = 200,
    The_left_head_of_the_housing_is_over_rounded_with_a_corner_radius: float = 491,
    The_right_head_of_the_housing_is_over_fillet_radius: float = 491,
    Thickness_of_the_shell_barrel_straight_pipe_section: float = 8,
    The_minimum_size_of_the_polygon_mesh: float = 1,
    The_maximum_size_of_the_polygon_mesh: float = 40,
    The_number_of_layers_of_boundaries: float = 5,
    The_height_of_the_first_layer_of_the_boundary_layer: float = 0.5,
    The_maximum_size_of_the_volume_mesh: float = 40


app = FastAPI()
gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间
gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
                               columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])
# date = datetime.datetime(year=2024, month=2, day=12, hour=12, minute=10, second=20)
date = datetime.datetime.now()
mesh = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"




@app.post('/runfluent/', description='')
async def runfluent(params: Params):
    print(params.dict())
    config.update(params.dict())
    if os.path.exists('run_status.csv'):
        run_status = pd.read_csv('run_status.csv')
    else:
        run_status = pd.DataFrame(columns=["start_time", "end_time", "running_status"])  # run_status
        run_status.to_csv("run_status.csv", index=False)
    if len(run_status) != 0:
        print("上一步计算状态", run_status.iloc[-1, -1])
        if run_status.iloc[-1, -1] == "running":
            return {"message": "上次计算未完成请等待并不要重复提交"}
    run_status.loc[len(run_status)] = [datetime.datetime.now(), "", "running"]
    run_status.to_csv("./run_status.csv", index=False)
    # time.sleep(60)
    clean_dir('.', 'out')
    clean_dir('.', 'trn')
    main(date, mesh=mesh, gas_liquid_time=gas_liquid_time)
    run_status.loc[len(run_status) - 1, ["end_time", "running_status"]] = [datetime.datetime.now(), "finished"]
    run_status.to_csv("./run_status.csv", index=False)

    return {"message": "计算完成了"}
@app.post('/txt/', description='')
async def runfluent(params: Params):
    data = params.dict()
    with open('data.txt', 'w') as f:
        for key in data.keys():
            line_content = str(key) + ":" + " " + str(data[key]) + "\n"
    f.write(line_content)




if __name__ == '__main__':
    uvicorn.run(app='taskworker:app', port=9001, workers=1)

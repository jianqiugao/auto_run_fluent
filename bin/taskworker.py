import fastapi
import uvicorn
from fastapi import FastAPI
import numpy as np
import pandas as pd
import datetime
from main import main

app = FastAPI()
gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间
gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
                               columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])
# date = datetime.datetime(year=2024, month=2, day=12, hour=12, minute=10, second=20)
date = datetime.datetime.now()
mesh = "../run/20240201_215030/fluent_data/chao54-DUIBI.msh"
@app.get("/")
async def root():
    main(date, mesh=mesh, gas_liquid_time=gas_liquid_time)

    return {"message": "计算完成吗"}


if __name__ == '__main__':
    uvicorn.run(app='taskworker:app', port=9001)

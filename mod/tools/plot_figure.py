import os.path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def plot_gas_liquid_time(gas_liquid_time:pd.DataFrame,path:str):
    gas_liquid_time.loc['liquid_vol',:].plot(xlabel='time', ylabel='liquid_vol')
    plt.legend(loc='best')
    plt.savefig(os.path.join(path, 'volume_liquid_time.png'))
    plt.close()
    gas_liquid_time.loc['liquid_mass', :].plot(xlabel='time', ylabel='liquid_mass')
    plt.savefig(os.path.join(path, 'mass_liquid_time.png'))
    plt.close()
    gas_liquid_time.loc['gas_mass', :].plot(xlabel='time', ylabel='gass_mass')
    plt.savefig(os.path.join(path, 'mass_gas_time.png'))
    plt.close()
    gas_liquid_time.loc['gas_vol', :].plot(xlabel='time', ylabel='gass_vol')
    plt.savefig(os.path.join(path, 'volume_gas_time.png'))
    plt.close()




def plot_temp_pres(temp_press_dict, path: str):
    averge_press_on_xz_clip = temp_press_dict['averge_press_on_xz_clip']
    averge_temp_on_xz_clip = temp_press_dict['averge_temp_on_xz_clip']
    averge_press_on_yz_clip = temp_press_dict['averge_press_on_yz_clip']
    averge_temp_on_yz_clip = temp_press_dict['averge_temp_on_yz_clip']

    averge_press_on_xz_clip.transpose().plot(xlabel='time', ylabel='pressure(pa)')
    plt.legend(loc='best')
    plt.savefig(os.path.join(path, 'xz_ave_pre.png'))
    plt.close()

    averge_temp_on_xz_clip.transpose().plot(xlabel='time', ylabel='temperature(k)')
    plt.legend(loc='best')
    plt.savefig(os.path.join(path, 'xz_ave_tem.png'))
    plt.close()

    averge_press_on_yz_clip.transpose().plot(xlabel='time', ylabel='pressure(pa)')
    plt.legend(loc='best')
    plt.savefig(os.path.join(path, 'yz_ave_pre.png'))
    plt.close()

    averge_temp_on_yz_clip.transpose().plot(xlabel='time', ylabel='temperature(k)')
    plt.legend(loc='best')
    plt.savefig(os.path.join(path, 'yz_ave_tem.png'))
    plt.close()


if __name__ == '__main__':
    data = np.random.random((5, 20))
    gas_liquid_data = np.random.random((4, 20))  # 液体质量/体积-时间，气体质量/体积-时间

    # 液体体积/质量 -时间图
    gas_liquid_time = pd.DataFrame(data=gas_liquid_data, index=['liquid_vol', 'liquid_mass', 'gas_vol', 'gas_mass'],
                                   columns=[f't{i}' for i in range(gas_liquid_data.shape[1])])

    # xz 平面的温度/压力时间图
    averge_press_on_xz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                           columns=[f't{i}' for i in range(data.shape[1])])
    averge_temp_on_xz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                          columns=[f't{i}' for i in range(data.shape[1])])
    # yz 平面的温度/压力时间图
    averge_press_on_yz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                           columns=[f't{i}' for i in range(data.shape[1])])
    averge_temp_on_yz_clip = pd.DataFrame(data, index=[f'clip{i + 1}' for i in range(data.shape[0])],
                                          columns=[f't{i}' for i in range(data.shape[1])])
    temp_press_dict = {'averge_press_on_xz_clip': averge_press_on_xz_clip,
                       'averge_temp_on_xz_clip': averge_temp_on_xz_clip,
                       'averge_press_on_yz_clip': averge_press_on_yz_clip,
                       'averge_temp_on_yz_clip': averge_temp_on_yz_clip}
    plot_temp_pres(temp_press_dict, '')
    plot_gas_liquid_time(gas_liquid_time, '')

# data = np.random.random((5,20))
# gas_liquid_data = np.random.random((4,20)) # 液体质量/体积-时间，气体质量/体积-时间
# # xz 平面的温度/压力时间图
# averge_press_on_xz_clip = pd.DataFrame(data, index=[f'clip{i+1}' for i in range(data.shape[0])],columns=[f't{i}' for i in range(data.shape[1])])
# averge_temp_on_xz_clip = pd.DataFrame(data, index=[f'clip{i+1}' for i in range(data.shape[0])],columns=[f't{i}' for i in range(data.shape[1])])
# # yz 平面的温度/压力时间图
# averge_press_on_yz_clip = pd.DataFrame(data, index=[f'clip{i+1}' for i in range(data.shape[0])],columns=[f't{i}' for i in range(data.shape[1])])
# averge_temp_on_yz_clip = pd.DataFrame(data, index=[f'clip{i+1}' for i in range(data.shape[0])],columns=[f't{i}' for i in range(data.shape[1])])
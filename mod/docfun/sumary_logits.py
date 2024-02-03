import numpy as np

press_logits = \
    {
        'press_above_1': '计算结果显示，在给定条件下，内部流体升压速率较快；',
        'press_lower_1': '计算结果显示，在给定条件下，内部流体升压速率最大值为{}Pa，所处截面为{}；'
    }

temp_logits = \
    {
        'temp_above_5': '流体内部的温度分布不均匀，存在温度梯度。最高截面平均温度为{}K，所处截面为{}，最低截面平均温度为{}K，所处截面为{}；',
        'temp_lower_5': '流体内部的温度分布均匀，不存在温度梯度。内部整体平均温度为{}K；'
    }

avg_press_logits = \
    {
        'avg_press_above_2000': '流体内部的压力分布不均匀，存在压力梯度。最高截面平均压力为{}Pa，所处截面为{}，最低截面平均压力为{}Pa，所处截面为{}；',
        'avg_press_lower_2000': '流体内部的压力分布均匀，不存在压力梯度。内部整体平均压力为{}Pa；'
    }

resource_consum_logits = \
    {
        'resource_consum_above_96': '计算资源占用较高，计算时长总耗时{}小时。',
        'resource_consum_lower_96': '计算资源占用较少'
    }


def summary_logits(press_up: list, temp_diff: list,average_press:list,sus_time,run_time_cost):
    if (max(press_up) > 1):
        press_promts = press_logits['press_above_1']
    else:
        press_promts = press_logits['press_lower_1'].format(max(press_up), press_up.index(max(press_up)))

    if (max(temp_diff) - min(temp_diff)) > 5:
        temp_promts = temp_logits['temp_above_5'].format(max(temp_diff), temp_diff.index(max(temp_diff)),
                                                         min(temp_diff), temp_diff.index(min(temp_diff)))
    else:
        temp_promts = temp_logits['temp_lower_5'].format(np.mean(temp_diff))

    if (max(average_press) - min(average_press)) > 5:
        avg_press_promts = avg_press_logits['avg_press_above_2000'].format(max(average_press), temp_diff.index(max(average_press)),
                                                         min(average_press), temp_diff.index(min(average_press)))
    else:
        avg_press_promts = avg_press_logits['avg_press_lower_2000'].format(np.mean(temp_diff))

    phase_promts = "流体内部界面形状          ，界面稳定性             ，       波动；"
    sus_time_promts = f"容器维持时间达到{sus_time}天 ，设定维持时间为          天，          维持时间要求；"

    if run_time_cost > 96:
        run_time_cost_promts = resource_consum_logits['resource_consum_above_96'].format(run_time_cost)
    else:
        run_time_cost_promts = resource_consum_logits['resource_consum_lower_96']

    res_promots = press_promts+temp_promts+avg_press_promts+phase_promts+sus_time_promts+run_time_cost_promts
    return res_promots


if __name__ == '__main__':
    res = summary_logits([0.1, 0.3, 0.5, 0.6], [0.1, 0.3, 0.5, 0.6],[0.1, 0.3, 0.5, 0.6],20,99)
    print(res)


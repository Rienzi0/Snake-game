import numpy as np
import time
from dqn_model import DQN
from env_0 import env
wait_p = 1
bbeta = 0.5


def main(taskDim, vmDim, cluster, filepath_input, filepath_output):
    vmsNum = len(cluster.machines)
    
    print("环境创建成功！")

    state_all = []  # 存储所有的状态 [None,2+2*20]
    action_all = []  # 存储所有的动作 [None,1]
    reward_all = []  # 存储所有的奖励 [None,1]

    DRL = DQN(taskDim, vmsNum, vmDim)
    print("网络初始化成功！")

    for step, batch_tasks in enumerate(all_batch_tasks):
        #print(len(all_batch_tasks))
        tasks_list = []
        for task in batch_tasks:
            tasks_list.append(Task(task[0], task[1], task[2], task[3]))  # 构建任务

        states = get_state(tasks_list, cluster.machines)
        state_all += states
        machines_id = DRL.choose_action(np.array(states))  # 通过调度算法得到分配 id
        machines_id = machines_id.astype(int).tolist()
        cluster.submit_tasks(tasks_list, machines_id)  # 提交任务到集群，并调度到虚拟机进行计算


        
        
        
        for i, task in enumerate(cluster.finished_tasks[-len(tasks_list):]):  # 便历新提交的一批任务，记录动作和奖励
            action_all.append([task.task_machine_id])
            reward_p = 0
            if task.wait_time == 0:
                reward_p += wait_p
            reward = bbeta * (task.task_response_time / task.mi - r_min)/(r_max - r_min) + (1 - bbeta) * (task.task_run_time * cluster.machines[task.task_machine_id].micost / c_max)
            reward_all.append([(reward +reward_p + 0.0001)])  # 计算奖励
        
        # 减少存储数据量
        if len(state_all) > 3000:
            state_all = state_all[-1500:]
            action_all = action_all[-1500:]
            reward_all = reward_all[-1500:]

        # 先学习一些经验，再学习
        if step > 400: ######step >400
            # 截取最后10000条记录
            new_state = np.array(state_all, dtype=np.float32)[-1000:-1]
            new_action = np.array(action_all, dtype=np.float32)[-1000:-1]
            new_reward = np.array(reward_all, dtype=np.float32)[-1000:-1]
            DRL.store_memory(new_state, new_action, new_reward)
            DRL.step = step
            loss = DRL.learn()
            if (step % 1000 == 0):
                print("step:", step, ", loss:", loss)

    finished_tasks = []
    for task in cluster.finished_tasks:
        finished_tasks.append(task.feature)
    FileIo(filepath_output).twoListToFile(finished_tasks, "w")

if __name__ == '__main__':
    start_time = time.time()
    taskDim = 3

    #filepath_input = "data/real/real_tasks(5-50)(100).txt"
    filepath_input = "data/real/google.txt"
    filepath_output = "/Users/rienzi/Desktop/实验代码/Pycloudsim/result/dqn(google).txt"
    #filepath_output = "/Users/rienzi/Desktop/实验代码/Pycloudsim/result/dqn(5-50)(100).txt"
    main(taskDim, vmDim, cluster, filepath_input, filepath_output)
   
   

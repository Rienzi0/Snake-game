import numpy as np
import time
from dqn_model import DQN
from env_0 import env
Steps = 100000
from reward_fn import score_reward,game_reward,food_distance
import os
import torch
def main(taskDim, action_dim,env):
    

    state_all = []  # 存储所有的状态 [None,2+2*20]
    action_all = []  # 存储所有的动作 [None,1]
    reward_all = []  # 存储所有的奖励 [None,1]
    try:
        DRL = DQN(taskDim, action_dim)
        DRL.train()
        DRL.load_state_dict(torch.load("checkpoints/model.pth"))
        print("successfullt loaded")
    except:
        DRL = DQN(taskDim, action_dim)
        print("successfully initialized")
    

    for step in range(Steps):

        states = env.get_state()
        state_all.append(states)
        
        action = DRL.choose_action(np.array(np.expand_dims(states,axis = 0)))  # 通过调度算法得到分配 id
        #print(action)
        action_all.append(action)
        env.Step(action)
        reward = score_reward(env) + game_reward(env) + food_distance(env)
        
        reward_all.append([reward])
        
        # 减少存储数据量
        if len(state_all) > 30:
            state_all = state_all[-15:]
            action_all = action_all[-15:]
            reward_all = reward_all[-15:]

        # 先学习一些经验，再学习
        if step > 40: ######step >400
            # 截取最后10000条记录
            new_state = np.array(state_all, dtype=np.float32)[-20:-1]
            new_action = np.array(action_all, dtype=np.float32)[-20:-1]
            new_reward = np.array(reward_all, dtype=np.float32)[-20:-1]
            DRL.store_memory(new_state, new_action, new_reward)
            DRL.step = step
            loss = DRL.learn()
            if (step % 10 == 0):
                print("step:", step, ", loss:", loss)
            if step % 100 == 0:
                torch.save(DRL.state_dict(),"checkpoints/model.pth")
        if env.game_over == True:
            env.Ready()
            env.Start()
            
                
                

        
        
        

    

if __name__ == '__main__':
    start_time = time.time()
    taskDim = 12
    action_dim = 3
    E = env()
    E.Ready()
    E.Start()
    
    main(taskDim,action_dim, E)
   
   

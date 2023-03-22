def score_reward(env):
    score_now = env.score_list[-1]
    score_past = env.score_list[-2] if len(env.score_list) >= 2 else 0
    if score_now > score_past:
        reward = 100
    else:
        reward = -5
    return reward

def game_reward(env):
    if env.game_over == False:
        return 1
    else:
        return -100

def food_distance(env):
    dis_now = env.dis_list[-1]
    dis_past = env.score_list[-2] if len(env.score_list) >= 2 else dis_now
    if dis_now < dis_past:
        reward = 10
    else:
        reward = -10
    return reward
 


def score_reward(env):
    score_now = env.score_list[-1]
    score_past = env.score_list[-2]
    if score_now > score_past:
        reward = 100
    else:
        reward = 0
    return reward

def game_reward(env):
    if env.game_over == False:
        return 1
    else:
        return -100


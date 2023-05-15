# from push_swap_env import PushSwapEnv
import gym

gym.envs.register(
    id='push-swap-v0',
    entry_point='push_swap_env:PushSwapEnv',
)
env = gym.make('push-swap-v0')  # 초기 상태는 [3, 1, 2]로 설정
obs = env.reset()
env.render()

env.run_value_iteration(episodes=2)

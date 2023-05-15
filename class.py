import gym
import numpy as np


class PushSwapEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(PushSwapEnv, self).__init__()
        nums = [83, 17, 49, 68, 92, 29, 72, 42, 56, 5]
        self.nums = nums  # 초기 상태
        self.goal = sorted(nums)  # 목표 상태
        self.stack_a = []  # 스택 A
        self.stack_b = []  # 스택 B
        for num in nums:
            self.stack_a.append(num)
        self.action_space = gym.spaces.Discrete(6)  # 0~5 중 하나의 액션 공간
        self.observation_space = gym.spaces.Box(low=-10, high=10, shape=(len(nums)*2,), dtype=np.int32)  # 관측 공간은 두 배열을 합친 형태

    def reset(self):
        self.stack_a = self.nums.copy()  # 초기 상태로 리셋
        self.stack_b = []
        return self._get_observation()

    def step(self, action):

        if action == "sa":
            self._swap(self.stack_a)
        elif action == "sb":
            self._swap(self.stack_b)
        elif action == "ss":
			self.ss(self.stack_a, self.stack_b)
        elif action == "pa":
            self._push(self.stack_a, self.stack_b)
        elif action == "pb":
            self._rotate(self.stack_b, self.stack_a)
		elif action == "ra":
            self._rotate(self.stack_a)
        elif action == "rb":
            self._rotate(self.stack_b)
		elif action == "rr":
            self._rr(self.stack_a, self.stack_b)
		elif action == "rra":
            self._reverse_rotate(self.stack_a)
		elif action == "rrb":
        	self._reverse_rotate(self.stack_b)
		elif action == "rrr":
            self._rrr(self.stack_a, self.stack_b)
        else:
            raise ValueError('action must be 0 or 1')

        # 목표 상태인지 확인
        done = len(self.stack_a) == 0 and self.stack_b == self.goal
        reward = 1 if done else 0  # 목표 상태에 도달하면 보상 1, 아니면 0
        return self._get_observation(), reward, done, {}

    def render(self, mode='human'):
        if mode == 'human':
            print('Stack A:', self.stack_a)
            print('Stack B:', self.stack_b)

    def _swap(self, stack):
        if len(stack) >= 2:
            stack[-1], stack[-2] = stack[-2], stack[-1]

    def ss(self, stack_a, stack_b):
        self._swap(stack_a)
        self._swap(stack_b)

    def _push(self, dst, src):
        if len(src) > 0:
            dst.append(src.pop())
    def _rotate(self, stack):
		if len(stack) > 0:
			stack.insert(0, stack.pop())

	def _rr(self, stack_a, stack_b):
		self._rotate(stack_a)
		self._rotate(stack_b)

	def _reverse_rotate(self, stack):
		if len(stack) > 0:
			stack.insert(len(stack), stack.pop(0))

	def _rrr(self, stack_a, stack_b):
		self._reverse_rotate(stack_a)
		self._reverse_rotate(stack_b)

    def _get_observation(self):
        return np.concatenate((self.stack_a, self.stack_b), axis=0)


print("hello world")

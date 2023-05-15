# from push_swap_env import PushSwapEnv
import gym
import numpy as np
import matplotlib.pyplot as plt
import time


class PushSwapEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		super(PushSwapEnv, self).__init__()
		nums = [4, 1, 2, 3, 5]  # 초기 상태
		self.episodes = 0
		self.nums = nums
		self.goal = sorted(nums)  # 목표 상태
		self.stack_a = []  # 스택 A
		self.stack_b = []  # 스택 B
		for num in nums:
			self.stack_a.append(num)
		self.action_space = gym.spaces.Discrete(11)  # 0~5 중 하나의 액션 공간
		self.observation_space = gym.spaces.Box(
			low=-5, high=5, shape=(len(nums)*2,), dtype=np.int32)  # 관측 공간은 두 배열을 합친 형태
		self.values = np.zeros(self.action_space.n)

	def reset(self):
		self.stack_a = self.nums.copy()
		self.stack_b = []
		return self._get_observation()

	def render(self, mode='human'):
		if mode == 'human':
			print('Stack A:', self.stack_a)
			print('Stack B:', self.stack_b)

	def _swap(self, stack):
		if len(stack) >= 2:
			stack[-1], stack[-2] = stack[-2], stack[-1]

	def _ss(self, stack_a, stack_b):
		self._swap(stack_a)
		self._swap(stack_b)

	def _push(self, dst, src):
		if len(src) >= 1:
			dst.append(src.pop())

	def _rotate(self, stack):
		if len(stack) >= 1:
			stack.insert(0, stack.pop())

	def _rr(self, stack_a, stack_b):
		self._rotate(stack_a)
		self._rotate(stack_b)

	def _reverse_rotate(self, stack):
		if len(stack) >= 1:
			stack.append(stack.pop(0))

	def _rrr(self, stack_a, stack_b):
		self._reverse_rotate(stack_a)
		self._reverse_rotate(stack_b)

	def step(self, action):
		if action == 0:  # "sa":
			self._swap(self.stack_a)
		elif action == 1:  # "sb":
			self._swap(self.stack_b)
		elif action == 2:  # "ss":
			self._ss(self.stack_a, self.stack_b)
		elif action == 3:  # "pa":
			self._push(self.stack_a, self.stack_b)
		elif action == 4:  # "pb":
			self._push(self.stack_b, self.stack_a)
		elif action == 5:  # "ra":
			self._rotate(self.stack_a)
		elif action == 6:  # "rb":
			self._rotate(self.stack_b)
		elif action == 7:  # "rr":
			self._rr(self.stack_a, self.stack_b)
		elif action == 8:  # "rra":
			self._reverse_rotate(self.stack_a)
		elif action == 9:  # "rrb":
			self._reverse_rotate(self.stack_b)
		elif action == 10:  # "rrr":
			self._rrr(self.stack_a, self.stack_b)
		else:
			raise ValueError('action must be 0 or 1')

		# 목표 상태인지 확인
		done = len(self.stack_b) == 0 and self.stack_a == self.goal
		reward = 1 if done else 0  # 목표 상태에 도달하면 보상 1, 아니면 0
		return self._get_observation(), reward, done, {}

	def _get_observation(self):
		return np.concatenate([self.stack_a, self.stack_b], axis=0)

	def update_value(self, action, next_state):
		value = self.values[action]
		next_value = np.max(self.values)  # 다음 상태에서의 가장 큰 가치 선택
		self.values[action] = value + self.learning_rate * (next_value - value)

	def run_value_iteration(self, episodes, learning_rate=0.1):
		self.learning_rate = learning_rate
		scores = []
		counts_action = []

		for episode in range(episodes):
			self.reset()
			done = False
			score = 0
			count_action = 0

			while not done:
				# 현재 상태에서 가치가 가장 큰 행동 선택
				action = np.argmax(self.values)
				count = np.count_nonzero(self.values == self.values[action])

				if count > 1:
					# 중복 값 중 랜덤하게 선택
					action_idx = np.where(
						self.values == self.values[action])[0]
					action = np.random.choice(action_idx)

				# 액션 수행
				obs, reward, done, _ = self.step(action)
				# self.render()
				score += reward
				count_action += 1

				# 가치 업데이트
				self.update_value(action, obs)
				print(self.values)

			print(f"Episode {episode+1} / {episodes} | Score: {score}")

			scores.append(score)
			counts_action.append(count_action)
			
		print("self.values: ", self.values)
		print(f"Final score: {score}")
		#점수 그래프 출력
		plt.plot(range(1, episodes+1), counts_action)
		plt.xlabel('Episode')
		plt.ylabel('Score')
		plt.show()

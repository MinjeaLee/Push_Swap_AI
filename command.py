# class command:
def _swap(stack):
	if len(stack) >= 2:
		stack[-1], stack[-2] = stack[-2], stack[-1]

def _ss(self, stack_a, stack_b):
	self._swap(stack_a)
	self._swap(stack_b)

def _push(dst, src):
	if len(src) >= 1:
		dst.append(src.pop())

def _rotate(stack):
	if len(stack) >= 1:
		stack.insert(0, stack.pop())

def _rr(self, stack_a, stack_b):
	self._rotate(stack_a)
	self._rotate(stack_b)

def _reverse_rotate(stack):
	if len(stack) >= 1:
		stack.append(stack.pop(0))
		
def _rrr(self, stack_a, stack_b):
	self._reverse_rotate(stack_a)
	self._reverse_rotate(stack_b)

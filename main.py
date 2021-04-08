#!/usr/bin/env python
from datetime import timedelta
import math, time, threading

# This is an attempt at a unique kind of rate limiter
# that uses the load algorithm to determine limits.

class RateLimit:

	# the current score (aka, rate limit)
	score = 0.0
	# timescale (aka, how quickly it releases the limit)
	timescale = 1.0
	# the rate which the timescale is updated by the thread
	rate = 1.0
	# Calculated magic
	_magic = 0.0
	# How many tokens the user has accrued
	tokens = 0
	# How many messages we can burst with
	burst = 0


	def __init__(self, timescale: timedelta, rate: int, burst: int) -> None:
		self.idleloop = threading.Thread(target=self.___idle_loop)
		self.timescale = timescale.total_seconds()
		self.rate = rate
		self.tokens = -burst
		self.burst = burst
		self._magic = math.exp(-self.rate / self.timescale)
		self.idleloop.start()

	def check_score(self) -> float:
		tmp = self.score * self._magic
		tmp += self.tokens * (1 - self._magic)
		return tmp

	def ___idle_loop(self) -> None:
		while True:
			self.score *= self._magic
			self.score += self.tokens * (1 - self._magic)
			# Clamp negative numbers
			if self.score < 0.00:
				self.score = 0.00
				if self.tokens >= -self.burst:
					self.tokens += - 1
			else:
				self.tokens = 0

			print(f"limit: {self.score}, tokens: {self.tokens}")
			time.sleep(self.rate)

	def CheckLimit(self) -> float:
		self.tokens += 1
		score = self.check_score()
		if score < 0.00:
			return 0.00
		return score


def main():

	limit = RateLimit(timedelta(seconds=10), 1, 10);
	for i in range(20):
		sl = limit.CheckLimit()
		print(f"Sleep for {sl}s")
		time.sleep(sl)

if __name__ == "__main__":
	main()
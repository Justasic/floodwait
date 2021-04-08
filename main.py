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

	def __init__(self, timescale: timedelta, rate: int) -> None:
		self.idleloop = threading.Thread(target=self.___idle_loop)
		self.timescale = timescale.total_seconds()
		self.rate = rate
		self._magic = math.exp(-self.rate / self.timescale)
		self.idleloop.start()

	def _calc_score(self) -> None:
		self.score *= self._magic
		self.score += self.tokens * (1 - self._magic)

	def ___idle_loop(self) -> None:
		while True:
			self._calc_score()
			self.tokens = 0
			print(f"limit: {self.score}")
			time.sleep(self.rate)

	def CheckLimit(self) -> int:
		self.tokens += 1
		# self._calc_score()


def main():

	limit = RateLimit(timedelta(minutes=1), 1);
	for i in range(10000):
		limit.CheckLimit()

if __name__ == "__main__":
	main()
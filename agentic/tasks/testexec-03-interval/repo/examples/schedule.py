"""Example: model busy time on a calendar with an IntervalSet.

Run: python examples/schedule.py
(Requires the IntervalSet implementation to be complete.)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intervalset import IntervalSet


def demo():
    busy = IntervalSet()
    busy.add(9, 10)     # 9-10 meeting
    busy.add(10, 11)    # 10-11 meeting (adjacent -> merges to 9-11)
    busy.add(13, 14)    # lunch-ish block
    print("busy blocks:", busy.intervals())
    print("busy hours:", busy.measure())
    busy.remove(9, 9)   # empty, no-op
    busy.remove(13, 14)
    print("after freeing 13-14:", busy.intervals())
    return busy


if __name__ == "__main__":
    demo()

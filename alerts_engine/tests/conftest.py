import pytest

from engine_tools import scheduler_async


class counting_test_class:
    def __init__(self,limit = None):
        self.limit = limit
        self.count = 0

    def task(self):
        if self.limit != None:
            if self.count >= self.limit:
                raise scheduler_async.EndRun()
        self.count = self.count + 1
        print("ENDING",self.count)

@pytest.fixture(scope='function',autouse=True)
def counter_class():
    counter_class = counting_test_class()
    return counter_class

@pytest.fixture(scope='function',autouse=True)
def limited_counter_class():
    counter_class = counting_test_class(50)
    return counter_class



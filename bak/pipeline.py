# -*- coding: utf-8 -*-

import abc


class TestClass1(object):
    def __init__(self):
        self.pip_workers = None
        self.pdata = {}

    @abc.abstractmethod
    def create_pip_workers(self):
        raise NotImplementedError()

    def run(self):
        self.create_pip_workers()
        for worker in self.pip_workers:
            worker(self.pdata)


def test_1(pdata):
    print("test 1")


class TestClass2(TestClass1):

    def test_2(self, pdata):
        print(self.pdata, "test worker 2")

    def create_pip_workers(self):
        self.pip_workers = [
            test_1,
            self.test_2
        ]


if __name__ == '__main__':
    test = TestClass2()
    test.run()

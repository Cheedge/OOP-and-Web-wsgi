# ref: https://www.liaoxuefeng.com/wiki/1016959663602400/1017590712115904
from typing import Union
class Fib(object):
    def __init__(self) -> None:
        self.a, self.b = 0, 1

    # realize index elements and slice
    def __getitem__(self, n: Union[int, slice]) -> int:
        if isinstance(n, int):
            for _ in range(n):
                self.a, self.b = self.b, self.a + self.b
            return self.a
        elif isinstance(n, slice):
            res = list()
            start, stop = n.start, n.stop
            for _ in range(stop):
                self.a, self.b = self.b, self.a + self.b
                if _ > start:
                    res.append(self.a)
            return res

    # realize for loop iterate
    def __iter__(self):
        return self
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 10: # 退出循环的条件
            raise StopIteration()
        return self.a

f = Fib()
for i in f:
    print(f'{i=}')
a = int(input())
print(f'{a=}, {f[a]=}')
start, stop = input().split(',')
print(f'{start=}, {stop=}, {f[int(start):int(stop)]=}')

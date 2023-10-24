

import random
from typing import Type

import matplotlib

from matplotlib import pyplot as plt
from itertools import count


matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False


c = count()


# warning AI提示词: 模仿BubbleSort以ArrayDisplay为基类实现一个基数排序


class ArrayDisplay:
    default_color = "black"
    swapped_color = "blue"
    title = "{cls}"
    step_delay = 0.001

    def __init__(self, arr):
        self.array = arr
        self.length = len(arr)
        self.canvas = plt.figure().canvas
        self.colors = [self.default_color] * self.length
        self.rend()

    def rend(self, *, clf=True):
        plt.ion()
        plt.title(self.title.format(cls=self.get_cls_name()), loc="center")
        plt.ylabel("值")
        plt.xlabel("索引")
        plt.bar(range(self.length), self.array, color=self.colors, width=1)
        plt.pause(self.step_delay)
        if clf:
            plt.clf()

    def swap(self, i, j):
        print(f"({next(c)+1})Swap # {i}: {self.array[i]} <-> {j}: {self.array[j]}")
        self.colors[i] = "red"
        self.colors[j] = "yellow"
        self.rend()
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.colors[i] = self.swapped_color
        self.colors[j] = self.swapped_color

    def get_cls_name(self):
        return f"{type(self).__name__}"

    def sort(self):
        raise NotImplementedError


class BubbleSort(ArrayDisplay):
    def __init__(self, arr):
        super().__init__(arr)
        self.array = arr
        self.length = len(arr)

    def sort(self):
        for i in range(self.length):
            for j in range(0, self.length - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.swap(j, j + 1)
        return self.array


class HeapSort(ArrayDisplay):
    build_heap_color = "pink"

    def __init__(self, arr):
        super().__init__(arr)
        self.array = arr
        self.length = len(arr)

    def heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            self.swap(i, largest)
            self.heapify(arr, n, largest)

    def sort(self):
        old_title = self.title
        old_color = self.swapped_color
        self.swapped_color = self.build_heap_color
        self.title += ": Building Heap"
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(self.array, self.length, i)

        self.swapped_color = old_color
        self.title = old_title

        for i in range(self.length - 1, 0, -1):
            self.swap(i, 0)

            self.heapify(self.array, i, 0)

        return self.array


class InsertionSort(ArrayDisplay):
    def __init__(self, arr):
        super().__init__(arr)
        self.array = arr
        self.length = len(arr)

    def sort(self):
        for i in range(1, self.length):
            key = self.array[i]
            j = i - 1
            while j >= 0 and self.array[j] > key:
                self.swap(j, j+1)
                j -= 1
            self.array[j+1] = key
        return self.array


class QuickSort(ArrayDisplay):
    def __init__(self, arr):
        super().__init__(arr)
        self.array = arr
        self.length = len(arr)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.swap(i, j)
        self.swap(i+1, high)
        return i + 1

    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi-1)
            self.quick_sort(pi+1, high)

    def sort(self):
        self.quick_sort(0, self.length-1)
        return self.array


class SelectionSort(ArrayDisplay):
    def __init__(self, arr):
        super().__init__(arr)
        self.array = arr
        self.length = len(arr)

    def sort(self):
        for i in range(self.length):
            min_idx = i
            for j in range(i+1, self.length):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.swap(i, min_idx)
        return self.array


class ShellSort(ArrayDisplay):
    def __init__(self, arr):
        super().__init__(arr)
        self.array = arr
        self.length = len(arr)

    def sort(self):
        gap = self.length // 2
        while gap > 0:
            for i in range(gap, self.length):
                temp = self.array[i]
                j = i
                while j >= gap and self.array[j-gap] > temp:
                    self.swap(j, j-gap)
                    j -= gap
                self.array[j] = temp
            gap //= 2
        return self.array


def generate_random_numbers(n):
    # numbers = list(range(1, n + 1))
    # random.shuffle(numbers)
    numbers = []
    for _ in range(n):
        numbers.append(random.randint(1, 1000)/100)
    return numbers


sorters = {
    "冒泡排序": BubbleSort,
    "快速排序": QuickSort,
    "堆排序": HeapSort,
    "插入排序": InsertionSort,
    "选择排序": SelectionSort,
    "希尔排序": ShellSort
}


while True:
    print("排序算法: ", ','.join(sorters.keys()))
    sorter_name = input("键入排序算法(全名): ")

    try:
        sorter_type = sorters[sorter_name]
    except KeyError:
        print("未找到该算法, 请重新键入")
        print()
    else:
        break


while True:
    try:
        random_range = int(input("键入数据规模(数据量): "))
    except ValueError:
        print("数据规模输入有误, 请重新键入")
        print()
    else:
        break


while True:
    try:
        step_delay = float(input("键入单步延迟(单位秒): "))
    except ValueError:
        print("单步延迟输入有误, 请重新键入")
        print()
    else:
        break

# 随机生成数值
random_arr = generate_random_numbers(random_range)


# 创建Sort实例
sorter_type: Type[ArrayDisplay]
sorter = sorter_type(random_arr)
sorter: ArrayDisplay

sorter.step_delay = step_delay
# _ _, 启动!
sorter.sort()

total_time = 1.5
faster = 0

sorter.rend(clf=False)
plt.pause(0.5)


for x in range(random_range):
    plt.bar(x, sorter.array[x], color="red", width=1)
    if x-1 >= 0:
        plt.bar(x-1, sorter.array[x-1], color="yellow", width=1)
    if x-2 >= 0:
        plt.bar(x-2, sorter.array[x-2], color="green", width=1)
    faster -= 0.001
    delay = total_time/random_range + faster
    if delay > 0.05:
        delay = 0.05
    elif delay <= 0:
        delay = 0.01
    plt.pause(delay)


plt.clf()

sorter.colors = ["green"] * sorter.length

sorter.rend(clf=False)
plt.pause(10)

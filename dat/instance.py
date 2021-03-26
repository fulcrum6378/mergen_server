import os
import copy

import dat.search as search


class Instance:  # ABSTRACT BY DEFAULT
    def __init__(self, obj):
        self.obj = obj
        self.number = -1
        self.reference = None
        self.attrs = None

    def lowest_free_id(self):
        if self.obj is None or self.obj.reference is None:
            return False
        already = search.folders(self.obj.reference)
        numerical = {}
        for a in already:
            if a.isnumeric():
                numerical[int(a)] = a
        self.number = 0
        toList = list(numerical)
        if len(toList) > 0:
            toList.sort()
            while self.number in toList:
                self.number += 1
        self.reference = self.obj.reference + "/" + str(self.number)
        return True

    def multiply(self, number):
        collect = []
        for _ in range(0, number): collect.append(copy.deepcopy(self))
        return collect


class NewInstance(Instance):
    def __init__(self, obj):
        Instance.__init__(self, obj)
        if not self.lowest_free_id():
            return
        if not os.path.isdir(self.reference):
            os.makedirs(self.reference)


class ReadyInstance(Instance):
    def __init__(self, obj, reference):
        Instance.__init__(self, obj)
        if type(reference) == int:
            self.number = reference
            self.reference = self.obj.reference + "/" + str(self.number)
        else:
            self.reference = reference
            self.number = int(self.reference.split("/")[-1])
        if not os.path.isdir(self.reference):
            os.makedirs(self.reference)


class RememberInstance(Instance):
    def __init__(self, obj):
        Instance.__init__(self, obj)
        # NEEDS TO BE WORKED ON...
        # self.acknowledge()

import os
import shutil

import dat.config as cfg


class Thing:
    def __init__(self):
        self.name = None
        self.reference = None
        self.attrs = None

    def exists(self):
        return self.reference is not None

    def parent(self, index):
        try:
            ret = ReadyThing(self.reference.split("/")[-(index + 1)])
        except:
            ret = None
        return ret

    def tiny_ref(self):
        try:
            return "/".join(self.reference[len(cfg.root):].split("/")[1:])
        except:
            return None


class NewThing(Thing):
    def __init__(self, name):
        Thing.__init__(self)
        self.name = name
        self.reference = cfg.root + 'mem/' + pathAdr(self.name)
        if not os.path.isdir(self.reference):
            os.makedirs(self.reference)


class ReadyThing(Thing):
    def __init__(self, path):
        Thing.__init__(self)
        self.reference = cfg.root + 'mem/' + path
        self.name = self.reference.split("/")[-1]
        if not os.path.isdir(self.reference):
            os.makedirs(self.reference)


class MoveThing(Thing):
    def __init__(self, first, second):
        Thing.__init__(self)
        self.first = first
        self.second = second
        self.movedFirst = None
        self.movedSecond = None

    def isRational(self):
        if self.first.reference == self.second.reference:
            return False
        if self.first.reference == self.second.reference + "/" + self.first.name:
            return False
        return True

    def execute(self, is_first_real, is_second_real):
        if is_first_real or is_second_real:
            if self.movedFirst is not None:
                return False
            if is_first_real and not self.first.exists():
                self.first.reference = NewThing(self.first.name).reference
            if is_second_real and not self.second.exists():
                self.second.reference = NewThing(self.second.name).reference
            if is_first_real and is_second_real and not self.isRational():
                return False
        return True


class MakeSubClassOf(MoveThing):
    def __init__(self, name, parent):
        MoveThing.__init__(self, name, parent)

    def execute(self, is_first_real=True, is_second_real=True):
        if not MoveThing.execute(self, is_first_real, is_second_real):
            return
        if self.second.reference.startswith(self.first.reference) and "/" not in self.first.reference[
                                                                                 len(self.second.reference):]:
            self.movedSecond = "/".join(self.second.reference.split("/")[0: -2]) + "/" + self.second.name
            shutil.move(self.second.reference, self.movedSecond)
            self.movedFirst = self.movedSecond + "/" + self.name
        else:
            self.movedFirst = self.second.reference + "/" + self.name
        shutil.move(self.first.reference, self.movedFirst)


class DeleteObject(ReadyThing):
    def __init__(self, reference):
        ReadyThing.__init__(self, reference)

    def execute(self):
        if self.reference is not None:
            shutil.rmtree(self.reference)


def pathAdr(raw): return raw.lower().replace(" ", "_")

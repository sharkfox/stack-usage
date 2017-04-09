
import sys

class CallGraph(object):
    def __init__(self):
        self.funcs = {}

    def getFunction(self, name):
        if name not in self.funcs:
            self.funcs[name] = Function(name)
        return self.funcs[name]

    def getStackString(self, funcList):
        return " ".join([f.name + "/" + str(f.stack) for f in funcList])

    def getStackSize(self, funcList):
        return sum([f.stack for f in funcList])

    def addCall(self, caller, callee):
        self.getFunction(caller).addCallee(self.getFunction(callee))
        self.getFunction(callee).addCaller(self.getFunction(caller))

    def linearizeNode(self, name, funcList, callStack = []):
        node = { "name": name, "children": [], "size": self.getStackSize(callStack), "callStack": self.getStackString(callStack) }
        for f in funcList:
            node["children"].append(self.linearizeNode(funcList[f].name, funcList[f].callee, callStack + [funcList[f]]))
        node["maxSize"] = max([c["maxSize"] for c in node["children"]] + [node["size"]])
        return node

    def linearize(self):
        return self.linearizeNode("", {k: v for k, v in self.funcs.items() if len(v.caller) == 0})

class Function(object):
    def __init__(self, name):
        self.name   = name
        self.stack  = 0
        self.caller = {}
        self.callee = {}

    def setStackSize(self, size):
        self.stack = max(self.stack, size)

    def addCaller(self, caller):
        self.caller[caller.name] = caller

    def addCallee(self, callee):
        self.callee[callee.name] = callee

if __name__ == "__main__":
    cgraph = CallGraph()

    with open('stack-usage-log.su', 'r') as f:
        for line in f:
            cols = line.split('\t')
            text = cols[0].split(':')

            cgraph.getFunction(text[3]).setStackSize(int(cols[1]))

    with open('stack-usage-log.cgraph', 'r') as f:
        for line in f:
            if line.find('@') != -1 and not line.startswith('  Aux: @'):
                name = line[0:line.find('/')]
            if line.startswith('  Calls:') and len(line) > 10:
                for callee in line[9:].split(' '):
                    if callee.find('/') != -1:
                        cgraph.addCall(name, callee[:callee.find('/')])

    print(cgraph.linearize())

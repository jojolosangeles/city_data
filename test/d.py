class Dynamo(object):
    pass

def add_dynamo(cls,i):
    def innerdynamo(self, param):
        print("in dynamo {i}, param {param}".format(i=i, param=param))
    innerdynamo.__doc__ = "docstring for dynamo%d" % i
    innerdynamo.__name__ = "dynamo%d" % i
    setattr(cls,innerdynamo.__name__,innerdynamo)

for i in range(2):
    add_dynamo(Dynamo, i)

d=Dynamo()
d.dynamo0(7)
d.dynamo1(22)

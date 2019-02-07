
class Dynamo(object):
  pass

def add_dynamo(cls, methodName, dataFrameName):
    def innerdynamo(self, paramName, dataFrameName, code):
        code = code.replace('DATA_FRAME',dataFrameName)
        x = eval(code)
        return x
        #print("innnerdynamo {methodName}, {paramName}={code}".format(methodName=methodName, paramName=paramName, code=code))
    innerdynamo.__doc__ = "docstring for {methodName}".format(methodName=methodName)
    innerdynamo.__name__ = methodName
    setattr(cls,innerdynamo.__name__,innerdynamo)

add_dynamo(Dynamo, "create", "df")

d=Dynamo()
result = d.create("longitude", "df", """print('DATA_FRAME.doLotsOfShit()')""")
  #return 33
#""")
print("result={}".format(result))
result = d.create("longitude", "df", """77""")
print("result={}".format(result))
#d.kk()

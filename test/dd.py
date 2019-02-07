class Dynamo(object):
  pass

def add_dynamo(cls,methodName):
    def innerdynamo(self, paramName, code):
        code = code.replace('DATA_FRAME','df')
        x = eval(code)
        #print("innnerdynamo {methodName}, {paramName}={code}".format(methodName=methodName, paramName=paramName, code=code))
    innerdynamo.__doc__ = "docstring for {methodName}".format(methodName=methodName)
    innerdynamo.__name__ = methodName
    setattr(cls,innerdynamo.__name__,innerdynamo)

add_dynamo(Dynamo, "JJ")
add_dynamo(Dynamo, "kk")

d=Dynamo()
d.JJ("longitude", "print('ha DATA_FRAME.doLotsOfShit()')")
#d.kk()

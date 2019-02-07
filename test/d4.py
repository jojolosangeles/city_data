
class MyClass:
  def __init__(self):
    print("MyClass constructor")

  def test1(self):
    print("MyClass.test1()")

  def test2(self):
    print("MyClass.test2()")

def testfn():
  myClass = MyClass()
  myClass.test1()
  eval("myClass.test2()")

print("Start of test, calling testfn()")
testfn()
print("End of test")

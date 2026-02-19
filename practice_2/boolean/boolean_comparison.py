#1 some values are True
bool("zxc")
bool(256)
bool(["pineapple", "pen", "apple"])


#2 some values are False
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})


#3 the function evaluates to False, if it's returns 0 or False
class oioioi():
  def __len__(self):
    return 0

obj = oioioi()
print(bool(obj))


#4 function can return a boolean and continue the code based on the answer
def funkciya() :
  return True

if funkciya():
  print("DA!")
else:
  print("NET!")


#5 checking if the variables is integer
x = 1.1111111111
print(isinstance(x, int))
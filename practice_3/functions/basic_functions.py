#1 creating a function
def funk():
    print("안녕하세요")


#2 calling a function
funk()
funk()
funk()
funk()


#3 functions can send data back to the code that called them using the return statement
def byebye():
    return "안녕히 가세요"

output = byebye()
print(output)


#4 "pass" will skip the funtion code
def nothing_happened():
    pass
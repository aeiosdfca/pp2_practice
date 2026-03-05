import re


#1
strings = ["a", "ab", "abb", "ac", "b"]
pattern = r"ab*"
for s in strings:
    if re.fullmatch(pattern, s):
        print(s, "-> Match")


#2 
strings = ["ab", "abb", "abbb", "abbbb"]
pattern = r"ab{2,3}"
for s in strings:
    if re.fullmatch(pattern, s):
        print(s, "-> Match")


#3 
text = "snake_case example test_string HelloWorld"
pattern = r"[a-z]+_[a-z]+"
result = re.findall(pattern, text)
print(result)


#4 
text = "Hello world From South Korea"
pattern = r"[A-Z][a-z]+"
print(re.findall(pattern, text))


#5
strings = ["ab", "acb", "a123b", "abbb", "ac"]
pattern = r"a.*b"
for s in strings:
    if re.fullmatch(pattern, s):
        print(s, "-> Match")


#6
text = "Python, Java. C++ programming language"
result = re.sub(r"[ ,\.]", ":", text)
print(result)


#7
snake = "python_regex_exercises"
camel = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), snake)
print(camel)


#8
text = "PythonRegexIsPowerful"
result = re.split(r"(?=[A-Z])", text)
print(result)


#9
text = "PythonRegexIsPowerful"
result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)
print(result)


#10
camel = "pythonRegexExercises"
snake = re.sub(r"([A-Z])", r"_\1", camel).lower()
print(snake)
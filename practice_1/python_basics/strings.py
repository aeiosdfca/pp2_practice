#1 quotes are important and must not be repeating in the same string
print("hi:3")
print('hi:3')
print("everything'll be okay!")
print("his name is 'Michael'")
print('and his surname is "Jackson"')


#2 multiline strings are also possible
w = '''    У лукоморья дуб зелёный;
    Златая цепь на дубе том:
    И днём и ночью кот учёный
    Всё ходит по цепи кругом;'''

v = """    Идёт направо — песнь заводит,
    Налево — сказку говорит.
    Там чудеса: там леший бродит,
    Русалка на ветвях сидит;"""

print(w + "\n" + v)


#3 strings are acting like an array and also can be checked for a length
for z in "meow":
    print(z)
x = "sea lions or seals?"
print(len(x))


#4 checking if word in a sentence and if not
poem = """    Там на неведомых дорожках
    Следы невиданных зверей;
    Избушка там на курьих ножках
    Стоит без окон, без дверей;"""
print("Там" in poem)

popyu = """    Там лес и дол видений полны;
    Там о заре прихлынут волны
    На брег песчаный и пустой,
    И тридцать витязей прекрасных"""
print("там" not in popyu)


#5 checking with "if"
stih = """  Чредой из вод выходят ясных,
    И с ними дядька их морской;
    Там королевич мимоходом
    Пленяет грозного царя;"""
if "вод" in stih:
  print("Yes, the russian 'waters' is here")

txt = """   Там в облаках перед народом
    Через леса, через моря
    Колдун несёт богатыря;
    В темнице там царевна тужит,"""
if "Маг" not in txt:
  print("No, 'mage' is not in there")


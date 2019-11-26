from my_CYK import Grammar

gram = Grammar('grammar.txt')
print("----------------------------------------")
print("-------------PYTHON COMPILER------------")
print("----------------------------------------")

print("Masukkan nama file : ", end="")
filename = input()

print("----------------------------------------")
print("------------Tunggu bentar ya------------")
print("----------------------------------------")
with open(filename,'r') as file:
    data = file.read()
    try :
        gram.parse(data)
    except :
        print("----------------------------------------")
        print("--------Kebanyakan programnya ): -------")
        print("----------------------------------------")
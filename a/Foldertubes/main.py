from my_CYK import Grammar
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help ="Menerima inputan nama file yang akan dibaca")
    args = parser.parse_args()
    gram = Grammar('grammar.txt')
    print("----------------------------------------")
    print("-------------PYTHON COMPILER------------")
    print("----------------------------------------")
    print("----------------------------------------")
    print("------------Tunggu bentar ya------------")
    print("----------------------------------------")
    with open(args.filename,'r') as file:
        data = file.read()
        try :
            gram.parse(data)
        except KeyboardInterrupt:
            print("----------------------------------------")
            print("--------Kebanyakan yaa programnya ): -------")
            print("----------------------------------------")
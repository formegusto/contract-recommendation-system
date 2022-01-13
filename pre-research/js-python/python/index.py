import sys


def getValue():
    print("value")


def getValueArgs(name, age):
    print("value")
    print(name, age)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        name = sys.argv[1]
        age = sys.argv[2]
        getValueArgs(name, age)
    else:
        getValue()

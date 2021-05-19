import configparser

def ReadConfig(filename='node.ini'):
    cf = configparser.ConfigParser()
    cf.read(filename, encoding='utf-8-sig')
    s = cf.sections() # 读取section
    # print(s)
    dict = {}
    for i in s:
        for j in cf.items(i):
            dict[j[0]] = j[1]

    return dict


if __name__ == '__main__':
    print(ReadConfig())
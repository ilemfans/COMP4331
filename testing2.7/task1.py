with open('COMP4331.txt', 'r') as f:
    data = f.readlines()  # txt中所有字符串读入data

    for line in data:
        odom = line.split()  # 将单个数据分隔开存好
        numbers_float = map(float, odom)  # 转化为浮点数

print data[0];
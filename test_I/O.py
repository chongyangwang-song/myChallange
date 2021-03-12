import sys
data = []
while True:
    # sys.stdout.write("请输入你的名字:")
    line = sys.stdin.readline().strip()
    data.append(line)
    if not line:
        print(data)
        break


import random
import collections

import sys
# while True:
#     line = sy
host_dict = {}
vm_dict = {}
# with open() as f:
#     lines = f.readlines()

# lines = [line.strip() for line in lines]

class Host:
    def __init__(self, name):
        self.name = name
        self.A_cpu = host_dict[name][0]/2
        self.B_cpu = host_dict[name][0]/2
        self.A_mem = host_dict[name][1]/2
        self.B_mem = host_dict[name][1]/2

    def putvm(self,vm):
        info = vm_dict[vm]
        cpu, mem, core = info
        if core == 0:
            if self.A_cpu >= cpu and self.A_mem >= mem: #优先放A节点
                self.A_cpu -= cpu
                self.A_mem -= mem
                return 'A'
            elif self.B_cpu >= cpu and self.B_mem >= mem:
                self.B_cpu -= cpu
                self.B_mem -= mem
                return 'B'
            else:
                return 'NULL'
        else:
            if self.A_cpu >= cpu/2 and self.A_mem >= mem/2 and self.B_cpu >= cpu/2 and self.B_mem >= mem/2:
                self.A_cpu -= cpu/2
                self.B_cpu -= cpu/2
                self.A_mem -= mem/2
                self.B_mem -= mem/2
                return  'ALL'
            else:
                return 'NULL'

    def delvm(self,vm,type):
        info = vm_dict[vm]
        cpu, mem, core = info
        if type == 'A':
            self.A_cpu += cpu
            self.A_mem += mem
        elif type == 'B':
            self.B_cpu += cpu
            self.B_mem += mem
        else:
            self.A_cpu += cpu/2
            self.A_mem += mem/2
            self.B_cpu += cpu/2
            self.B_mem += mem/2

class hostList:

    def __init__(self):
        self.allHost = []
        self.id_info = {}
        self.out = []

    def addHost(self):
        list_for_choice = list(host_dict.keys())
        lenth = len(list_for_choice)
        choice = random.randint(0, lenth-1)
        choice = list_for_choice[choice]
        newHost = Host(choice)
        self.allHost.append(newHost)

    def search_and_add(self, vm_name,vm_id):
        while True:

            if len(self.allHost) == 0:
                self.addHost()
            length = len(self.allHost)
            res = self.allHost[length-1].putvm(vm_name)
            if res != 'NULL':
                if res == 'A':
                    self.out.append([length-1,'A'])
                    # self.id_info[vm_id] = [vm_name, i, 'A']
                    return
                elif res == 'B':
                    self.out.append([length-1, 'B'])
                    # self.id_info[vm_id] = [vm_name, i, 'B']
                    return
                else:
                    self.out.append([length-1])
                    # self.id_info[vm_id] = [vm_name, i, 'ALL']
                    return
            else:
                self.addHost()



    def del_vm(self, id):
        vm_name, host_id, type = self.id_info[id]
        self.allHost[host_id].delvm(vm_name,type)

def main():
    #标准输入
    host_num = sys.stdin.readline().strip()
    host_num = int(host_num)
    # host_num = int(lines[0])
    for i in range(host_num):
        line = sys.stdin.readline().strip()
        temp = line.split(',')
        host_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4][:-1])]
        host_dict[host_name] = val

    vm_num = sys.stdin.readline().strip()
    vm_num = int(vm_num)
    for i in range(vm_num):
        line = sys.stdin.readline().strip()
        temp = line.split(',')
        vm_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3][:-1])]
        vm_dict[vm_name] = val
    day_num = sys.stdin.readline().strip()
    day_num = int(day_num)
    # data_index = host_num+2+vm_num+1
    data = []
    for i in range(day_num):
        requirement = sys.stdin.readline().strip()
        requirement = int(requirement)
        data_i = []
        for i in range(requirement):
            line = sys.stdin.readline().strip()
            data_i.append(line)
        data.append(data_i)

    my_hostList = hostList()
    out = []
    index = 0
    index_id = {}
    for a, day in enumerate(data):
        for line in day:
            add_or_del = line.split(',')[0][1:]
            ID = int(line.split(',')[-1][:-1])
            if add_or_del == 'add':
                vm_name = line.split(',')[1].strip()
                my_hostList.search_and_add(vm_name, ID)
            # else:
            #     # my_hostList.del_vm(ID)
            #     print('test')
        start_id = index
        temp = index
        index = len(my_hostList.allHost)
        name_indies = collections.OrderedDict()
        for idx, item in zip(range(temp, index), my_hostList.allHost[temp:index]):
            if item.name not in name_indies.keys():
                name_indies[item.name] = [idx]
            else:
                name_indies[item.name].append(idx)

        out.append('(purchase,' + ' ' + str(len(name_indies.keys())) + ')')
        for k, v in name_indies.items():
            out.append('(' + str(k) + ',' + ' ' + str(len(v)) + ')')

        out.append('(migration, 0)')

        for k, v in name_indies.items():
            for item in v:
                index_id[item] = start_id
                start_id += 1
        operate = my_hostList.out
        new_operate = []
        for line in operate:
            idx = line[0]
            new_index = index_id[idx]
            if len(line) == 1:
                new_operate.append('(' + str(new_index) + ')')
            else:
                new_operate.append('(' + str(new_index) + ',' + ' ' + line[1] + ')')

        out += new_operate
        my_hostList.out.clear()
        # if a%100 == 0:
        #     print('over')

    # with open('result.txt','w')as f:
    #     f.write('\n'.join(out))
    # end = time.time()
    # print('time consume',start-end)
    sys.stdout.write('\n'.join(out))  # 借
    sys.stdout.flush()
if __name__ == "__main__":
    main()

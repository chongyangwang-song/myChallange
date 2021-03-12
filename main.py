import random
import copy
import time

import sys
# while True:
#     line = sy
host_dict = {}
vm_dict = {}
PATH = '/data1/HUAWEI/training-1.txt'
with open(PATH) as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

host_num = int(lines[0])
for i in range(1, host_num+1):
    line = lines[i]
    temp = line.split(',')
    host_name = temp[0][1:]
    val = [int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4][:-1])]
    host_dict[host_name] = val
vm_num = int(lines[host_num+1])
for i in range(host_num+2,host_num+2+vm_num):
    line = lines[i]
    temp = line.split(',')
    vm_name = temp[0][1:]
    val = [int(temp[1]), int(temp[2]),int(temp[3][:-1])]
    vm_dict[vm_name] = val
day_num = int(lines[host_num+2+vm_num])
data_index = host_num+2+vm_num+1
data = []
for i in range(day_num):
    data_i = []
    data_num = int(lines[data_index])
    for item in lines[data_index+1:data_index+1+data_num]:
        data_i.append(item)
    data.append(data_i)
    data_index = data_index+data_num+1


class Host:
    def __init__(self, name):
        self.name = name
        self.A_cpu = host_dict[name][0]/2
        self.B_cpu = host_dict[name][0]/2
        self.A_mem = host_dict[name][1]/2
        self.B_mem = host_dict[name][1]/2

    def putvm(self,vm):
        info = vm_dict[vm]
        cpu,mem,core = info
        if core == 0:
            if self.A_cpu >=cpu and self.A_mem>=mem: #优先放A节点
                self.A_cpu -= cpu
                self.A_mem -= mem
                return 'A'
            elif self.B_cpu>=cpu and self.B_mem>=mem:
                self.B_cpu -= cpu
                self.B_mem -= mem
                return  'B'
            else:
                return 'NULL'
        else:
            if self.A_cpu>=cpu/2 and self.A_mem>=mem/2 and self.B_cpu>=cpu/2 and self.B_mem>=mem/2:
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
            self.A_cpu -= cpu
            self.A_mem -= mem
        elif type == 'B':
            self.B_cpu -= cpu
            self.B_mem -= mem
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
                    self.out.append('('+str(length-1)+','+' A'+')')
                    # self.id_info[vm_id] = [vm_name, i, 'A']
                    return
                elif res == 'B':
                    self.out.append('('+str(length-1)+','+' B'+')')
                    # self.id_info[vm_id] = [vm_name, i, 'B']
                    return
                else:
                    self.out.append('('+str(length-1)+')')
                    # self.id_info[vm_id] = [vm_name, i, 'ALL']
                    return
            else:
                self.addHost()


    def del_vm(self, id):
        vm_name, host_id, type = self.id_info[id]
        self.allHost[host_id].delvm(vm_name,type)

def main():
    my_hostList = hostList()
    out = []
    index = 0
    for a,day in enumerate(data):
        for line in day:
            add_or_del = line.split(',')[0][1:]
            ID = int(line.split(',')[-1][:-1])
            if add_or_del == 'add':
                vm_name = line.split(',')[1].strip()
                my_hostList.search_and_add(vm_name, ID)
            # else:
            #     # my_hostList.del_vm(ID)
            #     print('test')
        temp = index
        index = len(my_hostList.allHost)
        temp_host_list = my_hostList.allHost[temp:index]
        temp_dict = {}
        for item in temp_host_list:
            if item.name not  in temp_dict.keys():
                temp_dict[item.name] = 1
            else:
                temp_dict[item.name] += 1
        out.append('(purchase,'+' '+str(len(temp_dict.keys()))+')')
        for k,v in temp_dict.items():
            out.append('('+str(k)+','+' '+str(v)+')')
        out.append('(migration, 0)')
        operate = my_hostList.out
        out += operate
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

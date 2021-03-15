import random
import time
import sys
from collections import defaultdict
from collections import OrderedDict
start = time.time()
SERVER = False
TIME = True

host_dict = {}
vm_dict = {}
host_cpu_mem = defaultdict(list)
vm_cpu_mem = defaultdict(list)
host_cpu_mem_sorted = OrderedDict()
vm_cpu_mem_sorted = OrderedDict()

SPLIT = 10

if not SERVER:

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
        host_cpu_mem[int(temp[1])/int(temp[2])].append(host_name)
    vm_num = int(lines[host_num+1])
    for i in range(host_num+2,host_num+2+vm_num):
        line = lines[i]
        temp = line.split(',')
        vm_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]),int(temp[3][:-1])]
        vm_cpu_mem[int(temp[1]) / int(temp[2])].append(vm_name)
        vm_dict[vm_name] = val

    host_cpu_mem_keys = list(host_cpu_mem.keys())
    for i in sorted(host_cpu_mem_keys):
        host_cpu_mem_sorted[i] = host_cpu_mem[i]
    vm_cpu_mem_keys = list(vm_cpu_mem.keys())
    for i in sorted(vm_cpu_mem_keys):
        vm_cpu_mem_sorted[i] = vm_cpu_mem[i]
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
else:
    host_num = sys.stdin.readline().strip()
    host_num = int(host_num)
    # host_num = int(lines[0])
    for i in range(host_num):
        line = sys.stdin.readline().strip()
        temp = line.split(',')
        host_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4][:-1])]
        host_cpu_mem[int(temp[1]) / int(temp[2])].append(host_name)
        host_dict[host_name] = val

    vm_num = sys.stdin.readline().strip()
    vm_num = int(vm_num)
    for i in range(vm_num):
        line = sys.stdin.readline().strip()
        temp = line.split(',')
        vm_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3][:-1])]
        vm_dict[vm_name] = val
        vm_cpu_mem[int(temp[1]) / int(temp[2])].append(vm_name)

    host_cpu_mem_keys = list(host_cpu_mem.keys())
    for i in sorted(host_cpu_mem_keys):
        host_cpu_mem_sorted[i] = host_cpu_mem[i]
    vm_cpu_mem_keys = list(vm_cpu_mem.keys())
    for i in sorted(vm_cpu_mem_keys):
        vm_cpu_mem_sorted[i] = vm_cpu_mem[i]
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

host_dict_keys_list = list(host_dict.keys())
HOST_DICT_LEN = len(host_dict_keys_list)
#######划分服务器#######################################################################
host_split_step = int(len(host_cpu_mem)/SPLIT)
host_split_list = []
host_cpu_mem_sorted_keys = list(host_cpu_mem_sorted.keys())
host_cpu_mem_sorted_keys_split = []
for i in range(SPLIT-1):
    host_cpu_mem_sorted_keys_split.append(host_cpu_mem_sorted_keys[host_split_step*i:host_split_step*(i+1)])
host_cpu_mem_sorted_keys_split.append(host_cpu_mem_sorted_keys[host_split_step*(SPLIT-1):])
host_split_list = []
for i in host_cpu_mem_sorted_keys_split:
    temp = []
    for j in i:
        temp += host_cpu_mem_sorted[j]
    host_split_list.append(temp)

######划分虚拟机########################################################################
vm_split_step = int(len(vm_cpu_mem)/SPLIT)
vm_split_list = []
vm_cpu_mem_sorted_keys = list(vm_cpu_mem_sorted.keys())
vm_cpu_mem_sorted_keys_split = []
for i in range(SPLIT-1):
    vm_cpu_mem_sorted_keys_split.append(vm_cpu_mem_sorted_keys[vm_split_step*i:vm_split_step*(i+1)])
vm_cpu_mem_sorted_keys_split.append(vm_cpu_mem_sorted_keys[vm_split_step*(SPLIT-1):])
vm_split_list = []
for i in vm_cpu_mem_sorted_keys_split:
    temp = []
    for j in i:
        temp += vm_cpu_mem_sorted[j]
    vm_split_list.append(temp)
#######建立名称等级索引#################################################################
host_rank = {}
for idx,i in enumerate(host_split_list):
    for j in i:
        host_rank[j] = idx
vm_rank = {}
for idx,i in enumerate(vm_split_list):
    for j in i:
        vm_rank[j] = idx
    
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
                return 'B'
            else:
                return 'NULL'
        else:
            if self.A_cpu>=cpu/2 and self.A_mem>=mem/2 and self.B_cpu>=cpu/2 and self.B_mem>=mem/2:
                self.A_cpu -= cpu/2
                self.B_cpu -= cpu/2
                self.A_mem -= mem/2
                self.B_mem -= mem/2
                return 'ALL'
            else:
                return 'NULL'

    def available(self,vm):
        info = vm_dict[vm]
        cpu,mem,core = info
        if core == 0:
            if self.A_cpu >=cpu and self.A_mem>=mem: #优先放A节点
                return True
            elif self.B_cpu>=cpu and self.B_mem>=mem:
                return True
            else:
                return False
        else:
            if self.A_cpu>=cpu/2 and self.A_mem>=mem/2 and self.B_cpu>=cpu/2 and self.B_mem>=mem/2:
                return True
            else:
                return False

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
        self.rank_store = []
        for i in range(SPLIT):
            self.rank_store.append([])

    def addHost(self,vm_name):
        rank = vm_rank[vm_name]
        while True:
            select = random.randint(0,len(host_split_list[rank])-1)
            host_name = host_split_list[rank][select]
            host = Host(host_name)
            if host.available(vm_name):
                break
        self.allHost.append(host)
        self.rank_store[rank].append(len(self.allHost)-1)

    def search_and_add(self, vm_name,vm_id):
        if len(self.allHost) == 0:
            self.addHost(vm_name)
        rank = vm_rank[vm_name]
        for i in self.rank_store[rank]:
            res = self.allHost[i].putvm(vm_name)
            if res != 'NULL':
                self.upate_out(i,res,vm_id,vm_name)
                return
        self.addHost(vm_name)
        res = self.allHost[-1].putvm(vm_name)
        self.upate_out(len(self.allHost)-1,res,vm_id,vm_name)


    def upate_out(self,i,AorB,vm_id,vm_name):
        if AorB == 'A':
            self.out.append([i,'A'])
            self.id_info[vm_id] = [vm_name, i, 'A']
        elif AorB == 'B':
            self.out.append([i, 'B'])
            self.id_info[vm_id] = [vm_name, i, 'B']
        else:
            self.out.append([i])
            self.id_info[vm_id] = [vm_name, i, 'ALL']

    def del_vm(self, id):
        vm_name,host_id,type = self.id_info[id]
        self.allHost[host_id].delvm(vm_name, type)

def main():
    my_hostList = hostList()
    out = []
    index = 0
    index_id = {}
    ITER = 0
    for day in data:
        for line in day:
            add_or_del = line.split(',')[0][1:]
            ID = int(line.split(',')[-1][:-1])
            if add_or_del == 'add':
                vm_name = line.split(',')[1].strip()
                my_hostList.search_and_add(vm_name, ID)
            else:
                my_hostList.del_vm(ID)
        start_id = index
        temp = index
        index = len(my_hostList.allHost)
        name_indies = OrderedDict()
        for idx,item in zip(range(temp,index),my_hostList.allHost[temp:index]):
            if item.name not in name_indies.keys():
                name_indies[item.name] = [idx]
            else:
                name_indies[item.name].append(idx)

        out.append('(purchase,'+' '+str(len(name_indies.keys()))+')')
        for k,v in name_indies.items():
            out.append('('+str(k)+','+' '+str(len(v))+')')

        out.append('(migration, 0)')

        for k,v in name_indies.items():
            for item in v:
                index_id[item] = start_id
                start_id += 1
        operate = my_hostList.out
        new_operate = []
        for line in operate:
            idx = line[0]
            new_index = index_id[idx]
            if len(line) == 1:
                new_operate.append('('+str(new_index)+')')
            else:
                new_operate.append('('+str(new_index)+','+' '+line[1]+')')

        out += new_operate
        my_hostList.out.clear()
        ITER +=1
        if TIME:
            if ITER % 100 == 0:
                print('over')
        # if a%100 == 0:
        #     print('over')

    # with open('result.txt','w')as f:
    #     f.write('\n'.join(out))
    end = time.time()
    if TIME:
        print('time consume',end-start)
    sys.stdout.write('\n'.join(out))  # 借
    sys.stdout.flush()
if __name__ == "__main__":
    main()

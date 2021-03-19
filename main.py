import random
import time
import sys
from collections import defaultdict
from collections import OrderedDict
import copy
start = time.time()
SERVER = False
TIME = True

host_dict = {}
vm_dict = {}
host_cpu_mem = defaultdict(list)
vm_cpu_mem = defaultdict(list)
host_cpu_mem_sorted = OrderedDict()
vm_cpu_mem_sorted = OrderedDict()

SPLIT = 1
RATIO = 1  ##使用百分之八十
SORT_USE_PRICE = True # 是否使用价格排序
if not SERVER:

    PATH = '/data1/HUAWEI/training-1.txt'
    with open(PATH) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    host_num = int(lines[0])
    for i in range(1, host_num + 1):
        line = lines[i]
        temp = line.split(',')
        host_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4][:-1])]
        host_dict[host_name] = val
        host_cpu_mem[int(temp[1]) / int(temp[2])].append(host_name)
    vm_num = int(lines[host_num + 1])
    for i in range(host_num + 2, host_num + 2 + vm_num):
        line = lines[i]
        temp = line.split(',')
        vm_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3][:-1])]
        vm_cpu_mem[int(temp[1]) / int(temp[2])].append(vm_name)
        vm_dict[vm_name] = val

    host_cpu_mem_keys = list(host_cpu_mem.keys())
    for i in sorted(host_cpu_mem_keys):
        host_cpu_mem_sorted[i] = host_cpu_mem[i] #排好序的cpu/mem比例-》对应服务器列表
    vm_cpu_mem_keys = list(vm_cpu_mem.keys())
    for i in sorted(vm_cpu_mem_keys):
        vm_cpu_mem_sorted[i] = vm_cpu_mem[i]
    day_num = int(lines[host_num + 2 + vm_num])
    data_index = host_num + 2 + vm_num + 1
    data = []
    for i in range(day_num):
        data_i = []
        data_num = int(lines[data_index])
        for item in lines[data_index + 1:data_index + 1 + data_num]:
            data_i.append(item)
        data.append(data_i)
        data_index = data_index + data_num + 1
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
host_split_step = int(len(host_cpu_mem) * RATIO / SPLIT)
# host_split_list = []
LEN_KEYS = len(host_cpu_mem_sorted.keys())
host_cpu_mem_sorted_keys = list(host_cpu_mem_sorted.keys())[
                           int(((1 - RATIO) / 2) * LEN_KEYS):int((1 - (1 - RATIO) / 2) * LEN_KEYS)]
host_cpu_mem_sorted_keys_split = []
for i in range(SPLIT - 1):
    host_cpu_mem_sorted_keys_split.append(host_cpu_mem_sorted_keys[host_split_step * i:host_split_step * (i + 1)])
host_cpu_mem_sorted_keys_split.append(host_cpu_mem_sorted_keys[host_split_step * (SPLIT - 1):])
host_split_list = []
for i in host_cpu_mem_sorted_keys_split:
    temp = []
    for j in i:
        temp += host_cpu_mem_sorted[j]
    host_split_list.append(temp)
# 按照价格排序
for i, item in enumerate(host_split_list):
    host_split_list[i] = sorted(item, key=lambda host: host_dict[host][2])
######划分虚拟机########################################################################
vm_split_step = int(len(vm_cpu_mem) / SPLIT)
# vm_split_list = []
vm_cpu_mem_sorted_keys = list(vm_cpu_mem_sorted.keys())
vm_cpu_mem_sorted_keys_split = []
for i in range(SPLIT - 1):
    vm_cpu_mem_sorted_keys_split.append(vm_cpu_mem_sorted_keys[vm_split_step * i:vm_split_step * (i + 1)])
vm_cpu_mem_sorted_keys_split.append(vm_cpu_mem_sorted_keys[vm_split_step * (SPLIT - 1):])
vm_split_list = []
for i in vm_cpu_mem_sorted_keys_split:
    temp = []
    for j in i:
        temp += vm_cpu_mem_sorted[j]
    vm_split_list.append(temp)
#######建立名称等级索引#################################################################
host_rank = {}
for idx, i in enumerate(host_split_list):
    for j in i:
        host_rank[j] = idx
vm_rank = {}
for idx, i in enumerate(vm_split_list):
    for j in i:
        vm_rank[j] = idx


class Host:
    def __init__(self, name):
        self.name = name
        self.A_cpu = host_dict[name][0] / 2
        self.B_cpu = host_dict[name][0] / 2
        self.A_mem = host_dict[name][1] / 2
        self.B_mem = host_dict[name][1] / 2
        self.contains_vm = []
        self.history = []
    def putvm(self, vm_name, vm_id):
        info = vm_dict[vm_name]
        cpu, mem, core = info
        if core == 0:
            if self.A_cpu >= cpu and self.A_mem >= mem:  # 优先放A节点
                self.A_cpu -= cpu
                self.A_mem -= mem
                # self.contains_vm.append((vm_name, vm_id, 'A'))
                # self.history.append(('add',vm_name, vm_id, 'A'))
                return 'A'
            elif self.B_cpu >= cpu and self.B_mem >= mem:
                self.B_cpu -= cpu
                self.B_mem -= mem
                # self.contains_vm.append((vm_name, vm_id, 'B'))
                # self.history.append(('add',vm_name, vm_id, 'B'))
                return 'B'
            else:
                return 'NULL'
        else:
            if self.A_cpu >= cpu / 2 and self.A_mem >= mem / 2 and self.B_cpu >= cpu / 2 and self.B_mem >= mem / 2:
                self.A_cpu -= cpu / 2
                self.B_cpu -= cpu / 2
                self.A_mem -= mem / 2
                self.B_mem -= mem / 2
                # self.contains_vm.append((vm_name, vm_id, 'ALL'))
                # self.history.append((vm_name, vm_id, 'ALL'))
                return 'ALL'
            else:
                return 'NULL'

    def available(self, vm):
        info = vm_dict[vm]
        cpu, mem, core = info
        if core == 0:
            if self.A_cpu >= cpu and self.A_mem >= mem:  # 优先放A节点
                return True
            elif self.B_cpu >= cpu and self.B_mem >= mem:
                return True
            else:
                return False
        else:
            if self.A_cpu >= cpu / 2 and self.A_mem >= mem / 2 and self.B_cpu >= cpu / 2 and self.B_mem >= mem / 2:
                return True
            else:
                return False

    def delvm(self, vm, id, type):
        info = vm_dict[vm]
        cpu, mem, core = info
        if type == 'A':
            self.A_cpu += cpu
            self.A_mem += mem
            # self.contains_vm.remove((vm, id, 'A'))
            # self.history.append(('del',vm, id, 'A'))
        elif type == 'B':
            self.B_cpu += cpu
            self.B_mem += mem
            # self.contains_vm.remove((vm, id, 'B'))
            # self.history.append(('del', vm, id, 'B'))
        else:
            self.A_cpu += cpu / 2
            self.A_mem += mem / 2
            self.B_cpu += cpu / 2
            self.B_mem += mem / 2
            # self.contains_vm.remove((vm, id, 'ALL'))
            # self.history.append(('del', vm, id, 'ALL'))


class hostList:
    def __init__(self):
        self.allHost = []
        self.id_info = {}
        self.out = []
        # self.rank_store = []
        # for i in range(SPLIT):
        #     self.rank_store.append([])

    def addHost(self, vm_name):
        rank = vm_rank[vm_name]
        # select = random.randint(0,len(host_split_list[rank])-1)
        # host_name = host_split_list[rank][select]
        # host = Host(host_name)
        if not SORT_USE_PRICE:
            random.shuffle(host_split_list[rank])
        for host_name in host_split_list[rank]:
            host = Host(host_name)
            if host.available(vm_name):
                break
        self.allHost.append(host)
        # self.rank_store[rank].append(len(self.allHost) - 1)

    def search_and_add(self, add_ifo, start):
        store = []
        length = len(self.allHost)

        if length !=0:
            index = sorted(range(length), key=lambda k: self.allHost[k].A_cpu+self.allHost[k].B_cpu
                   +self.allHost[k].A_mem+self.allHost[k].B_mem)
            remove = []
            for vm in add_ifo:
                for host_id in range(index):
                    res = self.allHost[host_id].putvm(vm[0],vm[1])
                    if res != 'NULL':
                        self.upate_out(host_id,res,vm[1],vm[0])
                        remove.append(vm)
                        store.append(vm[2])
                        break
            for item in remove:
                add_ifo.remove(item)

        while len(add_ifo)!=0:
            max = add_ifo[0]
            self.addHost(max[0])
            id = len(self.allHost) - 1
            remove = []
            for vm in add_ifo:
                res = self.allHost[-1].putvm(vm[0],vm[1])
                if res != 'NULL':
                    self.upate_out(id, res, vm[1], vm[0])
                    remove.append(vm)
                    store.append(vm[2])
            for item in remove:
                add_ifo.remove(item)
        return store


            # index1.clear()
        # if len(self.allHost) == 0:
        #     self.addHost(vm_name)
        # rank = vm_rank[vm_name]
        # for i in self.rank_store[rank]:
        #     res = self.allHost[i].putvm(vm_name, vm_id)
        #     if res != 'NULL':
        #         self.upate_out(i, res, vm_id, vm_name)
        #         return
        # self.addHost(vm_name)
        # res = self.allHost[-1].putvm(vm_name, vm_id)
        # self.upate_out(len(self.allHost) - 1, res, vm_id, vm_name)

    def upate_out(self, i, AorB, vm_id, vm_name):
        if AorB == 'A':
            self.out.append([i, 'A'])
            self.id_info[vm_id] = [vm_name, i, 'A']
        elif AorB == 'B':
            self.out.append([i, 'B'])
            self.id_info[vm_id] = [vm_name, i, 'B']
        else:
            self.out.append([i])
            self.id_info[vm_id] = [vm_name, i, 'ALL']

    def del_vm(self, id):
        vm_name, host_id, type = self.id_info[id]
        self.allHost[host_id].delvm(vm_name, id, type)


def main():
    my_hostList = hostList()
    out = []
    index = 0
    index_id = {}
    ITER = 0
    start = 0
    for day in data:
        add_require = [item for item in day if item[1:4] == 'add']
        del_require = [item for item in day if item[1:4] == 'del']
        add_vm = [(item.split(',')[1].strip(), item.split(',')[2].strip()[:-1]) for item in add_require]
        del_vm = [item.split(',')[1][:-1].strip() for item in del_require]
        add_info = []
        for idx, vm_info in enumerate(add_vm):
            add_info.append(vm_info + (idx,))

        # 根据虚拟机的cpu+mem定义虚拟机的大小
        add_info = sorted(add_info, key=lambda vm: vm_dict[vm[0]][0] + vm_dict[vm[0]][1], reverse=True)
        # index_store = [item[2] for item in add_info]

        index_store = my_hostList.search_and_add(add_info, start)
        for vm in del_vm:
            my_hostList.del_vm(vm)

        start_id = index
        temp = index
        index = len(my_hostList.allHost)
        name_indies = OrderedDict()
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
        temp_operate = list(range(len(new_operate)))
        for i, idx in enumerate(index_store):
            temp_operate[idx] = new_operate[i]
        out += temp_operate
        my_hostList.out.clear()
        ITER += 1
        if TIME:
            if ITER % 100 == 0:
                print('over')
                # if a%100 == 0:
                #     print('over')

    # with open('result.txt','w')as f:
    #     f.write('\n'.join(out))
    end = time.time()
    if TIME:
        print('time consume', end - start)
    sys.stdout.write('\n'.join(out))  # 借
    sys.stdout.flush()


if __name__ == "__main__":
    main()

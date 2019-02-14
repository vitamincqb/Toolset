class Node:
    # 节点的初始化
    def __init__(self, data):
        self.data = data
        self.next = None


class SingleList:
    # 链表的初始化
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    # 在链表尾部添加结点数据
    def append(self, node_obj):
        if self.head is None:
            self.head = node_obj
            self.tail = node_obj
            self.current = node_obj
        else:
            self.tail.next = node_obj
            self.tail = node_obj

    # 在指定的结点位置的前面插入一个新的结点(起点为1)
    def insert(self, i, node_obj):
        length = self.getlength()
        # 先处理几个特殊位置的结点插入
        if i <= 0:
            print('插入位置错误, 最小位置为整数1')
            return
        if i == 1:
            node_obj.next = self.head
            self.head = node_obj
            self.current = node_obj
        elif i > length:
            self.append(node_obj)
        # 正常位置的插入
        elif i > 1 and i <= length:
            # 查找待插入位置的上一个结点
            temp = None
            for pos in range(1, i):
                temp = self.current
                self.current = self.current.next
            node_obj.next = temp.next
            temp.next = node_obj
            # 这个地方很关键，容易忽略
            self.current = self.head
        else:
            print('没有这么结点，插入位置错误，将直接插入在链表的结尾!')
            self.append(node_obj)
            
    # 获取链表的长度
    def getlength(self):
        length = 0
        for info in self:
            length += 1
        return length

    # 获取链表第i个节点的数据
    def getElem(self, i):
        # tapm为要获取的结点
        temp = None
        for pos in range(1, i+1):
                temp = self.current
                self.current = self.current.next
        # 找到数据后，将current重新指定表头
        # 这个地方很关键，容易忽略
        self.current = self.head
        return temp

    # 删除指定位置的节结
    def delete(self, i):
        length = self.getlength()
        if i <= 0 or i > length:
            print('位置错误！')
            return
        # 查找待删除位置的上一个结点
        temp = None
        if i == 1:
            temp = self.head
            self.current = self.head.next
            self.head = self.head.next
            del temp
            return
        else:    
            for pos in range(1, i):
                temp = self.current
                self.current = self.current.next
            deldata = temp.next
            if i == length:
                temp.next = None
            else:
                temp.next = deldata.next
            # 这个地方很关键，容易忽略
            del deldata
            self.current = self.head
            return

    # 链表反转
    def reverse(self):
        length = self.getlength()

        if length <= 1:
            print('链接为空或长度为1，不用反转')
            return
        else:
            for pos in range(1, length):
                temp = self.getElem(length)
                pre_temp = self.getElem(length-1)
                self.tail = pre_temp
                self.insert(pos, temp)
                self.tail.next = None
            return

    # 可迭代条件
    def __iter__(self):
        return self

    # 迭代器条件
    def __next__(self):
        if self.current is not None:
            temp = self.current
            self.current = self.current.next
            return temp
        else:
            # 如果current到了表尾，则将current重新指向表头
            self.current = self.head
            raise StopIteration

    # 打印整个链表记录
    def print_list_data(self):
        print('链表记录如下：')
        for info in self:
            print(info.data)
        print('记录输出完毕!')


def main():
    singlelist = SingleList()
    # 给单链表添加数据
    for info in ['张三', '李四', '王五', '赵六']:
        singlelist.append(Node(info))

    # 测试结果是否正确
    # 打印所有记录
    singlelist.print_list_data()
    print('获取链表长度')
    print(singlelist.getlength(), '\n')

    print('\n分别获取第1，2，最后位置的数据')
    print(f'位置1:{singlelist.getElem(1).data}---'
          f'位置2:{singlelist.getElem(2).data}---'
          f'位置End{singlelist.getlength()}:{singlelist.getElem(singlelist.getlength()).data}')

    # 反转链表
    print('反转链表')
    singlelist.reverse()
    singlelist.print_list_data()

    # 在指定位置1,2, 最后位置插入结点
    print('\n位置1插入insert1')
    singlelist.insert(1, Node('insert1'))
    singlelist.print_list_data()
    print('\n位置2插入insert2')
    singlelist.insert(2, Node('insert2'))
    singlelist.print_list_data()
    print('\n位置End插入insertEnd')
    singlelist.insert(singlelist.getlength(), Node('insertEnd'))
    singlelist.print_list_data()
    print(f'最后位置{singlelist.getlength()}:{singlelist.getElem(singlelist.getlength()).data}')

    # 删除指定位置1,2,最后位置的结点
    print('\n删除位置1的数据')
    singlelist.delete(1)
    singlelist.print_list_data()
    print('\n删除位置2的数据')
    singlelist.delete(2)
    singlelist.print_list_data()
    print('删除位置End的数据:', singlelist.getlength(),'-->', singlelist.getElem(singlelist.getlength()).data)
    singlelist.delete(singlelist.getlength())
    singlelist.print_list_data()
    print(f'\n最后位置{singlelist.getlength()}:{singlelist.getElem(singlelist.getlength())}')
    singlelist.delete(1)
    singlelist.print_list_data()
    singlelist.delete(1)
    singlelist.print_list_data()
    singlelist.delete(2)
    singlelist.print_list_data()
    singlelist.delete(1)
    singlelist.print_list_data()


if __name__ == "__main__":
    main()
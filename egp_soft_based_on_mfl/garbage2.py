# #multiple inputs in single line
# a,b, c= map(int, input().split())
# print(a+b+c)
#
#
#
# #strring reverse => hello world -- olleh dlrow
# s = input().split()
# rev = []
#
# for word in s:
#     rev.append(word[::-1])
#
# res = " ".join(rev)
# print(f"reverese list {res}")


# #HASHTABLE dict
# # s = input().split()
# # s = " ".join(s)
# # freq = {}
# # for ch in s:
# #     if ch in freq:
# #         freq[ch] += 1
# #     else:
# #         freq[ch] = 1
# #
# # print(freq)



# #queue from scratch
#
# class queue:
#     def __init__(self):
#         self.q = []
#
#     def enqueue(self, x):
#         self.q.append(x)
#
#     def dequeue(self):
#         if len(self.q) == 0:
#             return None
#         return self.q.pop(0)
#
#     def front(self):
#         if len(self.q) == 0:
#             return None
#         return self.q[0]
#
#     def is_empty(self):
#         return len(self.q) == 0
#
#
# q = queue()
#
# q.enqueue(56)
# q.enqueue(65)
# q.enqueue(76)
# q.dequeue()
# q.dequeue()
#
# print(q.q)


#single queue using import
# from collections import deque
#
# q = deque()
# q = deque([1,2,3])
# q.append(10)
# q.appendleft(5)
# q.pop()
# x = q.popleft()
# q.extend([4,5,6])
# q.extendleft([1,2])
# print(list(q))
# q.rotate(2)
# print(list(q))
# q.rotate(-2)
# print(list(q))
# q.reverse()
# print(list(q))
# print(q.count(1))
# print(q.index(1))




#linked list implementation
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def insert_at_position(self, index, value):
        if index == 0:
            self.insert_at_beginning(value)
            return

        new_node = Node(value)
        cur = self.head
        pos = 0

        while cur and pos < index - 1:
            cur = cur.next
            pos += 1

        if cur is None:
            return

        new_node.next = cur.next
        cur.next = new_node

    def search(self, key):
        cur = self.head
        while cur:
            if cur.value == key:
                return True
            cur = cur.next
        return False

    def delete_value(self, value):
        if self.head is None:
            return

        if self.head.value == value:
            self.head = self.head.next
            return

        cur = self.head
        while cur.next:
            if cur.next.value == value:
                cur.next = cur.next.next
                return
            cur = cur.next

    def delete_at_position(self, index):
        if self.head is None:
            return

        if index == 0:
            self.head = self.head.next
            return

        cur = self.head
        pos = 0

        while cur.next and pos < index - 1:
            cur = cur.next
            pos += 1

        if cur.next is None:
            return

        cur.next = cur.next.next

    def reverse(self):
        prev = None
        cur = self.head

        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        self.head = prev

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.value, end=" → ")
            cur = cur.next
        print("None")

    def size(self):
        count = 0
        cur = self.head
        while cur:
            count += 1
            cur = cur.next
        return count



t = linkedList()

t.insert_list(78)
t.insert_list(90)
t.print_list()
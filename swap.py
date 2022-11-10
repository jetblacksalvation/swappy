import copy


class List:
    class Node:
        def __init__(self, val, next=None, prev=None) -> None:
            self.val = val
            self.next: List.Node | None = next
            self.prev: List.Node | None = prev

        def find_index(self, depth):
            if depth == 0:
                return self
            if self.next:
                return self.next.find_index(depth - 1)
            raise IndexError

        def find_value(self, val):
            if self.val == val:
                return self
            if self.next:
                return self.next.find_value(val)

        def find_end(self):
            if self.next:
                return self.next.find_end()
            return self

        def print_list(self):
            print(self.val)
            if self.next:
                self.next.print_list()

        def print_back(self):
            print(self.val)
            if self.prev:
                self.prev.print_back()

        def print_extra(self):
            if self.prev and self.next:
                print(
                    f"Node with value {self.val}'s previous Node has value {self.prev.val}, and it's next Node has value {self.next.val}."
                )
            elif self.prev:
                print(
                    f"Node with value {self.val}'s previous Node has value {self.prev.val}, and does not have a next Node."
                )
            elif self.next:
                print(
                    f"Node with value {self.val}'s next Node has value {self.next.val}, and does not have a previous Node."
                )
            if self.next:
                self.next.print_extra()

        def move_through_backwards(self):
            pass

    def __init__(self, val=None) -> None:
        self.root: List.Node = List.Node(val)
        self.len = 1

    def insert_front(self, val):
        old_root = self.root
        new_root = List.Node(val, old_root)
        old_root.prev = new_root
        self.root = new_root
        self.len += 1

    def insert(self, index, val):
        if index >= self.len:
            self.append(val)
            return
        if abs(index) >= self.len or index == 0:
            old_root = self.root
            new_root = List.Node(val, old_root)
            old_root.prev = new_root
            self.root = new_root
            self.len += 1
            return
        old_node = self.get_index(index)
        prev = old_node.prev
        new_node = List.Node(val, old_node, prev)
        prev.next = new_node
        old_node.prev = new_node
        self.len += 1

    def pop(self, index=None):
        if index is None:
            self.get_index(self.len - 2).next = None
            return
        if index == 0:
            self.root = self.root.next
            self.root.prev = None
        else:
            current = self.get_index(index)
            prev = current.prev
            next = current.next
            if next:
                next.prev = prev
            if prev:
                prev.next = next
        self.len -= 1

    def append(self, val):
        end = self.root.find_end()
        end.next = List.Node(val, None, end)
        self.len += 1

    def remove(self, val):
        if self.root.val == val:
            self.root = self.root.next
            self.root.prev = None
            return
        if found := self.root.find_value(val):
            prev = found.prev
            next = found.next
            if next:
                next.prev = prev
            prev.next = next
            return
        raise IndexError

    def print_list(self, *, backwards=False):
        if backwards:
            self.root.find_end().print_back()
        else:
            self.root.print_list()

    def print_index(self, index):
        print(self.get_index(index).val)

    def get_index(self, index):
        return self.root.find_index(index)

    def print_extra(self):
        self.root.print_extra()

    def reverse(self):
        old_node = copy.copy(self.root)
        new_list = List(old_node.find_index(self.len - 1).val)
        for i in range(self.len - 2, -1, -1):
            new_list.append(old_node.find_index(i).val)
        self.root = new_list.root
        
    def swap(self, node1, node2):
        prev = node1.prev
        next = node2.next
        if prev and next:
            node1.next = next
            node1.prev = node2
            node2.next = node1
            node2.prev = prev
            prev.next = node2
            next.prev = node1
            # "normal" case
            pass
        elif not prev and next:
            # root case
            node1.prev = node2
            node2.prev = None
            node2.next = node1
            node1.next = next
            next.prev =node1
            self.root = node2
            pass
        elif prev and not next:
            # end case
            prev.next = node2
            node1.prev = node2
            node2.next = node1
            node1.next = None
            node2.prev = prev
            pass
        else:
            self.root = node2
            node2.next = node1
            node2.prev = None   
            node1.prev = node2
            node1.next = None
            # only things in the list
            pass
    
    def swap_all(self):
        for i in range(self.len // 2):
            temp = self.root.find_index(i * 2)
            self.swap(temp, temp.next)

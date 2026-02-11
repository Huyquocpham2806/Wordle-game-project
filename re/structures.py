# Cài đặt Stack
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
        self.count += 1

    def pop(self):
        if self.is_empty():
            return None
        
        value = self.top.value
        self.top = self.top.next
        self.count -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.top.value

    def is_empty(self):
        return self.top is None

    def size(self):
        return self.count
    
    def to_list(self):
        result = []
        current = self.top
        while current:
            result.append(current.value)
            current = current.next
        return result[::-1]
    

# Cài đặt SortedLinkedList cho bảng xếp hạng
class ListNode:
    def __init__(self, name, password, avg_time, total_time, total_games):
        self.name = name
        self.password = password  
        self.avg_time = avg_time 
        self.total_time = total_time
        self.total_games = total_games
        self.next = None

class SortedLinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    # Hàm dùng để sắp xếp người chơi theo thứ tự từ trên xuống
    def insert_sorted(self, name, password, avg_time, total_time, total_games):
        new_node = ListNode(name, password, avg_time, total_time, total_games)
        
        if total_time > 0:
            new_val = avg_time
        else:
            new_val = 999999 

        if self.head is None:
            self.head = new_node
            return

        if self.head.total_games:
            head_val = self.head.avg_time
        else:
            head_val = 999999

        if new_val < head_val:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while current.next:
            if current.next.total_games > 0:
                next_val = current.next.avg_time
            else:   
                next_val = 999999
            if new_val < next_val:
                break
            current = current.next
        
        new_node.next = current.next
        current.next = new_node

    # Hàm tìm người chơi có tồn tại hay chưa
    def find_user(self, name):
        current = self.head
        while current:
            if current.name == name:
                return {
                    'name': current.name, 
                    'pass': current.password,
                    'score': current.avg_time,
                    'total_time': current.total_time,
                    'total_game': current.total_games
                }
            current = current.next
        return None

    # Hàm dùng để tìm người chơi và sửa điểm
    def get_node(self, name):
        current = self.head
        while current:
            if current.name == name:
                return current
            current = current.next
        return None
    
    # Hàm dùng để xóa tên người chơi trên bảng xếp hạng cũ
    def remove(self, name):
        current = self.head
        previous = None

        if not current:
            return False
        
        if current.name == name:
            self.head = current.next
            return True
        
        while current:
            if current.name == name:
                previous.next = current.next
                return True
            
            previous = current
            current = current.next

    # Hàm trả về bảng xếp hạng đươi dạng list
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append({
                'name': current.name,
                'pass': current.password,
                'score': current.avg_time,
                'total_time': current.total_time,
                'total_game': current.total_games
            })
            current = current.next
        return result
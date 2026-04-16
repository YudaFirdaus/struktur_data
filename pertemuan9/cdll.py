class SongNode:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.next = None  # Pointer ke depan
        self.prev = None  # Pointer ke belakang

class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current = None

    def add_song(self, title, artist):
        new_node = SongNode(title, artist)
        if not self.head:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node
        else:
            last = self.head.prev
            last.next = new_node
            new_node.prev = last
            new_node.next = self.head
            self.head.prev = new_node

    def delete_current(self):
        if not self.current: return
        
        if self.current.next == self.current: # Jika sisa 1 lagu
            self.head = None
            self.current = None
        else:
            p = self.current.prev
            n = self.current.next
            p.next = n
            n.prev = p
            if self.current == self.head:
                self.head = n
            self.current = n

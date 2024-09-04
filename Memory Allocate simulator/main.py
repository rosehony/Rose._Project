class MemoryBlock:
    def __init__(self, size):
        self.size = size
        self.allocated = False
        self.process_id = None

    def allocate(self, process_id):
        self.allocated = True
        self.process_id = process_id

    def free(self):
        self.allocated = False
        self.process_id = None

    def __repr__(self):
        return f"{'Allocated' if self.allocated else 'Free'} block of size {self.size} (Process ID: {self.process_id})"


class MemoryManager:
    def __init__(self, memory_size, block_sizes):
        self.memory = [MemoryBlock(size) for size in block_sizes]
        self.total_memory = memory_size

    def first_fit(self, process_id, process_size):
        for block in self.memory:
            if not block.allocated and block.size >= process_size:
                block.allocate(process_id)
                self.display_fragmentation()
                return f"Process {process_id} allocated in {block.size} size block"
        self.display_fragmentation()
        return "No suitable block found for first-fit allocation"

    def best_fit(self, process_id, process_size):
        best_block = None
        for block in self.memory:
            if not block.allocated and block.size >= process_size:
                if best_block is None or block.size < best_block.size:
                    best_block = block
        if best_block:
            best_block.allocate(process_id)
            self.display_fragmentation()
            return f"Process {process_id} allocated in {best_block.size} size block"
        self.display_fragmentation()
        return "No suitable block found for best-fit allocation"

    def free_memory(self, process_id):
        for block in self.memory:
            if block.allocated and block.process_id == process_id:
                block.free()
                self.display_fragmentation()
                return f"Process {process_id} memory freed"
        self.display_fragmentation()
        return "No memory found for the given process ID"

    def display_memory(self):
        for i, block in enumerate(self.memory):
            print(f"Block {i + 1}: {block}")

    def display_fragmentation(self):
        free_memory = sum(block.size for block in self.memory if not block.allocated)
        fragmented_memory = sum(block.size for block in self.memory if not block.allocated and block.size < 50)  # Assuming 50 as a threshold for fragmentation
        fragmentation_percentage = (fragmented_memory / free_memory) * 100 if free_memory else 0
        print(f"\nTotal Free Memory: {free_memory}")
        print(f"Fragmented Memory: {fragmented_memory}")
        print(f"Fragmentation Percentage: {fragmentation_percentage:.2f}%\n")


def main():
    memory_size = 1000
    block_sizes = [100, 500, 200, 300, 600]

    manager = MemoryManager(memory_size, block_sizes)

    print("Initial Memory Blocks:")
    manager.display_memory()

    print("\nAllocating processes using First-Fit:")
    print(manager.first_fit(1, 120))
    print(manager.first_fit(2, 200))
    manager.display_memory()

    print("\nFreeing memory of Process 1:")
    print(manager.free_memory(1))
    manager.display_memory()

    print("\nAllocating processes using Best-Fit:")
    print(manager.best_fit(3, 180))
    print(manager.best_fit(4, 100))
    manager.display_memory()

if __name__ == "__main__":
    main()



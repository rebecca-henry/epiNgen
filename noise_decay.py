from CMCed.chunk_noise import add_noise_to_utility
from CMCed.retrieve import retrieve_memory_chunk
from CMCed.debugging import report_memory_contents
from CMCed.decay import decay_all_memory_chunks

# Define a memory store for sandwich working_memory with initial utilities
working_memory = {
    'fries': {'name': 'fries', 'utility': 10, 'taste': 'salty'},
    'salad': {'name': 'salad', 'utility': 5, 'taste': 'fresh'},
    'chips': {'name': 'chips', 'utility': 7, 'taste': 'crispy'}
}

# Wrap the working_memory in a dictionary as decay_all_memory_chunks expects a collection of stores
memories = {'working_memory_dictionary': working_memory}

# Add noise to each chunk's utility to simulate variability
print("\nAdding noise to utilities...")
add_noise_to_utility(working_memory,  scalar=2.0)

# Provide a detailed report of memory contents after noise addition
print("\nDetailed Memory Report after Noise Addition:")
report_memory_contents(working_memory)

# Apply decay to all memory chunks in the 'working_memory' memory store (simulate decay over time)
print("\nApplying decay to all memory chunks...")
decay_all_memory_chunks(memories, 'working_memory_dictionary', decay_amount=3)

# Display memory contents after decay to see the updated utilities
print("\nDetailed Memory Report after Decay:")
report_memory_contents(working_memory)

# Retrieve the sandwich side with the highest (noisy and decayed) utility
selected_side = retrieve_memory_chunk(working_memory, matches={})
print("\nSelected sandwich side (after noise addition and decay):")
print(selected_side)
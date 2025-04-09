from CMCed.chunk_noise import add_noise_to_utility
from CMCed.retrieve import retrieve_memory_chunk
from CMCed.debugging import report_memory_contents
from CMCed.decay import decay_all_memory_chunks
from CMCed.chunk_utility import utility_change

# Define a memory store for sandwich working_memory with initial utilities
working_memory = {
    'fries': {'name': 'fries', 'utility': 1, 'taste': 'salty'},
    'salad': {'name': 'salad', 'utility': 1, 'taste': 'fresh'},
    'chips': {'name': 'chips', 'utility': 10, 'taste': 'crispy'}
}

# Wrap the working_memory in a dictionary as decay_all_memory_chunks expects a collection of stores
memories = {'working_memory_dictionary': working_memory}

# Add noise to each chunk's utility to simulate variability
print("\nAdding noise to utilities...")
add_noise_to_utility(working_memory, scalar=2.0)

# Provide a detailed report of memory contents after noise addition
print("\nDetailed Memory Report after Noise Addition:")
report_memory_contents(working_memory)

# Apply decay to all memory chunks in the 'working_memory_dictionary' (simulate decay over time)
print("\nApplying decay to all memory chunks...")
decay_all_memory_chunks(memories, 'working_memory_dictionary', decay_amount=3)

# Display memory contents after decay to see the updated utilities
print("\nDetailed Memory Report after Decay:")
report_memory_contents(working_memory)

# Raise the utility of a specific chunk (e.g., 'salad') after noise and decay
print("\nRaising the utility of 'chips' by 5...") # changed salad to chips and 5 to 7
utility_change(memories, 'working_memory_dictionary', 'chips', amount=5) # changed salad to fries and amount 5 to 7

# Drop the utility of the other chunks
print("\Dropping the utility of 'fries' by 3...") 
utility_change(memories, 'working_memory_dictionary', 'fries', amount=-3)
print("\Dropping the utility of 'salad' by 4...") 
utility_change(memories, 'working_memory_dictionary', 'salad', amount=-4) 

# Display memory contents after the utility change to see the updated utilities
print("\nDetailed Memory Report after Utility Change:")
report_memory_contents(working_memory)

# Retrieve the sandwich side with the highest (noisy, decayed, and adjusted) utility
selected_side = retrieve_memory_chunk(working_memory, matches={})
print("\nSelected sandwich side (after noise, decay, and utility change):")
print(selected_side)
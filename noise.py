
from CMCed.chunk_noise import add_noise_to_utility
from CMCed.retrieve import retrieve_memory_chunk
from CMCed.debugging import report_memory_contents

# Define a memory store for sandwich sides with initial utilities
working_memory = {
    'fries': {'name': 'fries', 'utility': 10, 'taste': 'salty'},
    'salad': {'name': 'salad', 'utility': 5, 'taste': 'fresh'},
    'chips': {'name': 'chips', 'utility': 7, 'taste': 'crispy'}
}

# Add noise to each chunk's utility to simulate variability
print("\nAdding noise to utilities...")
# Adjust the scalar as needed to control noise amplitude
add_noise_to_utility(working_memory,  scalar=2.0)

# Provide a detailed report of memory contents for debugging/analysis
print("\nDetailed Memory Report after Noise Addition:")
report_memory_contents(working_memory)

# Retrieve the sandwich side with the highest (noisy) utility
selected_side = retrieve_memory_chunk(working_memory, matches={})
print("\nSelected sandwich side (after noise addition):")
print(selected_side)
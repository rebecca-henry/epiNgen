# interacting with the environment using a basic CMC approach

# this model has a basic CMC architecture
# the motor module carries out motor commands from the motor_buffer in working memory
# the visual module scans the environment and updates the visual_representation_buffer in working memory

# in this model the delay for motor actions is provided by putting the delay in the motor_buffer
# this is not realistic but without a detailed motor?environment model the delays must be provided


from CMCed.production_cycle import ProductionCycle
import copy

# -------------------------
# Initialize Memories
# -------------------------
working_memory = {
    'focusbuffer': {'state': 'bread1'},
    'motor_buffer': {'state': 'no_action'},  # Initially, no motor action is scheduled.
    'visual_representation_buffer': {
        'bread1': {'location': 'counter'},
        'cheese': {'location': 'counter'},
        'ham': {'location': 'counter'},
        'bread2': {'location': 'counter'}},
    'visual_command_buffer': {'state': 'scan'}  # Command to continuously scan the environment.
}
environment = {
    'bread1': {'location': 'counter'},
    'cheese': {'location': 'counter'},
    'ham': {'location': 'counter'},
    'bread2': {'location': 'counter'}
}
memories = {
    'working_memory': working_memory,
    'environment': environment  # Motor productions still update the actual environment.
}

# -------------------------
# Define Procedural Productions (Sandwich Steps)
# These productions match on the visual_representation_buffer directly.
# -------------------------
ProceduralProductions = []

def bread1(memories):
    # Set up motor action to move bread1 from 'counter' to 'plate'
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'bread1',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    # Update the focus for the next production.
    memories['working_memory']['focusbuffer']['state'] = 'cheese'
    print("bread1 production executed: focus updated to 'cheese'; motor action scheduled for bread1.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'bread1'},
             'visual_representation_buffer': {'bread1': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': bread1,
    'report': "bread1",
})
# -------------------------

def cheese(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'cheese',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    memories['working_memory']['focusbuffer']['state'] = 'ham'
    print("cheese production executed: focus updated to 'ham'; motor action scheduled for cheese.")

ProceduralProductions.append({
    'matches': {
        'working_memory':
            {'focusbuffer': {'state': 'cheese'},
            'visual_representation_buffer': {'bread1': {'location': 'plate'},
                                             'cheese': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'report': "cheese",
})
# -------------------------

def ham(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'ham',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    memories['working_memory']['focusbuffer']['state'] = 'bread2'
    print("ham production executed: focus updated to 'bread2'; motor action scheduled for ham.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'ham'},
        'visual_representation_buffer': {
            'cheese': {'location': 'plate'},
            'ham': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': ham,
    'report': "ham",
})
# -------------------------

def bread2(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'bread2',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    memories['working_memory']['focusbuffer']['state'] = 'done'
    print("bread2 production executed: focus updated to 'done'; motor action scheduled for bread2.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'bread2'},
        'visual_representation_buffer': {
            'ham': {'location': 'plate'},
            'bread2': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': bread2,
    'report': "bread2",
})
# -------------------------

def announce_sandwich(memories):
    print("Ham and cheese sandwich is ready!")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'done'}}
    },
    'negations': {},
    'utility': 10,
    'action': announce_sandwich,
    'report': "announce_sandwich",
})
# -------------------------



# -------------------------
# Define Motor Productions (Generic Motor)
# -------------------------
MotorProductions = []

def move_item(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    env_object = motorbuffer['env_object']
    slot = motorbuffer['slot']
    newslotvalue = motorbuffer['newslotvalue']
    delay = motorbuffer['delay']

    memories['working_memory']['motor_buffer']['state'] = 'moving'
    print(f"move_item production executed: moving {env_object} to {newslotvalue}.")
    print(f"Motor action scheduled to complete in {delay} cycles.")
    return delay

def motor_delayed_action(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    env_object = motorbuffer['env_object']
    slot = motorbuffer['slot']
    newslotvalue = motorbuffer['newslotvalue']
    # Update the environment once the delay has passed.
    memories['environment'][env_object][slot] = newslotvalue
    memories['working_memory']['motor_buffer']['state'] = 'no_action'
    print(f"motor_delayed_action executed: {env_object} moved to {newslotvalue}.")

MotorProductions.append({
    'matches': {
        'working_memory': {'motor_buffer': {'state': 'do_action'}}
    },
    'negations': {},
    'utility': 10,
    'action': move_item,
    'report': "move_item",
    'delayed_action': motor_delayed_action,
})
# -------------------------



# -------------------------
# Define Visual Productions (Vision)
# -------------------------
VisualProductions = []

def scan_environment(memories):
    # Copy the entire environment into the visual representation buffer.
    # Now the visual representation is structured the same as the environment.
    memories['working_memory']['visual_representation_buffer'] = copy.deepcopy(memories['environment'])
    print("scan_environment production executed: visual_representation_buffer updated.")
    return 2  # Delay of 1 cycle (adjust as needed).

VisualProductions.append({
    'matches': {
        'working_memory': {'visual_command_buffer': {'state': 'scan'}}
    },
    'negations': {},
    'utility': 10,
    'action': scan_environment,
    'report': "scan_environment",
})
# -------------------------



# -------------------------
# Production Systems Setup
# -------------------------
ProductionSystem1_Countdown = 1  # For procedural productions.
ProductionSystem2_Countdown = 1  # For motor productions.
ProductionSystem3_Countdown = 1  # For visual productions (vision system).

DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown,
    'ProductionSystem3': ProductionSystem3_Countdown
}

AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown],
    'ProductionSystem3': [VisualProductions, ProductionSystem3_Countdown]
}


# -------------------------
# Initialize and Run the Production Cycle
# -------------------------
ps = ProductionCycle()
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=22, millisecpercycle=50)

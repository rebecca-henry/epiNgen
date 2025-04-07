

# GOMS Assignment

from CMCed.production_cycle import ProductionCycle
import copy

# -------------------------
# Initialize Memories
# -------------------------
working_memory = {
    'focusbuffer': {'state': 'left_shoe'},
    'motor_buffer': {'state': 'no_action'},  
    'visual_representation_buffer': {
        'left_shoe': {'location': 'floor'},
        'right_shoe': {'location': 'floor'},
        'coat': {'location': 'hook'},
        'key': {'location':'shelf', 'direction':'N/A'},
        'door_lock':{'direction':'up', 'status':'locked'},
        'door' : {'status' : 'closed'},
        'me': {'location': 'inside'}},
        
    'visual_command_buffer': {'state': 'scan'}  
}
environment = {
    'left_shoe': {'location': 'floor'},
    'right_shoe': {'location': 'floor'},
    'coat': {'location': 'hook'},
    'key': {'location': 'shelf', 'direction':'N/A'},
    'door_lock':{'direction':'up', 'status': 'locked'},
    'door':{'status':'closed'},
    'me': {'location':'inside'}
}
memories = {
    'working_memory': working_memory,
    'environment': environment  
}

# -------------------------
# Define Procedural Productions
# These productions match on the visual_representation_buffer directly.
# -------------------------
ProceduralProductions = []

def left_shoe(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'left_shoe',
        'slot': 'location',
        'newslotvalue': 'left_foot',
        'delay': 5
    })
    memories['working_memory']['focusbuffer']['state'] = 'right_shoe'
    print("left_shoe production executed: focus updated to 'right_shoe'; motor action scheduled for left_shoe.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'left_shoe'},
             'visual_representation_buffer': {'left_shoe': {'location': 'floor'}}}},
    'negations': {},
    'utility': 10,
    'action': left_shoe,
    'report': "left_shoe",
})

# -------------------------
def right_shoe(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'right_shoe',
        'slot': 'location',
        'newslotvalue': 'right_foot',
        'delay': 5
    })
    memories['working_memory']['focusbuffer']['state'] = 'coat'
    print("right_shoe production executed: focus updated to 'coat'; motor action scheduled for right_shoe.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'right_shoe'},
             'visual_representation_buffer': {'left_shoe': {'location': 'left_foot'},
                                            'right_shoe': {'location': 'floor'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': right_shoe,
    'report': "right_shoe",
})

# -------------------------
def coat(memories):
    # Set up motor action to move bread1 from 'counter' to 'plate'
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'coat',
        'slot': 'location',
        'newslotvalue': 'me',
        'delay': 6
    })
    # Update the focus for the next production.
    memories['working_memory']['focusbuffer']['state'] = 'get_key'
    print("coat production executed: focus updated to 'get_key'; motor action scheduled for coat.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'coat'},
             'visual_representation_buffer': {'left_shoe': {'location': 'left_foot'},
                                            'right_shoe': {'location': 'right_foot'},
                                            'coat' : {'location': 'hook'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': coat,
    'report': "coat",
})

# -------------------------
def get_key(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'key',
        'slot': 'location',
        'newslotvalue': 'coat_pocket',
        'delay': 2
    })
    memories['working_memory']['focusbuffer']['state'] = 'unlock_door'
    print("get_key production executed: focus updated to 'unlock_door'; motor action scheduled for get_key.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'get_key'},
             'visual_representation_buffer': {'left_shoe': {'location': 'left_foot'},
                                            'right_shoe': {'location': 'right_foot'},
                                            'coat' : {'location': 'me'},
                                            'key' : {'location': 'shelf', 'direction':'N/A'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': get_key,
    'report': "get_key",
})
# -------------------------
def unlock_door(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'door_lock',
        'slot': 'direction',
        'newslotvalue': 'sideways',
        'delay': 3
    })
    environment['door_lock']['status'] = 'unlocked'
    #working_memory['visual_representation_buffer']['door_lock']['status'] = 'unlocked'
    memories['working_memory']['focusbuffer']['state'] = 'open_door'
    print("unlock_door production executed: focus updated to 'open_door'; motor action scheduled for unlock_door.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
            'focusbuffer': {'state': 'unlock_door'},
            'visual_representation_buffer': {'left_shoe': {'location': 'left_foot'},
                                            'right_shoe': {'location': 'right_foot'},
                                            'coat' : {'location': 'me'},
                                            'key' : {'location': 'coat_pocket', 'direction':'N/A'},
                                            'door': {'status':'closed'},
                                            'door_lock': {'direction': 'up', 'status':'locked'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': unlock_door,
    'report': "unlock_door",
})
# -------------------------
def open_door(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'door',
        'slot': 'status',
        'newslotvalue': 'open',
        'delay': 2
    })
    memories['working_memory']['focusbuffer']['state'] = 'step_outside'
    print("open_door production executed: focus updated to 'step_outside'; motor action scheduled for open_door.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
            'focusbuffer': {'state': 'open_door'},
            'visual_representation_buffer': {'key': {'location':'coat_pocket', 'direction':'N/A'}, 
                                            'door_lock':{'direction':'sideways', 'status':'unlocked'}, 
                                            'door':{'status':'closed'},
                                            'coat':{'location':'me'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': open_door,
    'report': "open_door",
})
# -------------------------
def step_outside(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'me',
        'slot': 'location',
        'newslotvalue': 'outside',
        'delay': 3
    })
    memories['working_memory']['focusbuffer']['state'] = 'close_door'
    print("step_outside production executed: focus updated to 'close_door'; motor action scheduled for step_outside.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'step_outside'},
             'visual_representation_buffer': {'me':{'location' : 'inside'},
                                            'key': {'location':'coat_pocket', 'direction':'N/A'}, 
                                            'door_lock':{'direction':'sideways', 'status': 'unlocked'}, 
                                            'door':{'status':'open'},
                                            'coat':{'location':'me'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': step_outside,
    'report': "step_outside",
})
# -------------------------
def close_door(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'door',
        'slot': 'status',
        'newslotvalue': 'closed',
        'delay': 2
    })
    memories['working_memory']['focusbuffer']['state'] = 'put_key_in_door'
    print("close_door production executed: focus updated to 'put_key_in_door'; motor action scheduled for close_door.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'close_door'},
             'visual_representation_buffer': {'key': {'location':'coat_pocket', 'direction':'N/A'}, 
                                            'door_lock':{'direction':'sideways', 'status':'unlocked'}, 
                                            'door':{'status':'open'},
                                            'coat':{'location':'me'},
                                            'me' : {'location':'outside'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': close_door,
    'report': "close_door",
})
# -------------------------
def put_key_in_door(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'key',
        'slot': 'location',
        'newslotvalue': 'door_lock',
        'delay': 2
    })
    environment['key']['direction'] = 'sideways'
    memories['working_memory']['focusbuffer']['state'] = 'lock_door'
    print("put_key_in_door production executed: focus updated to 'lock_door'; motor action scheduled for put_key_in_door.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'put_key_in_door'},
             'visual_representation_buffer': {'key': {'location':'coat_pocket', 'direction':'N/A'}, 
                                            'door_lock':{'direction':'sideways', 'status':'unlocked'}, 
                                            'door':{'status':'closed'},
                                            'me': {'location':'outside'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': put_key_in_door,
    'report': "put_key_in_door",
})
# -------------------------
def lock_door(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'key',
        'slot': 'direction',
        'newslotvalue': 'up',
        'delay': 1
    })
    environment['door_lock']['direction'] = 'up'
    environment['door_lock']['status'] = 'locked'
    memories['working_memory']['focusbuffer']['state'] = 'take_key_from_door'
    print("lock_door production executed: focus updated to 'take_key_from_door'; motor action scheduled for lock_door.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
            'focusbuffer': {'state': 'lock_door'},
            'visual_representation_buffer': {'key': {'location':'door_lock', 'direction': 'sideways'}, 
                                            'door_lock':{'direction':'sideways', 'status' : 'unlocked'}, 
                                            'door':{'status':'closed'},
                                            'me':{'location':'outside'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': lock_door,
    'report': "lock_door",
})
# -------------------------
def take_key_from_door(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'key',
        'slot': 'location',
        'newslotvalue': 'coat_pocket',
        'delay': 2
    })
    environment['key']['direction'] = 'N/A'
    memories['working_memory']['focusbuffer']['state'] = 'leave'
    print("take_key_from_door production executed: focus updated to 'leave'; motor action scheduled for take_key_from_door.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
            'focusbuffer': {'state': 'take_key_from_door'},
            'visual_representation_buffer': {'key': {'location':'door_lock', 'direction': 'up'}, 
                                            'door_lock':{'direction':'up', 'status' : 'locked'}, 
                                            'door':{'status':'closed'},
                                            'me':{'location':'outside'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': take_key_from_door,
    'report': "take_key_from_door",
})
# -------------------------
def leave(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'me',
        'slot': 'location',
        'newslotvalue': 'away_from_house',
        'delay': 1
    })
    memories['working_memory']['focusbuffer']['state'] = 'done'
    print("leave production executed: focus updated to 'done'; motor action scheduled for leave.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
            'focusbuffer': {'state': 'leave'},
            'visual_representation_buffer': {'key': {'location':'coat_pocket', 'direction': 'N/A'}, 
                                            'door_lock':{'direction':'up', 'status' : 'locked'}, 
                                            'door':{'status':'closed'},
                                            'me':{'location':'outside'}
                                            }}},
    'negations': {},
    'utility': 10,
    'action': leave,
    'report': "leave",
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=59, millisecpercycle=2000)
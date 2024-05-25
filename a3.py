from importlib import invalidate_caches
from importlib import import_module



def write_py(name: str, parameters: list[str], statements: list[str]):
    assert name != 'a3'

    filename = f'{name}.py'
    with open(filename, 'w+') as pyFile:
        code_lines = []
        # Create one function with 'name'
        params_list = ', '.join(parameters)
        function_def = f'def {name}({params_list}):\n'

        # Adding function_def to the code
        code_lines.append(function_def)

        # Adding function body
        for statement in statements:
            line = f'\t{statement}\n'
            code_lines.append(line)

        # Writing to the file
        pyFile.writelines(code_lines)


def load_function(name):
    '''
    load_function - imports a module recently created by name
        and returns the function of the same name from inside of it
    name - a string name of the module (not including .py at the end)
    '''
    # invalidate_caches is necessary to import any files created after this file started!
    invalidate_caches()
    print(f"    Attempting to import {name}...")
    module = import_module(name)
    print(f"    Imported!")
    assert hasattr(module, name), f"{name} is missing from {name}.py"
    function = getattr(module, name)
    assert type(function) is type(load_function)
    return function


def fixed_bubble(size: int):
    # Constants
    var_name = 'a_list'

    # Variables
    func_name = f'bubble{size}'
    parameters = [ var_name ]
    instructions = [ ]


    for i in range(size - 1):
        # Inserting the comment
        instructions.append(f'# Bubble {i}')
        for j in range(size - i - 1):
            # Inserting the if conditions
            instructions.append(f'if {var_name}[{j}] > {var_name}[{j + 1}]:')
            # Inserting the body of the if condition
            instructions.append(f'\t{var_name}[{j}], {var_name}[{j + 1}] = {var_name}[{j + 1}], {var_name}[{j}]')

    # Return statement
    instructions.append(f'return {var_name}')


    # Calling the write_py function
    write_py(func_name, parameters, instructions)


def flip(direction):
    if direction == '>':
        return '<'
    return '>'


def greatest_power_of_two_less_than(x):
    if x == 0:
        return 0
    num = 1
    while 2 * num < x:
        num *= 2
    return num


def bitonic(a_list):
    r_sort(a_list, 0, len(a_list), '>')

# Follows the algorithm described in the document
def r_merge(a_list: list[int], start: int, end: int, direction: str):
    # print('merge', start, end, direction)
    if start + 1 == end:
        return

    distance = greatest_power_of_two_less_than(end - start)
    middle = end - distance


    for index in range(start, middle):
        if direction == '>':
            if a_list[index] > a_list[index + distance]:
                a_list[index] , a_list[index + distance] = a_list[index + distance], a_list[index]

        elif direction == '<':
            if a_list[index] < a_list[index + distance]:
                a_list[index] , a_list[index + distance] = a_list[index + distance], a_list[index]

    r_merge(a_list, start, middle, direction)
    r_merge(a_list, middle, end, direction)


# Follows the algorithm described in the document
def r_sort(a_list: list[int], start: int, end: int, direction: str):
    # print('sort', start, end, direction)
    if start + 1 == end:
        return
    middle = int((end - start) // 2) + start
    r_sort(a_list, start, middle, direction)
    r_sort(a_list, middle, end, flip(direction))
    r_merge(a_list, start, end, direction)


# Follows the algorithm described in the document
# Slightly modified to match our use case for fixed_bitonic and write_py
def fixed_merge(instructions: list[str], var_name: str, start: int, end: int, direction: str):
    if start + 1 == end:
        return

    distance = greatest_power_of_two_less_than(end - start)
    middle = end - distance

    for index in range(start, middle):
        # Inserting the if conditions
        instructions.append(f'if {var_name}[{index}] {direction} {var_name}[{index + distance}]:')
        # Inserting the body of the if condition
        instructions.append(f'\t{var_name}[{index}], {var_name}[{index + distance}] = {var_name}[{index + distance}], {var_name}[{index}]')

    fixed_merge(instructions, var_name, start, middle, direction)
    fixed_merge(instructions, var_name, middle, end, direction)


# Follows the algorithm described in the document
# Slightly modified to match our use case for fixed_bitonic and write_py
def fixed_sort(instructions: list[str], var_name: str, start: int, end: int, direction: str='>'):
    if start + 1 == end:
        return
    middle = int((end - start) // 2) + start
    fixed_sort(instructions, var_name, start, middle, direction)
    fixed_sort(instructions, var_name, middle, end, flip(direction))
    fixed_merge(instructions, var_name, start, end, direction)


def fixed_bitonic(size: int):
    # Constants
    var_name = 'a_list'

    # Variables
    func_name = f'bitonic{size}'
    parameters = [ var_name ]
    instructions = [ ]

    # ============================ Bitonic sort logic ==========================
    # Calling the previous defined functions
    # This will call the recursive functions for the bitonic sort 
    # And insert the the generated if conditions + body to the instructions list
    fixed_sort(instructions, var_name, 0, size)

    # Return statement
    instructions.append(f'return {var_name}')
    # =========================================================================

    # Calling the write_py function
    write_py(func_name, parameters, instructions)



def main():

    # Testing write_py
    write_py("power", ["X", "n"], ["res = X ** n", "return res"])
    power = load_function("power")
    assert power(4, 2) == 16
    print('Power function works!')


    # Testing fixed_bubble
    fixed_bubble(4)
    bubble4 = load_function("bubble4")
    assert bubble4([3, 4, -6, 0]) == sorted([3, 4, -6, 0])
    print('Sorting using bubble4 works!')

    # Testing greatest_power_of_two_less_than
    assert greatest_power_of_two_less_than(3) == 2 # 2^1
    assert greatest_power_of_two_less_than(5) == 4 # 2^2
    assert greatest_power_of_two_less_than(100) == 64 # 2^6
    assert greatest_power_of_two_less_than(32) == 16 # 2^4

    # Testing flip
    assert flip('>') == '<'
    assert flip('<') == '>'
    
    # Testing bitonic
    l = [39, 0, 8, 2, 99]
    print(f"Sorting: {l}")
    bitonic(l)
    print(f"Result: {l}")

    # Testing bitonic
    fixed_bitonic(6)
    bitonic6 = load_function("bitonic6")
    assert bitonic6([109, 39, 0, 8, 2, 99]) == sorted([109, 39, 0, 8, 2, 99])
    print('Sorting using bitonic6 works!')




if __name__ == '__main__':
    main()

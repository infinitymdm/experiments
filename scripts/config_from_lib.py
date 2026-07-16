from liberty.parser import parse_liberty
from pathlib import Path

def strip_quotes(x):
    return str(x).strip('"')

def check_and_add(d, group, key, alt_key=None, edge=False):
    attr = group.get(key)
    if attr:
        attr = strip_quotes(attr)
        key = key if not alt_key else alt_key
        if edge:
            if attr.startswith('!'):
                attr = attr.replace('!', 'negedge ')
            else:
                attr = f'posedge {attr}'
        else:
            if attr.startswith('!'):
                attr = attr.replace('!', 'not ')
        d[key] = attr

def read_cells_and_functions(libfile):
    cells = {}
    with open(libfile, 'r') as file:
        library = parse_liberty(file.read())
        for cell_group in library.get_groups('cell'):
            cell_name = cell_group.args[0]

            # Parse output functions
            functions = []
            for pin_group in cell_group.get_groups('pin'):
                pin_name = pin_group.args[0]
                direction = pin_group.get('direction')
                function = pin_group.get('function')
                if direction == 'output' and function:
                    functions.append(f'{strip_quotes(pin_name)} = {strip_quotes(function)}')

            # If cell is a flop or latch, add state and modify functions
            attrs = {}
            for ff_group in cell_group.get_groups('ff'):
                check_and_add(attrs, ff_group, 'clocked_on', alt_key='clock', edge=True)
                check_and_add(attrs, ff_group, 'clear', alt_key='reset')
                check_and_add(attrs, ff_group, 'preset', alt_key='set')
                next_state = ff_group.get('next_state')
                if next_state:
                    attrs['state'] = []
                    attrs['state'].append(f'{strip_quotes(ff_group.args[0])} = {strip_quotes(next_state)}')
                    attrs['state'].append(f'{strip_quotes(ff_group.args[1])} = !({strip_quotes(next_state)})')
            for latch_group in cell_group.get_groups('latch'):
                check_and_add(attrs, latch_group, 'clear', alt_key='reset')
                check_and_add(attrs, latch_group, 'preset', alt_key='set')
                check_and_add(attrs, latch_group, 'enable')
                next_state = latch_group.get('data_in')
                if next_state:
                    attrs['state'] = []
                    attrs['state'].append(f'{strip_quotes(ff_group.args[0])} = {strip_quotes(next_state)}')
                    attrs['state'].append(f'{strip_quotes(ff_group.args[1])} = !({strip_quotes(next_state)})')

            if functions:
                attrs['functions'] = functions
                cells[strip_quotes(cell_name)] = attrs

    return cells

def print_as_yaml(obj, indent=0):
    IDNT = 4*' '
    if isinstance(obj, dict):
        for k in obj:
            print(f'\n{indent*IDNT}{k}:', end='')
            print_as_yaml(obj[k], indent=indent+1)
    elif isinstance(obj, list):
        if len(obj) > 1:
            for i in obj:
                print(f'\n{indent*IDNT}- {i}', end='')
        else:
            print(f' [{obj[0]}]', end='')
    else:
        print(f' {str(obj)}', end='')

if __name__ == '__main__':
    lib_path = Path('/home/marcus/.ciel/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib')
    # lib_path = Path('/home/marcus/.ciel/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu9t5v0/lib/gf180mcu_fd_sc_mcu9t5v0__tt_025C_3v30.lib')
    # lib_path = Path('/home/marcus/.ciel/ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib')
    config = read_cells_and_functions(lib_path)
    print_as_yaml(config)

from charlib.characterizer.characterizer import Characterizer
from charlib.cli import utils

from tqdm import tqdm

import memray

from pathlib import Path
import concurrent.futures
import random
import string
import os

def simulation_task_wrapper(task, *args):
    task_id = ''.join(random.choices(string.ascii_letters, k=8))
    with memray.Tracker(f'tmp/memray-task-{task.__name__}-{task_id}.bin'):
        result = task(*args)
    return result

def run(config_file):
    config = utils.find_config(config_file)

    characterizer = Characterizer(**config['settings'])
    for name, config in utils.read_cell_configs(config['cells']):
        try:
            characterizer.add_cell(name, config)
        except ValueError as e:
            print(e)
            continue

    # Custom characterize routine - characterize one cell at a time
    for cell, config in characterizer.cells:
        tasks = characterizer.analyse_cell(cell, config)
        with tqdm(bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]', total=len(tasks), desc=cell.name) as progress_bar:
            with concurrent.futures.ProcessPoolExecutor(max_workers=characterizer.settings.jobs) as executor:
                futures = [executor.submit(simulation_task_wrapper, task, *args) for (task, *args) in tasks]
                for completed in concurrent.futures.as_completed(futures):
                    characterizer.library.add_group(completed.result())
                    progress_bar.update(1)

    # Add LUTs
    for timing_group in characterizer.library.subgroups_with_name('timing'):
        for lut_group in timing_group.groups.values():
            characterizer.library.add_group(lut_group.template)

    print(characterizer.library.to_liberty(precision=6))

if __name__ == "__main__":
    run('sky130_fd_sc_hd__tt_025C_1v80.yaml')

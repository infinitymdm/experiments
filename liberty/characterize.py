from charlib.characterizer.characterizer import Characterizer
from charlib.cli import utils
from tqdm import tqdm
from pathlib import Path
import concurrent.futures
import os
import pickle

def run(config_file):
    workfiles = []
    config = utils.find_config(config_file)

    # Characterize cells one at a time, writing results to file for later merge
    for name, cell_config in utils.read_cell_configs(config['cells']):

        # Build characterizer and load the cell
        characterizer = Characterizer(**config['settings'])
        try:
            characterizer.add_cell(name, cell_config)
        except ValueError as e:
            print(e)
            continue

        # If we already have results for this cell, skip
        workfile = characterizer.settings.results_dir / 'work' / f'{name}.lib.pkl'
        if workfile.exists():
            print(f'Skipping previously characterized cell "{name}"')
            workfiles.append(workfile)
            continue

        # Run characterization
        print(f'Running cell "{name}"')
        characterizer.characterize()

        # Write results to file
        workfile.parent.mkdir(parents=True, exist_ok=True)
        with open(workfile, 'wb') as file:
            pickle.dump(characterizer.library, file)
        workfiles.append(workfile)

    # Compile results into the final library
    library = None
    for workfile in workfiles:
        with open(workfile, 'rb') as file:
            liberty = pickle.load(file)

            # Merge the new liberty into the library
            if library is None:
                library = liberty
            else:
                library += liberty
    if library is not None:
        libfile = characterizer.settings.results_dir / characterizer.library.file_name # intentionally leak from loop
        libfile.parent.mkdir(parents=True, exist_ok=True)
        with open(libfile, 'w') as file:
            file.write(str(library.to_liberty(precision=6)))

if __name__ == "__main__":
    possible_configs = utils.find_yaml_files(Path(__file__).resolve().parent)
    [print(i, v) for i, v in enumerate(possible_configs)]
    config = possible_configs[int(input('Select config to run: '))]
    os.chdir(config.parent)
    run(config.name)

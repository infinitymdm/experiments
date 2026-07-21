## CharLib Experiments

1. Create and activate a virtual environment: `python -m venv .venv; source .venv/bin/activate`
2. Install dependencies: `pip install git+https://github.com/stineje/CharLib.git siliconcompiler ciel`
3. Activate PDKs
    ```
    ciel enable --pdk-family gf180mcu f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7
    ciel enable --pdk-family sky130 f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7
    ciel enable --pdk-family ihp-sg13g2 ee974c3adc69d0f36adbf20577079f0df419d702
    ```
4. Characterize PDKs
5. Generate SPEF
6. Compare results

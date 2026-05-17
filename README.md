[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/CjRQqtHi)

## gather_data.py

How it works:

1. Run the code
2. Input your name in terminal
3. Input activity in terminal
4. Press Button 1 to start recording
5. Recording will last 10 seconds
6. Press Button 1 to start recording again - 5 recodings are possible
7. Each recording is resampled to 100Hz and saved as a CVS file


## training data 
- located in data
- one folder for each activity ("jumpingjacks", "running", "rowing", "lifting")
- if you have multiple folders with log data, get data in there via:
    - cd data
    - cp path/to/logs/folder/*/*row*.csv ./rowing/
    - cp path/to/logs/folder/*/*jump*.csv ./jumpingjacks/
    - cp path/to/logs/folder/*/*lift*.csv ./lifting/
    - cp path/to/logs/folder/*/*run*.csv ./running/

## How to use the fitness trainer
- make a venv and install all dependencies from the requirements.txt
- start the DIPPID app on your phone.
    - Make sure Port 5700 and your PCs IP are set correctly
    - Also check if both devices are in the same network and that network allows communication between the two
- start fitness_trainer.py in your venv
- follow the instructions in the displayed app
- app can be closed with clicking the x or pressing q on the keyboard


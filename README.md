## Installing

#### Clone Repository
`git clone https://gitlab2.informatik.uni-wuerzburg.de/chr58bk/mptv.git`

#### Setup and Activate Virtual Enviroment
`python -m pip install --user virtualenv`

`python -m virtualenv path/to/venv`

`source path/to/venv/bin/activate`

#### Install Requirements and Run MPTV Setup
`pip install -r requirements.txt`

`python setup.py install`


## Usage

### mptv-setup_folds
Input: image list (\*.png, \*.bin.png, \*.nrm.png, + corresponding GT (\*.gt.txt))  
Output: folder (--output, default: ./Data) with n (--folds, default = 5) sub folders which contain #lines/n lines  

The folder id gets placed in front of the line name in order to prevent overwriting of lines with the same name.

### mptv-run_multi_train
Input: folder containing the "Folds" sub folder.  
Output: "Models" folder which containes the trained models for each fold.

--models: "LH,LH,FRK,ENG,ENG" means that the first two folds starts training from LH fold 3 from ENG, and fold 4 and 5 from FRK with LH, ENG, 

and FRK being different mixed models from the pretraining folder.
"LH,,,,LH" starts the training of fold 1 and 5 from LH and trains the rest from scratch.

### mptv-find_best_model
Input: folder containing "Folds" and "Models" sub folders.  
Output: the best model of each fold stored in "Models/BestModels".

### mptv-recognize_lines
Input: folder(s) containing the to-be-predicted lines.  
Output: folder "Voting" in each input folder which contains the results (\*.txt and \*.extLlocs) for each fold.

### mptv-conf_vote  
Input: "Voting" folder(s) resulting from the preceding step.  
Output: "Voting/Voted" folders containing voted \*.txts.
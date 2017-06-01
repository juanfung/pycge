TODO list

- Add milestones (with dates) to TODO
     - v0.1: working module that replicates demo
     - v0.2.0: module with results export and output display
     - v0.2.5: module with unit test
     - v0.3.0: module with flexible data import (ideally, `pandas`)
     - v0.3.5: add unit tests
     - v0.4: 

- `src/splcge_module.py` (based on `splcge.gms`)
     - ~~port splcge_demo.py to module~~
     - unit test [module == demo]
          - depends on results export
     - read Section 18, pyomo documentation
          - preprocessing
          - postprocessing
          - other pyomo callbacks
          - relationship between `model` of type `AbstractModel` and 
            `instance` generated from `model`, given some data  
                 - why are results accessible from `model`?
     - implement results export: should be able to load results back into
       python (e.g., through `pandas`)
          - decide on export format (e.g., row names, col names, separate files, etc.)
          - test in demo
          - implement in module
     - implement pretty output: displaying instance and results, other informative
       messages
          - test in demo
          - implement in module
     - is it worth saving solved instance? 
          - if so, how?
     - implement data import via
          - `pyomo.DataPortal` 
          - `pandas`
     - implement external function import
          - goal is to have `AbstractModel` definition (i.e., defining constraints,
            variables, etc.) in a separate `.py` file to be imported into module
     - updating model 
          - new data, *given model*
          - changing parameter values or definitions
          - adding/removing parameters
          - changing variables and constraints (adding, removing, modifying)

- Extending the module
     - extend module to include `splcge.gms` and `stdcge.gms`
     - once code is broken up into multiple files, module -> package

- Documentation
     - initialize `doc/` directory in main project directory
     - initialize documentation (in markdown or rst?)
     - documentation is **for user**, should guide user through model
       model creation and model solution

- From module to package
     - reorganize project directory
     - see [python-packaging.readthedocs.io/en/latest/evertyhing.html](python-packaging.readthedocs.io/en/latest/evertyhing.html)

- SURF requirements
     - Symposium Abstract (Due July 11)
          - Send Juan abstract requirements
          - Meeting re abstract (June 27)
     - SURF Symposium (August 1-3)
          - Send Juan symposium requirements
          - Meeting re symposium (July 18, July 25)


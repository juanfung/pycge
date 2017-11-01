TODO list

As of October 4, 2017, package repository will be *hosted* on Github and *mirrored* on the
(private) Gitlab NIST server. Github issues will supercede this TODO list.

- Create RELEASE_NOTES file to document v0.1+ releases and major changes

- Pre-development and development version milestones 
     - ~~v0.0.1: working module that replicates demo~~
     - ~~v0.0.2: module with results export and output display~~
     - ~~v0.0.2.5: module with unit test~~
     - ~~v0.0.3: module with flexible data import (ideally, `pandas`)~~
        - using `pandas` straightforward with `ConcreteModel`
        - Not obviously necessary or advantageous to use `pandas` over `DataPortal`
     - ~~v0.0.4: module `PyCGE` that acts on an object of class `ModelDef`, where `ModelDef`
      is simply the model definition~~
     - v0.0.5: add `model_welfare()` method to `PyCGE`
     - v0.1: distribute as package with `disutils` 
     - v0.1.5: add unit tests to test `PyCGE` methods (use demos to benchmark?)
     - v0.2: 
            - error handling for `ConcreteModel` objects
            - example scripts should find data files before loading into `model_data`,
              conditional on package install (ie, check `../data`, `site-packages`, etc)

- Porting `splcge.gms` to `src/splcge_module.py`
     - ~~port splcge_demo.py to module~~
     - ~~unit test [module == demo]~~
          - depends on results export
     - ~~read Section 18, pyomo documentation~~
          - preprocessing
          - postprocessing
          - other pyomo callbacks
          - ~~relationship between `model` of type `AbstractModel` and 
            `instance` generated from `model`, given some data~~ 
                 - why are results accessible from `model`?
     - ~~implement results export: should be able to load results back into
       python (e.g., through `pandas`)~~
          - decide on export format (e.g., row names, col names, separate files, etc.)
               - for now, separate files for each variable
          - test in demo
          - implement in module
     - ~~implement pretty output: displaying instance and results, other informative
       messages~~
          - display output -> log file
          - test in demo
          - implement in module
     - ~~is it worth saving solved instance?~~
          - if so, how?
               - not sure solving model or instance is possible, but setting up a 
                 model is computationally cheap relative to solving
               - saving `results` object **is possible
                    - what do `instance.solutions.store()` and `instance.solutions.load_from()`
                      do?
                    - best option may be to `pickle` (serialize and deserialize) 
                      `results` object
               - see [this discussion](https://groups.google.com/d/msg/pyomo-forum/I6yuGnGl13c/lbr44a5HDAAJ)
     - ~~implement data import via~~
          - ~~`pyomo.DataPortal`~~
             - **THIS WORKS WELL BUT CAUSES PROBLEMS FOR SOME SOLVERS ON NEOS**
          - ~~`pandas`~~
             - **SEE COMMENT ABOVE; DOES NOT WORK WITH `AbstractModel` AND POSSIBLY UNNECESSARY**
     - ~~implement external function import~~
          - **THIS WAS ABANDONNED IN FAVOR OF SEPARATING MODEL DEFINITION INTO ITS OWN
          CLASS, `ModelDef`**
          - goal is to have `AbstractModel` definition (i.e., defining constraints,
            variables, etc.) in a separate `.py` file to be imported into module
     - ~~updating model~~
          - new data, *given model*
          - changing parameter values or definitions
          - adding/removing parameters
          - changing variables and constraints (adding, removing, modifying)
     - **ERROR HANDLING**
          - ~~need to catch errors and provide useful messages to user~~
          - ~~Try/Except in python~~
          - ~~saving results, etc: depends on having a solution!~~
               - ~~use If/Else, depending on `SolverStatus`~~

- ~~Extending the module~~
     - ~~extend module to include `splcge.gms` and `stdcge.gms`~~
         - **THIS IS IMPLENTED BY PASSING AN OBJECT OF CLASS `ModelDef` TO AN OBJECT
         OF CLASS `PyCGE` THAT *ACTS* ON A MODEL DEFINED BY `ModelDef`**
     - ~~once code is broken up into multiple files, module -> package~~
         - **FOR NOW, FORGET PACKAGING**
     - `splcge` and `stdcge` model definitions: one `ModelDef` file or separate?
         - **DEFINE EACH `*ModelDef` CLASS IN SEPARATE FILES**
     - port Cedar Rapids GAMS code to a `ModelDef` class

- Documentation
     - ~~initialize `doc/` directory in main project directory~~
     - ~~initialize documentation (in markdown or rst?)~~
     - ~~documentation is **for user**, should guide user through model~~
     - ~~model creation and model solution~~
     - Add installation instructions
     - Add instructions for importing examples *and example data*, eg, `from pycge.examples import *`
     - Host documentation on readthedocs

- ~~From module to package~~
     - reorganize project directory
     - see [python-packaging.readthedocs.io/en/latest/evertyhing.html](python-packaging.readthedocs.io/en/latest/evertyhing.html)


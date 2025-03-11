# Linear-supports
Calculating stresses in steel sections using sectionproperties, and check compliance with design code RCC-M Z VI.
Main steel sections library included (french / european steel sections).

Criterias similar to AISC Allowable Stress Design 9th / ASME III NF (without single angle appendix).
Stress limit for U sections in bending may be lower than the criteria.

Program is provided without responsabilities on results.
Some checks were done using available results from RSTAB + ASD.

# Installation and use 
Download a copy of this repo, and run "launcher.py" with Python.
Make sure that folders with steel section tables and images are located next to the launcher file, as in this repo.

Dependancies needed are the following :
- [sectionproperties](https://github.com/robbievanleeuwen/section-properties)
- [rich](https://github.com/Textualize/rich)
- [FreeSimpleGUI](https://github.com/spyoungtech/FreeSimpleGui)

All dependancies available on PyPI, with pip

# Documentation
See Wiki for more details

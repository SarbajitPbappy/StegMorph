# DDE Lab feature extractors (not redistributed)
V2.1 uses the SRM and maxSRM extractors of the DDE Lab, Binghamton University (research and non-profit use only, licence in the file headers). They are not included here. Download `SRM_linux_make_v1.1.tar` and `maxSRM_linux_make_v1.1.zip` from https://dde.binghamton.edu/download/feature_extractors/ , then in each `SRM_src` folder run
`mkoctfile --mex -O2 -I../include -o SRM SRM_matlab.cpp SRMclass.cpp submodel.cpp s.cpp image.cpp exception.cpp config.cpp` (and `-o maxSRM` for maxSRM) and copy the two `.mex` files into `tools/dde/bin/`.
`feat.m` is our batch wrapper around them.

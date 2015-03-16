Dejavu
======

Dejavu is a demo application for the [Cight](https://github.com/xperroni/Cight) visual navigation library, sharing its dependencies.

Building
--------

Open a command prompt, move into either folder `build/release/` or `build/debug/` (depending on which build mode you want to use) and enter the following commands:

    $ cmake -DCMAKE_BUILD_TYPE=$MODE ../..
    $ make -j2

Where `$MODE` should be either `Release` or `Debug`.

Alternatively, under Bash-compatible environments you can just call the `build.sh` script:

    $ ./build.sh

The build scripts expect to find the source files for [Cight](https://github.com/xperroni/Cight) and [Clarus](https://github.com/xperroni/Clarus) on a folder at the same level as the project's base folder, for example:

    .
    |
    +--+ Cight
    |  |
    |  +-- build
    |  +-- include
    |  +-- src
    |
    +-- Clarus
    |  |
    |  +-- build
    |  +-- include
    |  +-- src
    |
    +--+ Dejavu
       |
       +-- build
       +-- src

Version History
---------------

**2015-03-16**

Apart from some experiments with new feature selectors this version brings nothing new. It was pushed just to clean the slate before I port my code base to ROS.

**2015-01-26**

A hopelessly belated and somewhat broken update, but better late than never. This version includes the new image pairing method described in [this report](https://github.com/xperroni/Yamabiko/blob/master/2014-2/Article/Image%20Stream%20Synchronization%20for%20Visual%20Navigation.pdf). In fact the actual implementation has progressed a little beyond what is reported here, and is currently in a state of flux, but it had been too long since I uploaded anything and I was growing weary of having no backup of this work. So there.

TO DO
-----

* Increment the cmake scripts with better dependency detection;
* Document source files and scripts;
* Move the code base to C++ 11, when support is widespread enough.

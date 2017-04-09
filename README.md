# Stack Usage

## Summary

The purpose of this python script is to extract information about the **stack usage** and **callgraphs** of your C/C++ program just by using the standard GCC toolchain (native or as cross-compiler).

## Limitations

Of course there are some limitations. For instance **function pointers** cannot be resolved as the compiler itself has no information about how they will be executed during runtime. Next is **recursion**. Although it can be detected at compile time in general we never know how deep the nesting is at runtime. There is another limitation which is **duplicate functions**. As all data is currently collected into one file the python script can currently not resolv whether a function comes from source code A or B. However in a good project you shall not find two different functions in multiple files having the same name. So this usually shouldn't be an issue. The last thing to mention are **libraries**. We can only assume a stack usage of zero for 3rd party functions and internal functions provided by the runtime environment as we don't know anything about code we did not compile ourselves.

# Example

## Getting the data

Compile your source files using the flags *-fstack-usage* and *-fdump-ipa-cgraph* for GCC to get the information about stack usage and callgraph.

    gcc -fstack-usage -fdump-ipa-cgraph -o example example.c

Collect the data to process this information.

    find . -name '*.cgraph' | grep -v stack-usage-log | xargs cat > stack-usage-log.cgraph
    find . -name '*.su'     | grep -v stack-usage-log | xargs cat > stack-usage-log.su

Run the script to see your stack usage.

    python stack-usage.py --csv stack-usage.csv --json stack-usage.json

## Getting the data (the lazy way)

Just use the makefile provided with this repository by running the make command. It will perform the same steps as above.

    make

## Output

The output will be a CSV file and a dictionary in JSON format. It can be used for further post-processing or directly to generate sunburst diagrams (see: [Sunburst Partition](https://bl.ocks.org/mbostock/4063423)).

stack-usage.csv

    184;foobar/16 foo/160 bar/8
    24;foobar/16 bar/8
    184;main/16 foo/160 bar/8

stack-usage.json

    {
        'callStack':'',
        'maxSize':192,
        'size':0,
        'name':'',
        'children':[
            {
                'callStack':'main/16',
                'maxSize':192,
                'size':16,
                'name':'main',
                'children':[
                    {
                        'callStack':'main/16 foo/160',
                        'maxSize':192,
                        'size':176,
                        'name':'foo',
                        'children':[
                            {
                                'callStack':'main/16 foo/160 bar/16',
                                'maxSize':192,
                                'size':192,
                                'name':'bar',
                                'children':[
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

# License

Copyright (C) 2017 Enrico May

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
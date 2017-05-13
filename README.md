![Travis-CI status](https://travis-ci.org/goosechooser/file-manip-toolkit.svg?branch=master "Travis-CI status")
## what it is
* a collection of possibly helpful scripts to make certain low level file manipulations easier

## other info
* tested to work on python 3.6, confirmed to not work on python 2.7

## how to install
* download the repo then `pip install path/to/archive`    
or  
* `pip install git+git://github.com/goosechooser/[REPONAME].git@[BRANCHNAME]`  
(you may need to use sudo)

## features
* automatically recognizes whether to interleave or deinterleave based on number of input files
* can interleave an arbitrary amount of files together by an arbitrary number of bytes (this entire claim is untested)
* can deinterleave a file into an arbitrary amount of files together by an arbitrary number of bytes (this entire claim is untested)
* swap endianess every 2, 4, 8, ??? bytes

## usage - deinterleaving
* saving to current working directory with default file name  
`unfman FILE NBYTES NOUTPUTS -v`

* saving to a different directory with custom file name  
`unfman FILE NBYTES NOUTPUTS -o testdir\howdy.pardner -v`

* saving to a different directory with default file name  
`unfman FILE NBYTES NOUTPUTS -o testdir\ -v` 

## usage - interleaving
* saving to current working directory with default file name  
`unfman FILE1 FILE2 .. FILEN NBYTES -v`

* saving to a different directory with custom file name  
`unfman FILE1 FILE2 .. FILEN NBYTES -o testdir\yeehaw -v`

* saving to a different directory with default file name  
`unfman FILE1 FILE2 .. FILEN NBYTES -o testdir\ -v`

## usage - (de)interleaving cps2 graphics format
* -o and -v flags still work, not shown for brevity  
`unfman FILE NBYTES cps2`  
`unfman FILE1 FILE2 .. FILE4 cps2`


## usage - endianess swapping
* saving to current working directory with default file name  
`eswap FILE FMT -v`

* saving to a different directory with custom file name  
`eswap FILE FMT -o testdir\howdy.pardner -v`

* saving to a different directory with default file name  
`eswap FILE FMT -o testdir\ -v` 

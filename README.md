# XCTU-pkgsample

## Create an XCTU sample file

## IMPORTANT KEY

`projectName` name of the project : String
`outputNum` data sample size : int
`outputName` name of the output file : String
`data` : list of dictionary; contain different data type

## type of value which can be use

** PKG **

> running up number from 0 - your package number

** time **

> time - time in format hh:mm:ss

** [0,100] ** list of int or float (choose either not both)
only use the first two index of list

> range of random can only be in int or float format
> if you want to random float start with int use 0.0
> note: if the key of this value begins with GPS the float will convert to 7 decimal point
> ** ["A","B"] **
> choose item randomly in list
> use all value of list with the method of random.choice

** String **

> a constant value in the xml file e.g. teamID or package type

** simple condition **

> a simple condition which will act as an easy if-else
> `start` start value
> `condition` comparision operater e.g. < > <= >= == !=
> `action` action in which the condition is true
> `else` action in which the condition is false
> example value

```
{
"start":0,
"condition":"<1000",
"action":"+10",
"else":0
}
```

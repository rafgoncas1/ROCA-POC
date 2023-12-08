# ROCA-POC

This repository contains a CLI application of the ROCA attack, which can serve as cryptographic educational content.

The implementation of the attack was provided by Florian Picca and forked from [this repository](https://github.com/FlorianPicca/ROCA).

It's a Sage implementation that uses multiprocessing.

For more information about the implementation you can read [Florian's blog](https://bitsdeep.com/posts/analysis-of-the-roca-vulnerability/).

## What can we do with this app?

- Factorize modulus providing it directly.
- Factorize modulus from a file containing the modulus in a single line.
- Select diferent formats for the modulus: hex, decimal or base64.
- Generate weak modulus for testing, providing a number of primes "nprimes".


## Tests directory

This repository also contains a Tests directory where I have added some data for live testing.
The modulus in the data subdirectory may not be weak to the ROCA attack, only some of them contains the fingerprint.
To test the fingerprint I recommend using the roca-detect tool from [this repository](https://github.com/crocs-muni/roca) which can be easily pip installed.

```
pip install roca-detect
```
### Fingerprinted modulus

The modulus which are weak to the ROCA attack are the following:

- mod01.txt
- mod02.txt
- mod03.txt
- mod08.txt
- mod09.txt

Keep in mind these modulus have an hexadecimal format.

## Usage

### Help
Shows the help.
```
$ sage roca_attack.py -h
```
```
$ sage roca_attack.py --help
```
#### Output:
```
usage: roca_attack.py [-h] [-n N] [-f FILE] [--format {decimal,hex,base64}] [-g NPRIMES]

ROCA attack

options:
  -h, --help            show this help message and exit
  -n N, --modulus N     RSA modulus
  -f FILE, --file FILE  File containing the modulus in one line
  --format {decimal,hex,base64}
                        Format of the modulus (default: decimal)
  -g NPRIMES, --generate NPRIMES
                        Generate a weak modulus with n primes
```

### Generate
Generates a weak and fast factorizable modulus using NPRIMES.
```
$ sage roca_attack.py -g 39
```
```
$ sage roca_attack.py --generate 5
```
#### Output:
```
--- Generating key with [ 39 ] primes ---

# parameters:
k= 10 , a= 1

*** Key generated successfully! ***

N= 55636064106125042879014886654861104533143120611798750993759489833787978005495697671641810297410743834581133499179603089552791639462097

p= 5777684524415903562341677295406806575178514783655726322495167407781
q= 9629474207359839270569462159011344291964191306062130754159634978237

Information: Key is weak to ROCA attack
```

### Factorize
Factorize a modulus either providing it directly or from a file containing it in a single line, both can be in any format that this application supports.

In order to provide it directly, the -n or --modulus argument must be specified.
```
$ sage roca_attack.py -n 55636064106125042879014886654861104533143120611798750993759489833787978005495697671641810297410743834581133499179603089552791639462097
```
```
$ sage roca_attack.py --modulus 55636064106125042879014886654861104533143120611798750993759489833787978005495697671641810297410743834581133499179603089552791639462097
```
This modulus is in decimal format so the --format argument does not need to be specified.
But we can specify it this way.
```
$ sage roca_attack.py -n 13987879C5C5D20AF8D06A71A3E889CC8631959DB493B303FB5C02E863168F20F74FCB0E762A52A8DECE8499AD66027B757F94CCABBC90D1 --format hex
```
```
$ sage roca_attack.py -n NTU2MzYwNjQxMDYxMjUwNDI4NzkwMTQ4ODY2NTQ4NjExMDQ1MzMxNDMxMjA2MTE3OTg3NTA5OTM3NTk0ODk4MzM3ODc5NzgwMDU0OTU2OTc2NzE2NDE4MTAyOTc0MTA3NDM4MzQ1ODExMzM0OTkxNzk2MDMwODk1NTI3OTE2Mzk0NjIwOTc= --format base64
```
Reading modulus from a file containing it in a single line.
```
$ sage roca_attack.py -f path/to/file
```
```
$ sage roca_attack.py --file path/to/file
```
Finally, testing with the data provided in the tests/data folder.
```
sage roca_attack.py -f tests/data/mod01.txt --format hex
```
#### Output
```
--- Starting ROCA attack ---

Modulus:
N= 7767362024477185202421071250449328253951731768019490336151878552855168339808584137842228634592686806733490580212022012129148164150665235025414779529297831

*** SUCCESS: Factorization found ***
p=87616230635132712511069342847114754662128842683356224376963228413943832744221
q=88652090693372019893601608946467234323869171766861807964374450403698775563411
```
--------------------------------------------------------------
The `sage_functions.py` file contains coppersmith's algorithm.
It is placed separately so it can be imported in each subprocess.

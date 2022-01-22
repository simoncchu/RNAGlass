# RNAGlass

This software is provided ``as is” without warranty of any
kind. In no event shall the author be held responsible for any damage resulting from the
use of this software. The program package, including source codes, executables, and this
documentation, is distributed free of charge.


## **Functionalities and Usage of RNAGlass**
RNAGlass is designed to identify and quantity the transfered mRNA from root to scion (vice versa) in grafted plants. The basic idea is using the root (or scion) specific mutation as barcode to identify and quantify the expressed and transfered mRNAs.

## **Dependencies**

1. bwa (version **0.7.17** or later, require the **-o** option), which can be downloaded from https://github.com/lh3/bwa.
2. samtools (v1.0 or later), which can be downloaded from https://github.com/samtools.
3. Python 3.6 or later version
	+ pysam (https://github.com/pysam-developers/pysam, v0.12 or later) is required to be installed.

		+ In detail, first install Anaconda:
		
			```
			wget https://repo.anaconda.com/archive/Anaconda2-5.2.0-Linux-x86_64.sh
			sh Anaconda2-5.2.0-Linux-x86_64.sh
			```
		
		+ Install pysam:

			```
			conda config --add channels r
			conda config --add channels bioconda
			conda install pysam -y
			```


## **Basic usage**

## **Ouptput**
A VCF file containing the candidate barcode snps will be generated.
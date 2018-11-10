[![Build Status](https://travis-ci.org/robroooh/txt-mng.svg?branch=master)](https://travis-ci.org/robroooh/txt-mng)

# Text Mining Project

## Setting up development environment

make sure you have conda install in your environment, so that we can make sure we use the same versions of python, and libraries. 

```sh
conda create -n txtmng-dev -f environment.yml
source activate txtmng-dev
```
alternatively, please make sure that you're using `python==3.7`
```sh
pip install -r requirements.txt
```
use colab for faster notebook style
https://colab.research.google.com/drive/1EF5sANxEpaFrRXuWnSuSj5dXXwaRiMBx#scrollTo=98NDvVZOdRHj)

## Styling
it might be a good idea to run `yapf -ir file1 file2...` in the root directory of the repo just to make your code have cuter format

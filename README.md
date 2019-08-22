# math-exercises

Latex files with math exercises for http://tekvideo.sdu.dk.

# Getting started guide

Download or clone the git repository
```
git clone git@github.com:henrikmidtiby/math-exercises.git
```

Enter the directory
```
cd math-exercises
```

## Create a virtual environment for the program

Create a virtual environment
```
python3 -m venv env
```

Activate the virtual environment
```
source env/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```


## Convert the first exercise


```
cd 01foundations/01fractions/
python ../../src/exercise_converter/exerciseconverter.py 01simplicification.tex
```

A new file 01simplicification.json should now be present next to the input file 01simplicification.tex.
The .json file is now ready to be uploaded to [tekvideo.sdu.dk].


## Set up the system to handle images in the exercises

### Get a IMGUR client secret.

Register an application that will use the imgur api.
Use the following page [https://api.imgur.com/oauth2/addclient].

I have used the following settings: 

Application name: Exercise converter

Authorization type: OAuth2 authorization without a callback URL

Application website: None

Email: hemi@mmmi.sdu.dk


### Set the imgur client id environmental variable

In the line below, insert the client id, that was obtained in the previous step.
```
export IMGUR_CLIENT_ID='<obtained client id>'
```

### Convert exercises

It is now possible to convert exercises containing images.

```
cd unplaced
python ../src/exercise_converter/exerciseconverter.py insertedimage.tex
```




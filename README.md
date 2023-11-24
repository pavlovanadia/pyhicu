# PYHICU

### Python Hilber Curve Generator

Hilbert curve generator for a specified number of iterations.

### Installation

Clone the reposiory
```bash
git clone git@github.com:pavlovanadia/pyhicu.git
cd pyhicu
```

Create venv and install dependencies (recommended) or skip that step and use any other environment with Matplotlib package
```bash
python3 -m venv environment
source environment/bin/activate
pip install -r requirements.txt
```

### Usage

To run the script, call it from the directory where the tool is located:
```bash
./pyhicu ...
```

Usage options:
```bash
options:
  -h, --help            show this help message and exit
  -i ITERATION, --iteration ITERATION
                        Number of iterations (integer)
  --fs FS               Side of a picture (inches)
  --dc DC               Dot color (hex code or colorname)
  --lc LC               Line color (hex code or colorname)
  -o OUTPUT, --output OUTPUT
                        Output filename
```

# Rock Paper Scissors with Blind Computation

## Setup

0. Install python and anvil

Make sure you have python3 (version >=3.11) and pip, foundry, pidof, and grep installed on your machine.

- [python3 version >=3.11](https://www.python.org/downloads/) version 3.11 or higher with a working [pip](https://pip.pypa.io/en/stable/getting-started/) installed

Use these commands to confirm that you have python3 (version >=3.11) and pip installed:

```
python3 --version
python3 -m pip --version
```

```
# install Foundryup, the Foundry toolchain installer
curl -L https://foundry.paradigm.xyz | bash

# after installation, use the foundryup commmand to install the binaries including Anvil
foundryup
```

1. Install Nillion SDK - https://docs.nillion.com/nillion-sdk-and-tools#installation

2. Run nillion-devnet and get env variables

```
bash ./bootstrap-local-environment.sh
```

3. Create venv and install dependencies

```
python3.11 -m venv .venv
pip3 install --no-cache-dir -r requirements.txt
source .venv/bin/activate
```

4. Play

```
python3 game.py
```

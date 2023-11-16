#!/bin/bash

# Super secure way to install lean /s
wget -q https://raw.githubusercontent.com/leanprover-community/mathlib4/master/scripts/install_debian.sh && bash install_debian.sh ; rm -f install_debian.sh && source ~/.profile

# Install Python and Pip (If not already installed)
sudo apt-get install -y python3 python3-pip

# Install Flask for API development
pip3 install Flask

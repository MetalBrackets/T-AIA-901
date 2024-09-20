#!/bin/bash

# Add path
poetry run pylint aia-script/1_module_speech-to-text/script-speech-to-text.py
poetry run pylint aia-script/2_module_NLP/script-NLP.py
poetry run pylint aia-script/3_module_pathfinder/script-pathfinder.py

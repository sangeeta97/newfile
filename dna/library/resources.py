#!/usr/bin/env python3

from typing import Any
from pathlib import Path
import sys
import os



def get_resource(path: Any) -> str:
    return str("/home/sangeeta/Documents/DNAconvert-main/src/itaxotools/DNAconvert/resources" + "/" + path)

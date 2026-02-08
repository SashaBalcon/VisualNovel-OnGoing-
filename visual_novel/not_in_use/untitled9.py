#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 16:56:41 2025

@author: peppermintbalcon
"""

import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
font_families = tkFont.families()
root.destroy() # Close the temporary root window
print(font_families)
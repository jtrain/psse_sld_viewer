"""
PSSE SLD Viewer
"""

VERSION = (0, 1, 0)

import networkx as nx
import matplotlib.pyplot as plt

import Tkinter as tk
from tkFileDialog import askopenfilename

root= tk.Tk()
root.withdraw()

savedcase = askopenfilename(
    title="Select a PSSE Saved Case",
    filetypes=[('PSSE Saved Cases', '*.sav')],
    initialdir=r"c:/program files/pti/psse32/example/",
    parent=root,
    )

import os
import sys
PSSE_LOCATION = r'c:/program files/pti/psse32/pssbin'
sys.path.append(PSSE_LOCATION)
os.environ['PATH'] += ';' + PSSE_LOCATION

import psspy
import redirect
redirect.psse2py()

psspy.throwPsseExceptions = True

psspy.psseinit(1000)
psspy.case(savedcase)

ierr, (fromnumber, tonumber) = psspy.abrnint(
    sid=-1,
    flag=3,     # for all in service branches and two winding transformers.
    string=["FROMNUMBER", "TONUMBER"])
ierr, (weights,) = psspy.abrncplx(
    sid=-1,
    flag=3,
    string=["RX"]
    )

def inverse(cplx):
    return 1 / cplx.imag

weights = map(abs, weights)

G = nx.DiGraph()
G.add_weighted_edges_from(zip(fromnumber, tonumber, weights))

plt.figure(1, figsize=(20,20))
pos = nx.spring_layout(G, iterations=100)
nx.draw(
    G,
    pos,
    node_size=1600,
    node_color="#ffffff",
    font_size=14,
    edge_color="#444444"
    )

plt.savefig("output.png")


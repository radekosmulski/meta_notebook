# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['VarManager', 'CaptureShellExt', 'Notebook']

# %% ../nbs/00_core.ipynb 2
from execnb.nbio import *
from execnb.shell import *

from fastcore.all import *

# %% ../nbs/00_core.ipynb 4
@patch
def print_vars(self: CaptureShell):
    '''print user defined variables'''
    names = list(self.user_global_ns.keys())[18:]
    print(sorted(names))
    
@patch
def run_cells(self: CaptureShell, cells):
    for cell in cells:
        self.cell(cell)
        if hasattr(cell, 'outputs') and len(cell.outputs) > 0 and cell.outputs[0].output_type == 'error':
            raise RuntimeError(f'#{cell["idx_"]}: {cell.outputs[0].ename} {cell.outputs[0].evalue}')

class VarManager():
    def __init__(self, cs):
        self.cs = cs
    def __getitem__(self, name):
        return self.cs.user_global_ns[name]
    def __setitem__(self, name, val):
        if name == 'cs':
            super().__setattr__(name, val)
        else:
            self.cs.run(f'{name} = {val}')

class CaptureShellExt(CaptureShell):
    '''CaptureShell with additional functionality'''
    def __init__(self):
        super().__init__()
        self.var = VarManager(self) 

# %% ../nbs/00_core.ipynb 7
class Notebook():
    def __init__(self, path):
        self.nb = read_nb(path)
    
    @property
    def cells(self):
        return self.nb.cells
    
    def find(self, tag):
        '''finds the first occurence of `tag` (any string) in the notebook'''
        for i, cell in enumerate(self.cells):
            if tag in cell.source:
                return i
    
    def to(self, tag):
        '''runs the cells from `tag` to the end of the notebook'''
        return self.cells[self.find(tag):]
    
    def between(self, tag1, tag2):
        tag1_pos = self.find(tag1)
        tag2_pos = self.find(tag2)
        
        return self.cells[tag1_pos:tag2_pos]

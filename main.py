import sys
import toml
import csv
import subprocess as sp
from dataclasses import dataclass
import requests
import os

for i in [ 'OMPI_MCA_btl', 'LD_LIBRARY_PATH', 'UCX_NET_DEVICES' ]:
    os.environ.pop(i)


class HPL_Sweep:
    def __init__(self, hpl_path, executable, log_file, linen, N, log_url=''):
        self.hpl_path = hpl_path
        self.exec = executable
        self.log_file = log_file
        self.log_url = log_url
        self.N = N
        self.linen = linen
        self.data = {
            'P': [],
            'Q': [],
            'N': [],
            'NB': [],
            'gflops': [],
        }

    def signal(self,msg):
        if (self.log_url != ''): requests.post(self.log_url, data=msg)

    def serialize(self):
        with open(f'self.log_file.cxv', 'w') as f:
            w = cxv.DictWriter(f, self.data.keys())
            w.writeheader()
            w.writerow(sel.data)


    def run(self, P, Q, N, NB):
        result = sp.run([self.exec, 
                'P', str(P), 'Q', str(Q), 
                'N', str(N), 'NB', str(NB), 
           ], 
            cwd=self.hpl_path,
            capture_output=True,
            text=True
        )
        return float(result.stdout.strip().splitlines()[self.linen].split()[-2])

    def sweep(self):
        self.signal("{self.exec} Sweep Initialized")
# uncomment for big run
#        for p in [1,2,4,8,16]:
#            for q in [1,2,4,8,16]:
#                for nb in range(10, 2000, 10):
        for p in [1,2,4,8,16]:
            for q in [1,2,4,8,16]:
                for nb in range(640, 641,10):
                    self.signal(f'{self.exec} starting (P,Q,NB): ({p},{q},{nb})')
                    res = self.run(p, q, self.N, nb)

                    self.data['P'].append(p)
                    self.data['Q'].append(q)
                    self.data['NB'].append(nb)
                    self.data['P'].append(self.N)
                    self.data['gflops'].append(res)

                    self.signal(f'{self.exec} finished (P,Q,NB): ({p},{q},{nb}) -> {res} gflops')
        self.serialize()
        self.signal("{self.exec} Sweep Finished")

def main():
    hplsweeper = HPL_Sweep('/home/k6vu/dev/rocHPL/build/', 
                        './mpirun_rochpl',
                        'hpl-sweep', 
                        -3, 437256)
    mxpsweeper = HPL_Sweep('/home/k6vu/dev/rocHPL-MxP/build/', 
                        './mpirun_rochplmxp',
                        'hplmxp-sweep', 
                        -2, 624652)

    hplsweeper.sweep()
    mxpsweeper.sweep()

if __name__ == "__main__":
    main()

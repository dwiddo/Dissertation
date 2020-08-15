from ccdc.io import CrystalReader
import traceback

csd_crystal_reader = CrystalReader('CSD')

exceptions = []
exception_count = []
from progressbar import progressbar
for i, crystal in enumerate(progressbar(csd_crystal_reader)):
    try:
        cell = crystal.reduced_cell
    except Exception as e:
        e = str(e)
        if e in exceptions:
            exception_count[exceptions.index(e)] += 1
        else:
            exceptions.append(str(e))
            exception_count.append(1)


with open('LOG.txt', 'w') as logfile:
    for e, count in zip(exceptions, exception_count):
        logfile.write(e + '\n')
        logfile.write("count: " + str(count) + "\n")

import csv
import threading


class Writer:

    def __init__(self, outfile, header):
        self._lock = threading.Lock()
        self.csv_file = open(outfile, mode='w', newline='')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(header)

    def write_row(self, metrics):
        with self._lock:
            self.writer.writerow(metrics)

    def __del__(self):
        self.csv_file.close()

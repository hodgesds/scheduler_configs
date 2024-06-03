#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np


class sample:
    def __init__(self, trans_sec, query_sec, lat_min, lat_avg, lat_max, lat_95th):
        self.trans_sec = trans_sec
        self.query_sec = query_sec
        self.lat_min = lat_min
        self.lat_avg = lat_avg
        self.lat_max = lat_max
        self.lat_95th = lat_95th


def parse(data_file):
    samples = []
    with open(data_file) as f:
        trans_sec = 0
        query_sec = 0
        lat_min = 0
        lat_avg = 0
        lat_max = 0
        lat_95th = 0
        seen_lat = False
        for line in f:
            line = line.replace("\n", "")
            if 'transactions:' in line:
                trans_sec = float(line.split("(")[1].split(" ")[0])
                seen_lat = False
            if 'queries:' in line:
                query_sec = float(line.split("(")[1].split(" ")[0])
            if 'Latency (ms):' in line:
                seen_lat = True
            if seen_lat:
                if 'min:' in line:
                    lat_min = float(line.replace(" ","").split(":")[1])
                if 'avg:' in line:
                    lat_avg = float(line.replace(" ","").split(":")[1])
                if 'max:' in line:
                    lat_max = float(line.replace(" ","").split(":")[1])
                if '95th percentile:' in line:
                    lat_95th = float(line.replace(" ","").split(":")[1])
                    samples.append(sample(trans_sec, query_sec, lat_min, lat_avg, lat_max, lat_95th))


    return samples

def parse_files(files):
    data = {}
    for f in files:
        sched = f.split(".")[0]
        samples = parse(f)
        data[sched] = {}
        data[sched]["transactions/sec"] = np.array([ x.trans_sec for x in samples])
        data[sched]["query/sec"] = np.array([ x.query_sec for x in samples])
        data[sched]["latency min"] = np.array([ x.lat_min for x in samples])
        data[sched]["latency avg"] = np.array([ x.lat_avg for x in samples])
        data[sched]["latency max"] = np.array([ x.lat_max for x in samples])
        data[sched]["latency p95"] = np.array([ x.lat_95th for x in samples])

    labels = data.keys()



    for stat in ["transactions/sec", "query/sec", "latency min", "latency avg", "latency max", "latency p95"]:
        fig, ax = plt.subplots()
        ax.set_ylabel(stat)
        bplot = ax.boxplot([ data[sched][stat] for sched in labels], patch_artist=True, labels=labels)
        plt.savefig(stat.replace("/", "_").replace("/", "_").replace(" ", "_")+".png")


    # for patch, color in zip(bplot['boxes'], colors):
    #     patch.set_facecolor(color)

    # plt.show()


if __name__ == '__main__':
    parse_files(sys.argv[1:])


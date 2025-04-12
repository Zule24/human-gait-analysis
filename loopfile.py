import os
import pandas as pd
from pandas import Timestamp
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from multiprocessing import Pool

FOLDER_NAME = "subjects" #replace with subjects when ready for full run
#FOLDER_NAME = "test1"


def create_plots(i):
    newfolder = "processed_data/"+i
    os.mkdir(newfolder)

    #timestamp formatting
    dateparse = lambda x: datetime.strptime(x[:-6], "%Y-%m-%d %H:%M:%S.%f")

    #open csv
    df = pd.read_csv((os.path.join(FOLDER_NAME, i)), parse_dates=['loggingTime.txt.'], date_parser=dateparse)

    #timestamp formatting
    df['loggingTime.txt.'] = df['loggingTime.txt.'].apply(lambda x: x.timestamp())
    df['loggingTime.txt.'] -= df['loggingTime.txt.'][0]

    #clean speed data
    #replace zeros or near-zero values with NaN
    df['locationSpeed.m.s.'] = df['locationSpeed.m.s.'].replace(0, np.nan)
    df['locationSpeed.m.s.'] = df['locationSpeed.m.s.'].mask(df['locationSpeed.m.s.'] < 0.05)

    #fill gaps with interpolation (optional but helpful for visualization)
    df['locationSpeed.m.s.'] = df['locationSpeed.m.s.'].interpolate()

    #smooth with a rolling median or mean
    df['cleaned_speed'] = df['locationSpeed.m.s.'].rolling(window=5, center=True, min_periods=1).median()

    #set range for x axis
    max = (df['loggingTime.txt.'].max())
    min = (df['loggingTime.txt.'].min())

    #plot
    plot1 = df.plot(x='loggingTime.txt.', y =('motionUserAccelerationX.G.'),color='orange',fontsize = 7,kind='scatter', s = 2, title="X", xlabel = 'Time in Seconds')
    plot2 = df.plot(x='loggingTime.txt.', y =('motionUserAccelerationY.G.'), color='green',fontsize = 7, kind='scatter',  s = 2,title="Y", xlabel = 'Time in Seconds')
    plot3 = df.plot(x='loggingTime.txt.', y =('motionUserAccelerationZ.G.'),color='blue',fontsize = 7, kind='scatter', s = 2, title="Z", xlabel = 'Time in Seconds')
    plot4 = df.plot(x='loggingTime.txt.', y =('locationSpeed.m.s.'),color='blue',fontsize = 7, kind='line', title="Speed", xlabel = 'Time in Seconds')
    xinterval = np.arange(min,max,40)
    plot1.set_xticks(xinterval)
    plot2.set_xticks(xinterval)
    plot3.set_xticks(xinterval)
    plot4.set_xticks(xinterval)

    plot1.figure.savefig(newfolder+'/x.png')
    plot2.figure.savefig(newfolder+'/y.png')
    plot3.figure.savefig(newfolder+'/z.png')
    plot4.figure.savefig(newfolder+'/speed.png')

    plt.close(plot1.figure)
    plt.close(plot2.figure)
    plt.close(plot3.figure)
    plt.close(plot4.figure)


    #plt.show()

#---------------------------------------------------------------------------------
#Goes through subjects folder and creates a folder in processed_data for each one
#makes 4 figs each, x.png, y.png, z.png and speed.png
#----------------------------------------------------------------------------------

#get folder and creates array that holds all csv files inside
numFiles = [f for f in os.listdir(FOLDER_NAME) if f.endswith('.csv')]

#for each csv make new folder and make figures
N_PROCESSES = 4
with Pool(N_PROCESSES) as pool:
    pool.map(create_plots, numFiles)

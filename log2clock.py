import re, sys, os.path
import numpy as np
from datetime import datetime, timezone
import matplotlib.pyplot as plt

if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        filename = sys.argv[1]
    else:
        print('File does not exist')
else:
    print('Please, provide one filename')

usec = float(1e-6)

def fmoutRead(files):
    timeStamps = []
    offsets = []
    gps_re = re.compile('.*(\w{4}.\w*.\w*:\w*:\w*.\w*).*gps-fmout/([-+]*\d*.\d*[eE][+-]\d*).*')
    fmout_re = re.compile('.*(\w{4}.\w*.\w*:\w*:\w*.\w*).*fmout-gps/([-+]*\d*.\d*[eE][+-]\d*).*')
    #gps_re = re.compile('.*(2020.*)/gps-fmout/([-+]\d*.\d*[eE][+-]\d*).*')
    #fmout_re = re.compile('.*(2020.*)/fmout-gps/([-+]\d*.\d*[eE][+-]\d*).*')
    for lines in open(files):
        match_gps = gps_re.match(lines)
        match_fmout = fmout_re.match(lines)
        if match_gps:
            timestamp = timeConvert(match_gps[1])
            timeStamps.append(timestamp)
            offsets.append(float(match_gps[2])/usec)
        elif match_fmout:
            timestamp = timeConvert(match_fmout[1])
            timeStamps.append(timestamp)
            # ATTENTION: minus sign (to check with log2vex!)
            offsets.append(-float(match_fmout[2])/usec)
    return timeStamps, offsets

def timeConvert(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, '%Y.%j.%H:%M:%S.%f')
    timestamp = date_time_obj.replace(tzinfo=timezone.utc).timestamp()
    return timestamp

def estimate_coef(x, y): 
    n = np.size(x) 
    m_x, m_y = np.mean(x), np.mean(y) 
  
    # Cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x 
  
    # Regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 
  
    return(b_0, b_1) 
  
def plot_regression_line(x, y, b): 
    plt.plot(x, y, color = "m", marker = "o") 
  
    # predicted response vector 
    y_pred = b[0] + b[1]*x 
  
    # plotting the regression line 
    plt.plot(x, y_pred, color = "g") 
    plt.xlabel('x') 
    plt.ylabel('y') 
  
    plt.show() 


if __name__ ==  '__main__':
    times, offs = fmoutRead(filename)
    b = estimate_coef(np.array(times), np.array(offs))
    print("Estimated rate = {} usec/s".format(b[1])) 
    #plot_regression_line(np.array(times), np.array(offs), b)

    print(times)
    

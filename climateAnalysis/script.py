import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
import sys

def solow(RSS1,RSS2,n):
    return ((RSS1 - RSS2)/3)/(RSS2/(n-4)) > scipy.stats.f.ppf(0.95,3,n-4) 
    #Alpha = 0.05
def Ztest(sub1, sub2):
    X1 = np.mean(sub1)
    X2 = np.mean(sub2)
    sd1 = np.std(sub1)
    sd2 = np.std(sub2)
    n1 = len(sub1)
    n2 = len(sub2)
    pooledSE = np.sqrt(sd1**2/n1 + sd2**2/n2)
    z = (X1 - X2)/pooledSE
    return np.abs(z) > np.abs(scipy.stats.norm.ppf(0.025)) 
    #Bilateral test: Alpha = 0.05

def load_data():
    col_stations = ['province','id','name','longitude','latitude','height',
        'unknown']
    stationsID = pd.read_csv(r'data\ESTACIONES.txt', sep=';', header=None, 
        names=col_stations).drop(columns='unknown')

    station = {}
    for id in stationsID['id'].iteritems():
        station[str(id[1])] = pd.read_csv('data/Tmin_'+str(id[1])+
            '_filled_annual_means.txt', sep='    ',
            header=None, names=['year',str(id[1])], 
            engine='python').set_index('year')
    stations = pd.concat(station.values(),axis=1)
    return stations, stationsID

def discontinuity(OriRefDF, start, end):
    _, RSS1, _, _, _ = np.polyfit(OriRefDF.index[start:end],OriRefDF['diff'].iloc[start:end],1,full=True)
    OriRefDF['RSS2'] = RSS1[0]
    for point in range(start + 5,end-start-5):
        sub1 = OriRefDF['diff'].iloc[start:point]
        sub2 = OriRefDF['diff'].iloc[point:end]
        _, RSSs1,_,_,_ = np.polyfit(OriRefDF.index[start:point],sub1,1,full=True)
        #sublinear_reg1 = np.poly1d(subcoef1)
        _, RSSs2,_,_,_ = np.polyfit(OriRefDF.index[point:end],sub2,1,full=True)
        #sublinear_reg1 = np.poly1d(subcoef2)
        OriRefDF['RSS2'].iloc[point] = RSSs1[0] + RSSs2[0]
    point = OriRefDF.index.get_loc(OriRefDF['RSS2'].idxmin())
    RSS2 = OriRefDF['RSS2'].min()

    if solow(RSS1,RSS2,end-start):
        sub1 = OriRefDF['diff'].iloc[start:point]
        sub2 = OriRefDF['diff'].iloc[point:end]
        if Ztest(sub1,sub2):
            return True, point
        else:
            return False, 0
    else:
        return False, 0

def search_discont(OriRefDF):
    points=[]
    value, point = discontinuity(OriRefDF,0,OriRefDF.shape[0]-1)
    if value == True:
        points.append(point)
        if points[0] <= 9:
            value, point = discontinuity(OriRefDF,points[0],OriRefDF.shape[0]-1)
            if value == True:
                points.append(point)
        elif points[0] <= OriRefDF.shape[0] - 10:
            value, point = discontinuity(OriRefDF,0,points[0])
            if value == True:
                points.append(point)
            value, point = discontinuity(OriRefDF,points[0],OriRefDF.shape[0]-1)
            if value == True:
                points.append(point)
        elif points[0] >= OriRefDF.shape[0] - 10:
            value, point = discontinuity(OriRefDF,0,points[0])
            if value == True:
                points.append(point)
    else:
        print('No discontinuities found.')
        return 0
    print('Discontinuities in: ')
    for point in points:
        print('\t'+ str(1956 + point))
    return points

def fix_plot_data(OriRefDF, points, origin):
    OriRefDF['Fixed']=OriRefDF['Original']
    means = []
    points.append(OriRefDF.shape[0]-1)
    prevPoint = 0
    for point in points:
        means.append(OriRefDF['diff'].iloc[prevPoint:point].mean())
        prevPoint = point
    prevPoint = 0
    points = points[:-1]
    for i,point in enumerate(points):
        OriRefDF['Fixed'].iloc[prevPoint:point] = OriRefDF['Fixed'].iloc[prevPoint:point] + \
            means[i+1] - means[i]
        prevPoint = point
    plt.figure(figsize=(10,7))
    plt.plot(OriRefDF.index,OriRefDF['Original'],label='Original')
    plt.plot(OriRefDF.index,OriRefDF['Reference'],label='Reference')
    plt.plot(OriRefDF.index,OriRefDF['Fixed'],label='Fixed')

    plt.legend()
    ymin = min(OriRefDF['Original'].min(),OriRefDF['Reference'].min(),OriRefDF['Fixed'].min())
    ymax = max(OriRefDF['Original'].max(),OriRefDF['Reference'].max(),OriRefDF['Fixed'].max())
    plt.ylim(ymin,ymax)
    for point in points:
        plt.vlines(1956+point,ymin,ymax, linestyles='dashed')
    plt.xlabel('Año')
    plt.ylabel('Temperatura (ºC)')
    plt.show()
    ask = input('Save figure? (WARNING: This could overwrite some files) ')
    if ask.capitalize() in ['Yes','Si']:
        plt.savefig('station_'+origin+'.png')
        print('Figure saved as station_%s.png' % (origin))
    else:
        print('Figure not saved.')

def main():

    stations, stationsID = load_data()

    if len(sys.argv) > 1:
        origin = sys.argv[1]
    else:
        print(stationsID[['id','name']])
        origin = input('Origin (ID): ')
    oriSeries = stations[origin]

    ydiff ={}
    for col in stations.columns[:]:
        ydiff[col] = stations[col].shift(-1)-stations[col]
    yearDiff = pd.concat(ydiff.values(), axis=1).drop(1998)

    correlations = yearDiff.corr(method='pearson')
    bestSts = correlations[origin][correlations[origin] > 0.35].drop(origin). \
                sort_values(ascending=False).head(5).to_frame(name='corrCoef') 
                #drops origin index with corr = 1
    bestSts['corrCoef2'] = bestSts['corrCoef']**2

    refDict = {}
    for index in bestSts.index:
        refDict[index] = yearDiff[index]*bestSts['corrCoef2'].loc[index]
    refSeriesDiff = pd.concat(refDict.values(), 
        axis=1).sum(axis=1)/bestSts['corrCoef2'].sum()

    refSeries = oriSeries.copy()
    for i,diff in enumerate(refSeriesDiff.sort_index(ascending=False).tolist()):
        refSeries.loc[1998-(i+1)] = refSeries.loc[1998-i]-diff
    refSeries = refSeries.sort_index()

    OriRefDF = pd.concat({'Reference':refSeries, 'Original':oriSeries}, axis=1)
    OriRefDF['diff']=OriRefDF['Original'] - OriRefDF['Reference']


    points = search_discont(OriRefDF)

    fix_plot_data(OriRefDF, points, origin)


if __name__ == '__main__':
    main()
import datetime
import time
import pandas as pd
import requests

from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, DCCSOptions, EdgeData, EdgeTag

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def Creat_agedAgent():
    edgeAgentOptions = EdgeAgentOptions(nodeId="60902660-f772-4e6b-97bf-f846841da7e7")
    edgeAgentOptions.connectType = constant.ConnectType['DCCS']
    dccsOptions = DCCSOptions(apiUrl="https://api-dccs-ensaas.education.wise-paas.com/",
                              credentialKey="f08e7cf43849ce07281164da4c8f04s7")
    edgeAgentOptions.DCCS = dccsOptions
    edgeAgent = EdgeAgent(edgeAgentOptions)

    return edgeAgent


def getNumberOfDbs(location):
    URL = "http://140.112.94.123:20000/PEST_DETECT/_rwsn/get_number_of_dbs.php?location=" + location
    r = requests.get(url=URL)
    data = r.json()
    number_of_dbs = data['RESULT'][0]['NUM']

    return number_of_dbs


def generateData():
    tagList = {'T': 'ATag1', 'H': 'ATag2', 'L': 'ATag3', 'TVOC': 'ATag4', 'CO2': 'ATag5', 'cranefly': 'ATag6', 'fly': 'ATag7',
     'gnat': 'ATag8', 'midge': 'ATag9', 'mosquito': 'ATag10', 'mothfly': 'ATag11', 'thrips': 'ATag12', 'whitefly': 'ATag13'}
    DataList = ['T', 'H', 'L', 'TVOC', 'CO2', 'cranefly', 'fly', 'gnat', 'midge', 'mosquito', 'mothfly', 'thrips', 'whitefly']

    # collect data
    edgeData = EdgeData()

    for sensor in DataList:
        if sensor in ['T', 'H', 'L']:
            data = pd.read_csv(
                "E:/XAMPP/htdocs/PEST_DETECT/___csv_data/_V3/envi/current/ntusmart_gh_current_" + sensor + ".csv",
                index_col=0)
            for i in range(6):
                temp_time = data['Date' + str(i + 1)]
                temp_time = temp_time[0]
                temp_time = datetime.datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S")

                temp_data = data[str(i + 1)]
                temp_data = temp_data[0]

                tag = EdgeTag('Device' + str(i + 1), tagList[sensor], temp_data)
                edgeData.tagList.append(tag)
                edgeData.timestamp = temp_time
        elif sensor in ['TVOC', 'CO2']:
            data = pd.read_csv(
                "E:/XAMPP/htdocs/PEST_DETECT/___csv_data/_V3/pesticide/current/ntusmart_gh_current_" + sensor + ".csv",
                index_col=0)
            for i in range(6):
                temp_time = data['Date' + str(i + 1)]
                temp_time = temp_time[0]
                temp_time = datetime.datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S")

                temp_data = data[str(i + 1)]
                temp_data = temp_data[0]

                tag = EdgeTag('Device' + str(i + 1), tagList[sensor], temp_data)
                edgeData.tagList.append(tag)
                edgeData.timestamp = temp_time
        else:
            data = pd.read_csv(
            "E:/XAMPP/htdocs/PEST_DETECT/___csv_data/_V3/count/current/ntusmart_gh_{:03d}"
            .format(int(getNumberOfDbs("ntusmart_gh"))) + "_current_" + insect + ".csv",
            index_col=0)
            for i in range(6):
                temp_time = data['Date' + str(i + 1)]
                temp_time = temp_time[0] + ":00"  # add second to fit datetime format
                temp_time = datetime.datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S")

                temp_data = data[str(i + 1)]
                temp_data = float(temp_data[0])  # upload format must be float not int

                tag = EdgeTag('Device' + str(i + 1), tagList[sensor], temp_data)
                edgeData.tagList.append(tag)
                edgeData.timestamp = temp_time

    return edgeData


if __name__ == "__main__":
    edgeAgent = Creat_agedAgent()
    edgeAgent.connect()
    while 1:
        print(datetime.datetime.now())
        data = generateData()
        edgeAgent.sendData(data)
        time.sleep(5)
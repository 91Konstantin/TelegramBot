from suds.sudsobject import asdict
from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor

imp = Import('http://www.w3.org/2001/XMLSchema', location='http://www.w3.org/2001/XMLSchema.xsd')
url = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
client = Client(url, doctor=ImportDoctor(imp))

def GetCurString():
    Curs = client.service.AllDataInfoXML()
    DictCurs = asdict(Curs)
    USDCurs = DictCurs['AllData']['MainIndicatorsVR']['Currency']['USD']['curs']
    USDCursDate = DictCurs['AllData']['MainIndicatorsVR']['Currency']['USD']['_OnDate']
    EURCurs = DictCurs['AllData']['MainIndicatorsVR']['Currency']['EUR']['curs']
    EURCursDate = DictCurs['AllData']['MainIndicatorsVR']['Currency']['EUR']['_OnDate']
    KEY_RATE_val = DictCurs['AllData']['KEY_RATE']['_val']
    KEY_RATE_date = DictCurs['AllData']['KEY_RATE']['_date']
    Inflation_val = DictCurs['AllData']['MainIndicatorsVR']['Inflation']['_val']
    Inflation_OnDate = DictCurs['AllData']['MainIndicatorsVR']['Inflation']['_OnDate']
    InflationTarget_val = DictCurs['AllData']['MainIndicatorsVR']['InflationTarget']['_val']

    CurStringUSD = str('USD: ') +USDCurs + str('руб.')+ str(' на дату ') + USDCursDate
    CurStringEUR = str('EUR: ') +EURCurs + str('руб.')+ str(' на дату ') + EURCursDate
    KeyRateString = str('Ключевая ставка ЦБ: ') + KEY_RATE_val + str('% с ') + KEY_RATE_date
    InflationString = str('Инфляция: ') + Inflation_val + str('% ') + str(' на дату ') + Inflation_OnDate + str('/ Цель: ') + InflationTarget_val + str('% ')

    return CurStringUSD, CurStringEUR, KeyRateString, InflationString

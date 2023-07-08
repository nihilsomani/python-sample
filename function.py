import pandas as pd
import requests
import json
from datetime import date

def available_bid_offers(country_name):
    xls = pd.ExcelFile('/home/ec2-user/hackathon/AutoKaas_dummy_data_v4.xlsx')
    df = pd.read_excel(xls, 'Prices')
    df = df.fillna('')
    return df[df['Country']==country_name].to_dict('records')

def submit_bid_offer(data):
    df = pd.read_excel('/home/ec2-user/hackathon/Bid_Offer.xlsx')
    data['Req_ID'] = len(df)+1
    data['Date'] = pd.to_datetime('now')
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y', errors='coerce').dt.date
    df.to_excel('/home/ec2-user/hackathon/Bid_Offer.xlsx', index = False)
    return "Bid Submitted"

def no_of_open_contracts(row):
    if((row - pd.to_datetime('now')).days>0):
        return "Open"
    else:
        return "Close"
    

def open(partner_description):
    xls = pd.ExcelFile('/home/ec2-user/hackathon/AutoKaas_dummy_data_v4.xlsx')
    df1 = pd.read_excel(xls, 'contract_line_item')
    df2 = pd.read_excel(xls, 'contract_partner')
    df1 = pd.merge(df1, df2, on='contract_number')

    df1 = df1.fillna('')
    df1['delivery_beginning_date'] = pd.to_datetime(df1['delivery_beginning_date'])
    df1['delivery_end_date'] = pd.to_datetime(df1['delivery_end_date'])

    df1['contract_status'] = df1['delivery_end_date'].apply(lambda x:no_of_open_contracts(x))
    return df1[(df1['contract_status']=="Open") & (df1['partner_description']==partner_description)]['contract_number'].tolist()

def status_of_contract(contract_number):
    xls = pd.ExcelFile('/home/ec2-user/hackathon/AutoKaas_dummy_data_v4.xlsx')
    df = pd.read_excel(xls, 'contract_line_item')
    df['delivery_beginning_date'] = pd.to_datetime(df['delivery_beginning_date'])
    df['delivery_end_date'] = pd.to_datetime(df['delivery_end_date'])
    df['contract_status'] = df['delivery_end_date'].apply(lambda x:no_of_open_contracts(x))
    row = df[df['contract_number']==contract_number]

    return row.iloc[0]['contract_status']

def contract_data(contract_number,column_name):
    xls = pd.ExcelFile('/home/ec2-user/hackathon/AutoKaas_dummy_data_v4.xlsx')
    df = pd.read_excel(xls, 'contract_line_item')
    df['delivery_beginning_date'] = pd.to_datetime(df['delivery_beginning_date'])
    df['delivery_end_date'] = pd.to_datetime(df['delivery_end_date'])
    df['contract_status'] = df['delivery_end_date'].apply(lambda x:no_of_open_contracts(x))
    row = df[df['contract_number']==contract_number]

    return row.iloc[0][column_name]


def bid_offers(client_id,status=""):
    df = pd.read_excel('/home/ec2-user/hackathon/Bid_Offer.xlsx')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Status'] = df['Date'].apply(lambda x:"Expired" if((pd.to_datetime('now')-x).days>0) else "Under Review")
    #print(df.dtypes)
    #print(df)
    df.to_excel('/home/ec2-user/hackathon/Bid_Offer.xlsx', index = False)
    
    if(status=="Under Review"):
        return df[(df['Client_ID']==client_id) & (df['Status']=="Under Review")].to_dict('records')
    elif(status=="Expired"):
        return df[(df['Client_ID']==client_id) & (df['Status']=="Expired")].to_dict('records')
    else:
        return df[df['Client_ID']==client_id].to_dict('records')
    
    
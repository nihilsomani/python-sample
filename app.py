from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from function import available_bid_offers, submit_bid_offer, open, status_of_contract,contract_data,bid_offers

from fastapi_utils.tasks import repeat_every
app=FastAPI(docs_url="/hackathon/docs",
            openapi_url="/hackathon/openapi.json",
            title="Hackathon Microservice"
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)



class Bid(BaseModel):
    client_id: str
    bid_offer_id: int
    base_price: int
    quote_price: int
    quote_volume: int
    offer_validity: str
    status: str

class Partner(BaseModel):
    partner: str

@app.get('/hackathon/health')
def get_func():
    return "Alive"
    
@app.post('/hackathon/available_bid_offer')
def available_bids(country_name: str):
    status = available_bid_offers(country_name)
    #print(status)
    return status 
    
@app.post('/hackathon/submit_bid')
def submit_bids(bid: Bid):
    data = {
        "Client_ID":bid.client_id,
        "Bid/Offer ID":bid.bid_offer_id,
        "Basis/Flat Price":bid.base_price,
        "Quote Price":bid.quote_price,
        "Quote Volume":bid.quote_volume,
        "Offer Validity":bid.offer_validity,
        "Status":bid.status
    }
    status = submit_bid_offer(data)
    return status 


 
@app.get('/hackathon/bid_status')
def bid_status(client_id: str,status: str):
    status = bid_offers(client_id,status)
    return status 

 
@app.post('/hackathon/open_contracts')
def open_contracts(partner_desc: Partner):
    status = open(partner_desc.partner)
    return status 

 
@app.post('/hackathon/contract_status')
def contract_status(contract_number: int):
    status = status_of_contract(contract_number)
    return status 


@app.post('/hackathon/contract_detail')
def contract_status(contract_number: int,column_name: str):
    status = contract_data(contract_number,column_name)
    return status 

if __name__=='__main__':
    uvicorn.run("app:app",port=3300,host="0.0.0.0", reload = True)

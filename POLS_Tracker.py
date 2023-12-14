import streamlit as st
import time
from datetime import datetime, timezone, timedelta
import requests
import json
import base64
from web3 import Web3
from web3.auto import w3

    
abi = """
[{"inputs":[],"name":"CurrencyInvalid","type":"error"},{"inputs":[],"name":"ETHTransferFailed","type":"error"},{"inputs":[],"name":"EmptyOrderCancelList","type":"error"},{"inputs":[],"name":"EthscriptionInvalid","type":"error"},{"inputs":[],"name":"ExpiredSignature","type":"error"},{"inputs":[],"name":"InsufficientConfirmations","type":"error"},{"inputs":[],"name":"MerkleProofInvalid","type":"error"},{"inputs":[{"internalType":"uint256","name":"length","type":"uint256"}],"name":"MerkleProofTooLarge","type":"error"},{"inputs":[],"name":"MsgValueInvalid","type":"error"},{"inputs":[],"name":"NoncesInvalid","type":"error"},{"inputs":[],"name":"OrderExpired","type":"error"},{"inputs":[],"name":"OrderNonceTooLow","type":"error"},{"inputs":[],"name":"RecipientInvalid","type":"error"},{"inputs":[],"name":"SignatureInvalid","type":"error"},{"inputs":[],"name":"SignerInvalid","type":"error"},{"inputs":[],"name":"TrustedSignatureInvalid","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"newMinNonce","type":"uint256"},{"indexed":false,"internalType":"uint64","name":"timestamp","type":"uint64"}],"name":"CancelAllOrders","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"orderNonces","type":"uint256[]"},{"indexed":false,"internalType":"uint64","name":"timestamp","type":"uint64"}],"name":"CancelMultipleOrders","type":"event"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"orderNonce","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"ethscriptionId","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"quantity","type":"uint256"},{"indexed":false,"internalType":"address","name":"seller","type":"address"},{"indexed":false,"internalType":"address","name":"buyer","type":"address"},{"indexed":false,"internalType":"address","name":"currency","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"uint64","name":"endTime","type":"uint64"}],"name":"EthscriptionOrderExecuted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"bytes32","name":"ethscriptionId","type":"bytes32"},{"indexed":false,"internalType":"uint64","name":"timestamp","type":"uint64"}],"name":"EthscriptionWithdrawn","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"trustedVerifier","type":"address"}],"name":"NewTrustedVerifier","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ethscriptions_protocol_TransferEthscriptionForPreviousOwner","type":"event"},{"stateMutability":"nonpayable","type":"fallback"},{"inputs":[],"name":"cancelAllOrders","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"orderNonces","type":"uint256[]"}],"name":"cancelMultipleMakerOrders","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"signer","type":"address"},{"internalType":"address","name":"creator","type":"address"},{"internalType":"bytes32[]","name":"ethscriptionIds","type":"bytes32[]"},{"internalType":"uint256[]","name":"quantities","type":"uint256[]"},{"internalType":"address","name":"currency","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint64","name":"startTime","type":"uint64"},{"internalType":"uint64","name":"endTime","type":"uint64"},{"internalType":"uint16","name":"protocolFeeDiscounted","type":"uint16"},{"internalType":"uint16","name":"creatorFee","type":"uint16"},{"internalType":"bytes","name":"params","type":"bytes"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct BatchOrder.EthscriptionOrder","name":"order","type":"tuple"},{"components":[{"internalType":"bytes32","name":"root","type":"bytes32"},{"components":[{"internalType":"bytes32","name":"value","type":"bytes32"},{"internalType":"enum BatchOrder.MerkleTreeNodePosition","name":"position","type":"uint8"}],"internalType":"struct BatchOrder.MerkleTreeNode[]","name":"proof","type":"tuple[]"}],"internalType":"struct BatchOrder.MerkleTree","name":"merkleTree","type":"tuple"},{"internalType":"address","name":"recipient","type":"address"}],"name":"executeOrderWithMerkle","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"root","type":"bytes32"},{"internalType":"uint256","name":"proofLength","type":"uint256"}],"name":"hashBatchOrder","outputs":[{"internalType":"bytes32","name":"batchOrderHash","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"orderNonce","type":"uint256"}],"name":"isUserOrderNonceExecutedOrCancelled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_trustedVerifier","type":"address"}],"name":"updateTrustedVerifier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userMinOrderNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address payable","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"ethscriptionId","type":"bytes32"},{"internalType":"uint64","name":"expiration","type":"uint64"},{"internalType":"bytes","name":"trustedSign","type":"bytes"}],"name":"withdrawEthscription","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"ethscriptionIds","type":"bytes32[]"},{"internalType":"uint64","name":"expiration","type":"uint64"},{"internalType":"bytes","name":"trustedSign","type":"bytes"}],"name":"withdrawMultipleEthscriptions","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
"""


contract = w3.eth.contract(abi=abi)

polygon_api = st.secrets["POL_API"]

def get_pol_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=MATICUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

def POL_balance_ix(address):
# Define the API endpoint and parameters
    BASE_URL = "https://api.polygonscan.com/api"
    PARAMS = {
        "module": "account",
        "action": "txlist",
        "address": f"{address}",
        "startblock": 50500000,
        "endblock": 60000000,
        "page": 1,
        "offset": 100,
        "sort": "desc",
        "apikey": "U6N3PK19T5815DV893JNSBAAK66P7W1TAA"  # Replace with your actual API key
    }

    # Make the request
    response = requests.get(BASE_URL, params=PARAMS)
    data = response.json()
    return data['result']


def main_content():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        時間(GMT+8)
    </div>
    """, unsafe_allow_html=True)
    with col2:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        狀態
    </div>
    """, unsafe_allow_html=True)
    with col3:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        數量(10^8)
    </div>
    """, unsafe_allow_html=True)
    with col4:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        總價 Matic($)
    </div>
    """, unsafe_allow_html=True)
    with col5:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 10px; margin-top: 10px; background-color: blue; color: white;'>
        單價 Matic($)
    </div>
    """, unsafe_allow_html=True)
    # if st.button("Start Fetching Data"):
    with st.empty():
        while True:
            new_data = POL_balance_ix("0x6acEd66903866FfDe0d85AaB947C81C3f6c38CDd")
            time_list = []
            quantity_list = []
            value_list = []
            unit_value_list = []
            status_list = []
            for i in new_data:
                if i["methodId"] == "0xee2f675e":
                    time_list.append(i["timeStamp"])
                    status_list.append(i["txreceipt_status"])
                    decoded_input = contract.decode_function_input(i["input"])
                    quatity = decoded_input[1]["order"][3][0]/1e8
                    value = decoded_input[1]["order"][5]/1e18
                    unit_price = value/quatity
                    quantity_list.append(round(quatity, 2))
                    value_list.append(round(value, 2))
                    unit_value_list.append(round(unit_price, 2))
                    # print (f"Order sold, quantity {quatity}, Value {value} Matic, unit price {unit_price} Matic")
            # st.session_state.data_list.insert(0, new_data)  # insert new data at the top
                
            # If data_list exceeds 15 rows, remove the oldest row
            # if len(st.session_state.data_list) > 15:
                # st.session_state.data_list.pop(-1)
            new_data = new_data[:15]
            # Displaying the data
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                for data in time_list:
                    # current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    utc_time = datetime.fromtimestamp(float(data), timezone.utc)
                    utc_plus_8 = utc_time + timedelta(hours=8)

                    utc_plus_8 = utc_plus_8.strftime("%m-%d %H:%M:%S")
                    st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px;white-space: nowrap;'>{utc_plus_8}</div>", unsafe_allow_html=True)
            with col2:
                for data in status_list:
                    if data == "1":
                        st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px; background-color: green; color: white;white-space: nowrap;'>SOLD</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px; background-color: red; color: white;white-space: nowrap;'>FAIL</div>", unsafe_allow_html=True)
                    # if status
                    # st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px;white-space: nowrap;'>{data} BTC</div>", unsafe_allow_html=True)
            with col3:
                for data in quantity_list:
                    st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px;white-space: nowrap;'>{data}</div>", unsafe_allow_html=True)
            with col4:
                for data in value_list:
                    st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px;white-space: nowrap;'>{data} <span style='color: red;'>(${round(data*matic_price,2)})</span></div>", unsafe_allow_html=True)
                    # st.text(data['value'])
            with col5:
                for data in unit_value_list:
                    st.markdown(f"<div style='text-align: center; margin-bottom: 5px; margin-top: 5px;white-space: nowrap;'>{data} <span style='color: red;'>(${round(data*matic_price,2)})</span></div>", unsafe_allow_html=True)
                    # st.text(data['value'])

            
            time.sleep(10)

        # st.write("Produced by 0x0funky: ", "https://twitter.com/0x0funky ")
        # st.write("FT: ", "https://friend.tech/0x0funky")
        # st.write("SocialFi Tracker open for free now, will open for key holders only in the future.")

# st.set_page_config(layout="wide")
st.set_page_config(page_title= "POLS Market Order Tracker", page_icon="./POLS_Tracker.png")

def image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

icon_url = f"data:image/png;base64,{image_to_base64('./POLS_Tracker.png')}"
title_text = "POLS Market Tracker"

st.markdown(f'<img src="{icon_url}" style="vertical-align:middle; display:inline; margin-right:10px; width:40px; height:40px;"> <span style="font-size: 30px; vertical-align:middle;"><strong>{title_text}</strong></span>', unsafe_allow_html=True)


# st.title("NewBitcoinCity Lucky Wheel Sniper")

current_time = datetime.utcnow()
current_time_plus_8 = current_time + timedelta(hours=8)

current_time_plus_8 = current_time_plus_8.strftime("%Y-%m-%d %H:%M:%S %Z%z")
st.write("Last updated (Auto update 10 Second):", current_time_plus_8)

matic_price = get_pol_price()
st.write("Current Matic Price:", matic_price)

st.markdown(f"""
    <div>
        Produced by <a href="https://twitter.com/0x0funky" target="_blank">0xFunky</a>
    </div>
    """, unsafe_allow_html=True)


st.markdown(f"""
    <div>
        歡迎贊助(Any Shit) : 0xF3bb9C5E63e38540d8792ed7E33dB95713f1e55e
    </div>
    """, unsafe_allow_html=True)



st.write('''
<style>
@media (max-width: 600px) {
    [data-testid="block-container"] {
        flex-direction: row !important;
    }
    [data-testid="column"] {
        width: 16% !important;  /* 100% divided by 6 columns */
        flex: 0 0 16% !important;
        min-width: 16% !important;
        font-size: 10px;
    }
    [data-testid="column"] img {
        width: 30px !important;
        height: auto;  /* This ensures the aspect ratio of the image remains unchanged */
        margin-bottom: 10px;
    }
    [data-testid="column"] p {
        font-size: 8px;
        margin-top:-10px;
        margin-bottom: -10px;
        margin-left:-5px;
    }
}
</style>
''', unsafe_allow_html=True)



main_content()


from configs import CONN_STR, KEY
from kaspabook.mexc_orderbook import MEXCOrderbook
from kaspabook.txbit_orderbook import TxbitOrderbook
import pandas as pd
from time import sleep
import os
import sys
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobServiceClient
import schedule


# Define a function that schedules the execution of your function
def schedule_function():
    # Define the minutes at which you want to run the function
    minutes = ["00", "15", "30", "45"]
    print(f'Setting schedule for {minutes}')
    for minute in minutes:
        schedule.every().hour.at(":{}".format(minute)).do(save_orderbook)

def save_orderbook():
    # Instantiate a new BlobServiceClient using a connection string

    blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)

    # Instantiate a new ContainerClient
    container_client = blob_service_client.get_container_client("kaspabook-test")
    try:
        # Create new Container in the Service
        #container_client.create_container()
        now= pd.Timestamp.now(tz='UTC')
        print(f'Triggered a orderbook export at {now}')
        mexc_df = MEXCOrderbook("KAS/USDT").calculate_cumsum_df()
        txbit_df = TxbitOrderbook("KAS/USDT").calculate_cumsum_df()
        folder = now.strftime('%Y-%m-%d')
        filename = now.strftime("%Y-%m-%d_%H_%M")
        local_mexc_filename = "mexc.parquet"
        local_txbit_filename = "txbit.parquet"
    
        mexc_filename = f"MEXC/{folder}/mexc_{filename}.parquet"
        txbit_filename = f"TXBIT/{folder}/txbit_{filename}.parquet"
        mexc_df.to_parquet(local_mexc_filename)
        txbit_df.to_parquet(local_txbit_filename)

        # Instantiate a new BlobClient
        mexc_blob_client = container_client.get_blob_client(mexc_filename)
        txbit_blob_client = container_client.get_blob_client(txbit_filename)

        # Upload content to the Page Blob
        with open(local_mexc_filename, "rb") as data:
            mexc_blob_client.upload_blob(data,overwrite=True )
        print(f'Uploaded for MEXC at {now}')
        with open(local_txbit_filename, "rb") as data:
            txbit_blob_client.upload_blob(data,overwrite=True )
        print(f'Uploaded to TXBIT at {now}')
    except Exception as exe:
        print(exe)


if __name__ == "__main__":
    save_orderbook()
    # # Schedule the function to run every 15 minutes
    # schedule_function()

    # # Keep the program running indefinitely
    # while True:
    #     schedule.run_pending()
    #     sleep(1)

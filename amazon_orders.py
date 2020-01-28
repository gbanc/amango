import os
import io
import time
import pandas as pd
import pytz
import psycopg2

from AMWSconnection import MWSConnection
from datetime import datetime, timedelta, timezone
from django.db import connection
from io import StringIO

from sqlalchemy import create_engine
from models import *

from profile.models import Profile

def ingest_report(seller_profile):

    amconn = MWSConnection(os.environ['MWS_ACCESS_KEY'], os.environ['MWS_SECRET_KEY'])

    amconn.MWSAuthToken = seller_profile.mwsAuthToken
    amconn.SellerId = seller_profile.seller_id
    amconn.Merchant = seller_profile.seller_id
    amconn.MarketplaceId = seller_profile.marketplace_id

    #reqest report

    date1 = datetime.now().replace(tzinfo=pytz.utc)
    date_today = date1.strftime("%Y-%m-%dT23:59:00+00:00")
    #date_today = ldate.strftime("%Y-%m-%dT%H:%M:00+00:00")

    date_29_days_ago= datetime.now().replace(tzinfo=pytz.utc) - timedelta(days=29)
    days_ago = date_29_days_ago.strftime("%Y-%m-%dT23:59:00+00:00")

    kwargs = {"StartDate": days_ago, "EndDate": date_today}
    req_report = amconn.request_report(ReportType='_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_', **kwargs)
    req_id = req_report.RequestReportResult.ReportRequestInfo.ReportRequestId

    time.sleep(30)

    #get report

    rep_id=None
    while rep_id is None:
        time.sleep(10)
        listreports = amconn.get_report_list()
        for report in listreports.GetReportListResult.ReportInfo:
            if report.ReportRequestId == req_id:
                rep_id = report.ReportId

    #z = listreports.GetReportListResult.ReportInfo[0].ReportId

    x = amconn.get_report(ReportId=rep_id)

    b = StringIO(x.decode('ISO-8859-1'))
    df = pd.read_csv(b, sep="\t")


    df['purchase-date'] = pd.to_datetime(df['purchase-date']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df['last-updated-date'] = pd.to_datetime(df['last-updated-date']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df.fillna(0, inplace=True)

    #show duplicated
    #df3[~df.duplicated(subset=['amazon-order-id])]
    #df.index = pd.to_datetime(df['purchase-date'], utc=True)
    #df.index = df.index.tz_localize('UTC').tz_convert('US/Pacific')

    #latestentry = cur.execute('SELECT * FROM amazon_sales_data ORDER BY date DESC LIMIT 1;')
    #latestentry = AmazonSalesData.query.order_by("-id").first()
    #ldate = pd.to_datetime(latestentry.date)
    #mask = (df_db['purchase-date'].dt.floor('d') > ldate) 
    #dmask = df_db.loc[mask]

    cur = connection.cursor()

    output = io.StringIO()

    df.to_csv(
        output,
        sep='\t',
        header=False,
        index=False)

    output.seek(0)

    contents = output.getvalue()

    cur.copy_from(
        output, 
        'amazon_orders',
        null="",
        columns=(
            "amazon_order_id",
            "merchant_order_id",
            "purchase_date",
            "last_updated",
            "order_status",
            "fulfillment_channel", 
            "sales_channel", 
            "order_channel", 
            "url", 
            "ship_service_level", 
            "product_name", 
            "sku", 
            "asin", 
            "number_of_items", 
            "item_status", 
            "quantity", 
            "currency", 
            "item_price", 
            "item_tax", 
            "shipping_price", 
            "shipping_tax", 
            "gift_wrap_price", 
            "gift_wrap_tax", 
            "item_promotion_discount", 
            "ship_promotion_discount", 
            "ship_city", 
            "ship_state", 
            "ship_postal_code", 
            "ship_country", 
            "promotion_ids", 
            "payment_method_details", 
            "is_business_order", 
            "purchase_order_number", 
            "price_designation"
            )
        ) # null values become "


    cur.execute(
        "DELETE FROM amazon_orders a" \
            "USING (SELECT MIN(ctid) as ctid, amazon_order_id" \ 
            "FROM amazon_orders" \ 
            "GROUP BY amazon_order_id" \ 
            "HAVING COUNT(*) > 1) b" \ 
            "WHERE a.amazon_order_id = b.amazon_order_id" \ 
            "AND a.ctid <> b.ctid"
            )
    connection.commit()
    connection.close()


    print('amazon complete')


    #if __name__ == '__main__':

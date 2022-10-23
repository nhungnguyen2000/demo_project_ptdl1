# Install dash: pip install dash
# Học thêm tại: https://dash.plotly.com/

# Install bootstrap: import dash_bootstrap_components as dbc
# Học thêm tại: https://dash-bootstrap-components.opensource.faculty.ai/
# Học thêm bootstrap tại: https://getbootstrap.com/docs/5.0/components/card/

# Run this app with `python official_lab_v2.py` and

# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY

from turtle import width
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

import dash_bootstrap_components as dbc

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./iuh-19472811-77985-firebase-adminsdk-oyfmm-b17e62624f.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-19472811').where(u'DEALSIZE', u'==', 'Large').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
df["SALES"] = df["SALES"].astype("float")
df["QUANTITYORDERED"] = df["QUANTITYORDERED"].astype("float")
df["PRICEEACH"] = df["PRICEEACH"].astype("float")

df["LoiNhuan"] = df["SALES"] - (df["QUANTITYORDERED"] * df["PRICEEACH"])
dfGroup = df.groupby("YEAR_ID").sum()
dfGroup["YEAR_ID"] = dfGroup.index

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = "Finance Data Analysis"
figDoanhSoBanHangTheoNam = px.bar(dfGroup, x='YEAR_ID', y="SALES",
                                  title='Doanh số bán hàng theo năm', color='YEAR_ID',
                                  labels={'YEAR_ID': 'Từ năm 2003, 2004 và 2005', 'SALES': 'Doanh số'})
figLoiNhuanBanHangTheoNam = px.line(dfGroup, x='YEAR_ID', y="LoiNhuan",
                                    title='Lợi nhuận bán hàng theo năm',
                                    labels={
                                        'YEAR_ID':'Năm', 'LoiNhuan':'Lợi nhuận'
                                    }
                                    
                                    )


figTileDoanhSo = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
                             color='SALES',
                             labels={'parent': 'Năm', 'id': 'Year / month','SALES': 'Doanh số'},
                             title='Tỉ lệ đóng góp của doanh số theo từng danh mục trong từng năm')

figTileLoiNhuan = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='LoiNhuan',
                              color='LoiNhuan',
                              labels={'parent': 'Năm', 'id': 'Year / month', 'LoiNhuan': 'Lợi nhuận'},
                              title='Tỉ lệ đóng góp của lợi nhuận theo từng danh mục trong từng năm')
            
doanhso = round(df["SALES"].sum(), 2) 
loinhuan = round(df['LoiNhuan'].sum(), 2)

topDoanhSo = df.groupby('CATEGORY').sum()['SALES'].max()
topLoiNhuan = round(df.groupby('CATEGORY').sum()['LoiNhuan'].max(), 2)

app.layout = dbc.Container(
    # html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children =[
                        html.H3(
                            children="XÂY DỰNG DANH MỤC SẢN PHẨM TIỀM NĂNG" 
                        )
                    ], 
                    className="col-6"   
                ),
                html.Div(
                    children =[
                        html.H3(
                            children="IUH-DHHTTT16A-19472811-NGUYỄN HỒNG NHUNG"
                        )   
                    ]
                    , className="col-6"   
                )
               
            ], 
            className="row bg-primary rounded pt-2 mb-4"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H6(
                                    children="DOANH SỐ SALE", className="font-weight-bold"
                                ),
                                html.P(
                                    children=[doanhso, "$"]
                                )
                            ], className="card p-2"
                        )
                    ]   , className="col-lg-3 col-md-6 mb-4"   
                ),  
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H6(
                                    children="LỢI NHUẬN"
                                ),
                                html.P(
                                    children=[loinhuan, "$"]
                                )
                            ], className="card p-2"
                        )
                    ], className="col-lg-3 col-md-6 mb-4"       
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H6(
                                    children="TOP DOANH SỐ"
                                ),
                                html.P(
                                    children=[topDoanhSo, "$"]
                                )
                            ], className="card p-2"
                        )
                    ]   , className="col-lg-3 col-md-6 mb-4"    
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H6(
                                    children="TOP LỢI NHUẬN"
                                ),
                                html.P(
                                    children=[topLoiNhuan, "$"]
                                )
                            ], className="card p-2"
                        )
                    ], className="col-lg-3 col-md-6 mb-4"  
                )

            ],
            className="row mt-4 ",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                        children=dcc.Graph(
                        id='figDoanhSoBanHangTheoNam-graph',
                        figure=figDoanhSoBanHangTheoNam),
                        className="card"
                    )
                    ],
                    className="col-lg-6 col-md-6 mb-4"
                ),
                html.Div(
                    children=[
                        html.Div(
                        children=dcc.Graph(
                        id='figTileDoanhSo-graph',
                        figure=figTileDoanhSo),
                        className="card"
                    )
                    ],
                    className="col-lg-6 col-md-6 mb-4"
                ),
                html.Div(
                    children=[
                        html.Div(
                        children=dcc.Graph(
                        id='figLoiNhuanBanHangTheoNam-graph',
                        figure=figLoiNhuanBanHangTheoNam),
                        className="card"
                    )
                    ],
                    className="col-lg-6 col-md-6 mb-4"
                ),
                html.Div(
                    children=[
                        html.Div(
                        children=dcc.Graph(
                        id='figTileLoiNhuan-graph',
                        figure=figTileLoiNhuan),
                        className="card"
                    )
                    ],
                    className="col-lg-6 col-md-6 mb-4"
                )
               
            ], className="row")
    ]
    # )
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
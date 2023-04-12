import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots #2軸


st.set_page_config(page_title='merket_condition')
st.markdown('### 市況情報')

def chakkou():
    st.markdown('#### 着工数')
    #建築着工統計調査 住宅着工統計/都道府県別、工事別、利用関係別／戸数・件数、床面積/持家分譲/新設+その他
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdTab=18&cdCat01=12%2C15&cdCat02=12%2C13&appId=&lang=J&statsDataId=0003114535&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    #csvファイルの取得＋df化
    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    #metaデータと本データの切れ目に'VALUE'がある
    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    #カラムの絞込み
    df_val2 = df_val[['地域', '時間軸(月次)', 'value']]

    #data型の変換
    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('int')

    

    # 地域選択
    with st.form("chakkou"):
        areas = st.multiselect(
        '地域選択 ※複数選択可',
        df_val2['地域'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:
        df_selected = df_val2[df_val2['地域'].isin(areas)]

        #'時間軸(月次)'でgroupby
        sum_selected = df_selected.groupby('時間軸(月次)')['value'].sum()

        #*******可視化
        # #*******月単位
        # #グラフを描くときの土台となるオブジェクト
        # fig = go.Figure()
        # #今期のグラフの追加

        # fig.add_trace(
        #     go.Scatter(
        #         x=sum_selected.index,
        #         y=sum_selected,
        #         # mode = 'lines+markers+text', #値表示
        #         # text=round(df3['合計']),
        #         # textposition="top center",
        #         name='着工数'
        #         )
        # )

        # #レイアウト設定     
        # fig.update_layout(
        #     title='着工数/月単位',
        #     showlegend=True #凡例表示
        # )
        # st.plotly_chart(fig, use_container_width=True) 
        #     #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

        #*******年単位
        df_selected['year'] = df_selected['時間軸(月次)'].apply(lambda x: x.year)
        sum_year = df_selected.groupby('year')['value'].sum()

        #グラフを描くときの土台となるオブジェクト
        fig3 = go.Figure()
        #今期のグラフの追加

        fig3.add_trace(
            go.Scatter(
                x=sum_year.index,
                y=sum_year,
                mode = 'lines+markers+text', #値表示
                text=round(sum_year),
                textposition="top center",
                name='着工数'
                )
        )

        #レイアウト設定     
        fig3.update_layout(
            title='着工数/年単位',
            showlegend=True #凡例表示
        )
        st.plotly_chart(fig3, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

        #月単位　直近1年
        #グラフを描くときの土台となるオブジェクト
        fig2 = go.Figure()
        #今期のグラフの追加

        fig2.add_trace(
            go.Scatter(
                x=sum_selected[-13:].index,
                y=sum_selected[-13:],
                mode = 'lines+markers+text', #値表示
                text=sum_selected[-13:],
                textposition="top center",
                name='着工数'
                )
        )

        #レイアウト設定     
        fig2.update_layout(
            title='着工数/月単位/直近1年',
            showlegend=True #凡例表示
        )
        st.plotly_chart(fig2, use_container_width=True) 
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    
            
def keiki():

    #******************景気ウォッチャー調査
    st.markdown('#### 景気ウォッチャー調査')
    st.caption('0から100/50が境目') 
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?appId=&lang=J&statsDataId=0003348424&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照
    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    #dfの分割　後半が本データ
    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['地域', '時間軸(月次)', 'value']]

    df_val2['時間軸(月次)'] = pd.to_datetime(df_val2['時間軸(月次)'], format='%Y年%m月')
    df_val2['value'] = df_val2['value'].astype('float')

     # 地域選択
    with st.form("keiki"):
        area = st.selectbox(
        '地域選択',
        df_val2['地域'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:
        df_selected = df_val2[df_val2['地域']==area]


        #*******可視化
        #*****景気ウオッチャー調査　月
        #グラフを描くときの土台となるオブジェクト
        fig4 = go.Figure()
        #今期のグラフの追加

        fig4.add_trace(
            go.Scatter(
                x=df_selected['時間軸(月次)'][:37],
                y=df_selected['value'][:37],
                # mode = 'lines+markers+text', #値表示
                # text=round(df3['合計']),
                # textposition="top center",
                name='指数'
                )
        )

        #レイアウト設定     
        fig4.update_layout(
            title='景気ウオッチャー調査/月単位/過去3年',
            showlegend=True #凡例表示
        )
        st.plotly_chart(fig4, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

    #     #*****景気ウオッチャー調査　月/直近1年
        #グラフを描くときの土台となるオブジェクト
        fig5 = go.Figure()
        #今期のグラフの追加

        fig5.add_trace(
            go.Scatter(
                x=df_selected['時間軸(月次)'][:13], #新しい順に並んでいる
                y=df_selected['value'][:13],
                mode = 'lines+markers+text', #値表示
                text=df_selected['value'][:13],
                textposition="top center",
                name='指数'
                )
        )

        #レイアウト設定     
        fig5.update_layout(
            title='景気ウオッチャー調査/月/直近1年',
            showlegend=True #凡例表示
        )
        st.plotly_chart(fig5, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅

#     #********************************消費者物価指数
def bukka():
    st.markdown('#### 消費者物価指数')
    st.caption('基準2020年')
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=0001&cdTab=1&appId=&lang=J&statsDataId=0003427113&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_val2 = df_val[['地域（2020年基準）', '時間軸（年・月）', 'value']]

     # 地域選択
    with st.form("bukka"):
        area = st.selectbox(
        '地域選択',
        df_val2['地域（2020年基準）'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:

        #年集計行の削除
        for idx, val in enumerate(df_val2['時間軸（年・月）']):
            if '月' not in val:
                df_val2.drop(index=idx, axis=0, inplace=True)

        df_val2['時間軸（年・月）'] = pd.to_datetime(df_val2['時間軸（年・月）'], format='%Y年%m月')
        df_val2['value'] = df_val2['value'].astype('float') 

        df_selected = df_val2[df_val2['地域（2020年基準）']==area]

        #******************可視化
        # *********消費者物価指数 月
        #グラフを描くときの土台となるオブジェクト
        fig6 = go.Figure()
        #今期のグラフの追加

        fig6.add_trace(
            go.Scatter(
                x=df_selected['時間軸（年・月）'],
                y=df_selected['value'],
                # mode = 'lines+markers+text', #値表示
                # text=round(df3['合計']),
                # textposition="top center",
                name='指数'
                )
        )

        #レイアウト設定     
        fig6.update_layout(
            title='消費者物価指数/月単位 2020年基準',
            showlegend=True #凡例表示
        )
        st.plotly_chart(fig6, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

        # *********消費者物価指数 月/直近1年
        #グラフを描くときの土台となるオブジェクト
        fig7 = go.Figure()
        #今期のグラフの追加

        fig7.add_trace(
            go.Scatter(
                x=df_selected['時間軸（年・月）'][:13],
                y=df_selected['value'][:13],
                mode = 'lines+markers+text', #値表示
                text=df_selected['value'][:13],
                textposition="top center",
                name='指数'
                )
        )

        #レイアウト設定     
        fig7.update_layout(
            title='消費者物価指数/月/直近1年',
            showlegend=True #凡例表示
        )
        st.plotly_chart(fig7, use_container_width=True) 
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅 

#     #*********************************家計調査
def kakei():
    st.markdown('#### 家計調査')
    st.caption('二人以上世帯/全国約9千世帯')
    #urlの作成
    url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData?cdCat01=040130030%2C090410001%2C090420000&cdCat02=03&appId=&lang=J&statsDataId=0003343671&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    appId = st.secrets['PRIVATE']['appId'] #.streamlit\secret.tmolから参照

    url_sp = url.split("appId=")
    url = url_sp[0] + "appId=" + appId + url_sp[1]

    # DataFrameの列名を「0,1,2, … ,99」と指定する
    df = pd.read_csv(url, names=range(50))

    idx = df[df[0]=="VALUE"].index[0] #tapleで返ってくる為[0]指定
    df_val = pd.DataFrame(df[idx+2:].values, columns=df.iloc[idx+1].values) # 27行目列名 28行目以降data

    #空欄列の削除
    df_val = df_val.dropna(axis=1, how="all")

    df_travel2 = df_val[df_val['品目分類（2020年改定）'].isin(['9.4.1 宿泊料', '9.4.2 パック旅行費'])]
    df_table2 = df_val[df_val['品目分類（2020年改定）']=='482 テーブル・ソファー']

    df_travel2 = df_travel2[['地域区分', '時間軸（月次）', 'value']]
    df_table2 = df_table2[['地域区分', '時間軸（月次）', 'value']]

    df_travel2['時間軸（月次）'] = pd.to_datetime(df_travel2['時間軸（月次）'], format='%Y年%m月')
    df_travel2['value'] = df_travel2['value'].apply(lambda x: 0 if x=='-' else x)
    df_travel2['value'] = df_travel2['value'].astype('int')
    df_table2['時間軸（月次）'] = pd.to_datetime(df_table2['時間軸（月次）'], format='%Y年%m月')
    df_table2['value'] = df_table2['value'].apply(lambda x: 0 if x=='-' else x)
    df_table2['value'] = df_table2['value'].astype('int')

     # 地域選択
    with st.form("kakei"):
        area = st.selectbox(
        '地域選択',
        df_travel2['地域区分'].unique())

        submitted = st.form_submit_button("決定")

    if submitted:
        df_travel3 = df_travel2[df_travel2['地域区分']==area]
        #***************可視化
        #*******旅行
        s_travel = df_travel3.groupby('時間軸（月次）')['value'].sum()

        #グラフを描くときの土台となるオブジェクト
        fig8 = go.Figure()
        #今期のグラフの追加

        fig8.add_trace(
            go.Scatter(
                x=s_travel.index,
                y=s_travel,
                # mode = 'lines+markers+text', #値表示
                # text=round(df3['合計']),
                # textposition="top center",
                name='旅行'
                )
        )

        #レイアウト設定     
        fig8.update_layout(
            title='旅行/月単位',
            showlegend=True #凡例表示
        )

        st.plotly_chart(fig8, use_container_width=True) 

        #*******旅行　直近1年
        #グラフを描くときの土台となるオブジェクト
        fig9 = go.Figure()
        #今期のグラフの追加

        fig9.add_trace(
            go.Scatter(
                x=s_travel.index[-13:],
                y=s_travel[-13:],
                mode = 'lines+markers+text', #値表示
                text=s_travel[-13:],
                textposition="top center",
                name='旅行'
                )
        )

        #レイアウト設定     
        fig9.update_layout(
            title='旅行/直近1年',
            showlegend=True #凡例表示
        )

        st.plotly_chart(fig9, use_container_width=True) 

           #*******家具
        df_table3 = df_table2[df_table2['地域区分']==area]
        s_table = df_table3.groupby('時間軸（月次）')['value'].sum()

        #グラフを描くときの土台となるオブジェクト
        fig8 = go.Figure()
        #今期のグラフの追加

        fig8.add_trace(
            go.Scatter(
                x=s_travel.index,
                y=s_travel,
                # mode = 'lines+markers+text', #値表示
                # text=round(df3['合計']),
                # textposition="top center",
                name='テーブル/ソファ'
                )
        )

        #レイアウト設定     
        fig8.update_layout(
            title='テーブル/ソファ/月単位',
            showlegend=True #凡例表示
        )

        st.plotly_chart(fig8, use_container_width=True) 

        #*******旅行　直近1年
        #グラフを描くときの土台となるオブジェクト
        fig9 = go.Figure()
        #今期のグラフの追加

        fig9.add_trace(
            go.Scatter(
                x=s_table.index[-13:],
                y=s_table[-13:],
                mode = 'lines+markers+text', #値表示
                text=s_table[-13:],
                textposition="top center",
                name='テーブル/ソファ'
                )
        )

        #レイアウト設定     
        fig9.update_layout(
            title='テーブル/ソファ/直近1年',
            showlegend=True #凡例表示
        )

        st.plotly_chart(fig9, use_container_width=True) 



def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '着工数': chakkou,
        '景気ウォッチャー調査': keiki,
        '消費者物価指数': bukka,
        '家計調査': kakei
       
    }
    selected_app_name = st.sidebar.selectbox(label='分析項目の選択',
                                             options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('サイドバーから分析項目を選択してください')
        st.stop()

    link = '[home](http://linkpagetest.s3-website-ap-northeast-1.amazonaws.com/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.caption('homeに戻る')    

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()

if __name__ == '__main__':
    main()
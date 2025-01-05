
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END 
from typing import Any

import a80_109_PDFを1ページごとにテキスト化 as pdf2text
import a80_115_テキストを整えて集約 as text_format
import a80_116_ヘッダーフッターを選択 as hdft_sentaku 
import a80_131_見出しの抽出 as midashi 
import a80_135_見出しの選択 as midashi_sentaku
# import a80_032_チャンク分割 as chunk_bunkatu
# import a80_041_df_allをDBへ登録 as emb

# エージェントの状態を表すデータモデル
class EmbeddingState(BaseModel):
    file_pdf : str = Field(..., description="PDFファイルのパス")
    page_sta : int = Field(..., description="開始ページ")
    page_end : int = Field(..., description="終了ページ")
    folder_temp : str = Field(..., description="一時フォルダ")
    folder_db : str = Field(..., description="DBフォルダ")
    jokyo : str = Field(..., description="状況")
    midashi1 : str = Field(..., description="見出しレベル1")
    midashi2 : str = Field(..., description="見出しレベル2")
    midashi3 : str = Field(..., description="見出しレベル3")
    midashi4 : str = Field(..., description="見出しレベル4")
    kajo1    : str = Field(..., description="箇条書きレベル1")
    kajo2    : str = Field(..., description="箇条書きレベル2")
    kajo3    : str = Field(..., description="箇条書きレベル3")
    combined_text : str = Field(..., description="結合テキスト")
    df_all : Any = Field(..., description="チャンクデータの pl.Dataframe ") 
    HeaderFooter1 : Any = Field(..., description="ヘッダー・フッターの正規表現 エージェント1")
    HeaderFooter2 : Any = Field(..., description="ヘッダー・フッターの正規表現 エージェント2")
    HeaderFooter3 : Any = Field(..., description="ヘッダー・フッターの正規表現 エージェント3")
    HeaderFooter_sentaku : Any = Field(..., description="ヘッダー・フッターの正規表現 選択したもの")
    HeaderFooter_bango : int = Field(..., description="ヘッダー・フッターの正規表現 選択した番号") 
    HeaderFooter_riyu : str = Field(..., description="ヘッダー・フッターの正規表現 選択した理由")
    midashi_kajo_agent1 : Any = Field(..., description="見出し・箇条書きのテキスト エージェント1")
    midashi_kajo_agent2 : Any = Field(..., description="見出し・箇条書きのテキスト エージェント2")
    midashi_kajo_agent3 : Any = Field(..., description="見出し・箇条書きのテキスト エージェント3")
    midashi_kajo_sentaku : Any = Field(..., description="見出し・箇条書きのテキスト 選択したもの")
    midashi_kajo_sentaku_bango : int = Field(..., description="見出し・箇条書きのテキスト 選択した番号")
    midashi_kajo_sentaku_riyu : str = Field(..., description="見出し・箇条書きのテキスト 選択した理由")


# エージェントの定義
class EmbeddingAgent:
    # エージェントの初期化
    def __init__(self, llm: AzureChatOpenAI, llm_emb: AzureOpenAIEmbeddings, llm_temperature: AzureChatOpenAI):
        self.pdf2text_ = pdf2text.Pdf2Text(llm)
        self.text_format_1 = text_format.HeaderFootersGenerator(llm)
        self.text_format_2 = text_format.HeaderFootersGenerator(llm)
        self.text_format_3 = text_format.HeaderFootersGenerator(llm)
        self.hdft_sentaku_ = hdft_sentaku.HeaderFootersSentaku(llm)
        self.midashi_1 = midashi.MidashiGenerator(llm) 
        self.midashi_2 = midashi.MidashiGenerator(llm_temperature) 
        self.midashi_3 = midashi.MidashiGenerator(llm_temperature) 
        self.midashi_sentaku = midashi_sentaku.MidashiSentaku(llm)
        # self.chunk_bunkatu_ = chunk_bunkatu.Chunk_bunkatu()
        # self.emb_ = emb.Embedding_jikko(llm_emb)
        self.graph = self._create_graph()

    # グラフの作成
    def _create_graph(self) -> StateGraph:
        graph = StateGraph(EmbeddingState)
        graph.add_node("node_pdf2text", self.node_pdf2text)
        graph.add_node("node_text_format1", self.node_text_format1)
        graph.add_node("node_text_format2", self.node_text_format2)
        graph.add_node("node_text_format3", self.node_text_format3)
        graph.add_node("node_hdft_sentaku", self.node_hdft_sentaku)
        graph.add_node("node_midashi1", self.node_midashi1)
        graph.add_node("node_midashi2", self.node_midashi2)
        graph.add_node("node_midashi3", self.node_midashi3)
        graph.add_node("node_midashi_sentaku", self.node_midashi_sentaku)
        # graph.add_node("node_chunk_bunkatu", self.node_chunk_bunkatu)
        # graph.add_node("node_emb", self.node_emb)

        graph.set_entry_point("node_pdf2text")
        graph.add_edge("node_pdf2text", "node_text_format1")
        graph.add_edge("node_text_format1", "node_text_format2")
        graph.add_edge("node_text_format2", "node_text_format3")
        graph.add_edge("node_text_format3", "node_hdft_sentaku")
        # graph.add_conditional_edges("node_text_format",  # 条件によって遷移先を変える。見出しが指定されている場合は、見出し抽出をスキップする
        #                              lambda state: state.midashi1 == '',
        #                              {True: "node_midashi", False: "node_chunk_bunkatu"}
        #                             )
        graph.add_edge("node_hdft_sentaku", "node_midashi1")
        graph.add_edge("node_midashi1", "node_midashi2")
        graph.add_edge("node_midashi2", "node_midashi3")
        graph.add_edge("node_midashi3", "node_midashi_sentaku")
        # graph.add_edge("node_midashi_sentaku", "node_chunk_bunkatu")
        # graph.add_edge("node_chunk_bunkatu", "node_emb")
        graph.add_edge("node_midashi_sentaku", END)
        return graph.compile()        

    # ノードの定義
    def node_pdf2text(self, state:EmbeddingState) -> dict[str, Any]:
        folder_temp: str = self.pdf2text_.run(state.file_pdf, state.page_sta, state.page_end)
        return { 'jokyo':'1','folder_temp':folder_temp  }

    def node_text_format1(self, state:EmbeddingState) -> dict[str, Any]:
        HeaderFooter  = self.text_format_1.run(state.folder_temp, 1)
        return { 'jokyo':'2'
                ,'HeaderFooter1':HeaderFooter
                }
    def node_text_format2(self, state:EmbeddingState) -> dict[str, Any]:
        HeaderFooter  = self.text_format_2.run(state.folder_temp, 2)
        return { 'jokyo':'2'
                ,'HeaderFooter2':HeaderFooter
                }
    def node_text_format3(self, state:EmbeddingState) -> dict[str, Any]:
        HeaderFooter  = self.text_format_3.run(state.folder_temp, 3)
        return { 'jokyo':'2'
                ,'HeaderFooter3':HeaderFooter
                }
    def node_hdft_sentaku(self, state:EmbeddingState) -> dict[str, Any]:
        HeaderFooter_sentaku, HeaderFooter_bango, HeaderFooter_riyu ,combined_text= self.hdft_sentaku_.run(state.folder_temp, state.HeaderFooter1, state.HeaderFooter2, state.HeaderFooter3)
        return { 'jokyo':'2'
                ,'HeaderFooter_sentaku':HeaderFooter_sentaku
                ,'HeaderFooter_bango':HeaderFooter_bango
                ,'HeaderFooter_riyu':HeaderFooter_riyu
                ,'combined_text':combined_text
                }

    def node_midashi1(self, state:EmbeddingState) -> dict[str, Any]:
        midashi_kajo_agent1  = self.midashi_1.run(state.combined_text, state.folder_temp, 1)
        return { 'jokyo':'3' 
                ,'midashi_kajo_agent1':midashi_kajo_agent1
                 }

    def node_midashi2(self, state:EmbeddingState) -> dict[str, Any]:
        midashi_kajo_agent2  = self.midashi_2.run(state.combined_text, state.folder_temp, 2)
        return { 'jokyo':'3' 
                ,'midashi_kajo_agent2':midashi_kajo_agent2
                 }

    def node_midashi3(self, state:EmbeddingState) -> dict[str, Any]:
        midashi_kajo_agent3  = self.midashi_3.run(state.combined_text, state.folder_temp, 3)
        return { 'jokyo':'3' 
                ,'midashi_kajo_agent3':midashi_kajo_agent3
                 }

    def node_midashi_sentaku(self, state:EmbeddingState) -> dict[str, Any]:
        midashi_kajo_sentaku , midashi_kajo_sentaku_bango, midashi_kajo_sentaku_riyu  = self.midashi_sentaku.run(state.combined_text, state.folder_temp, state.midashi_kajo_agent1, state.midashi_kajo_agent2, state.midashi_kajo_agent3)
        return { 'jokyo':'3'
                ,'midashi_kajo_sentaku':midashi_kajo_sentaku
                ,'midashi_kajo_sentaku_bango':midashi_kajo_sentaku_bango
                ,'midashi_kajo_sentaku_riyu':midashi_kajo_sentaku_riyu
                }

    # def node_chunk_bunkatu(self, state:EmbeddingState) -> dict[str, Any]:
    #     df_all = self.chunk_bunkatu_.run(state.combined_text, state.folder_temp ,state.midashi1, state.midashi2, state.midashi3, state.midashi4, state.kajo1, state.kajo2, state.kajo3)
    #     return { 'jokyo':'4', 'df_all':df_all  }

    # def node_emb(self, state:EmbeddingState) -> dict[str, Any]:
    #     folder_db = self.emb_.run(state.folder_temp, state.df_all)
    #     return { 'jokyo':'5', 'folder_db':folder_db  }

    # エージェントの実行
    def run(self, state:EmbeddingState):
        final_state = self.graph.invoke(state)
        return final_state


if __name__ == "__main__":
    import time
    start_time = time.perf_counter()

    # 設定ファイルから LLM接続情報 を読み込む
    import json
    with open('a80.json', 'r', encoding='utf-8') as file:
        dict_ = json.load(file)
    deployment_name=dict_['deployment_name']
    azure_endpoint=dict_['azure_endpoint']
    openai_api_key=dict_['openai_api_key']
    openai_api_version=dict_['openai_api_version']
    emb_azure_deployment=dict_['emb_azure_deployment']
    emb_azure_endpoint=dict_['emb_azure_endpoint']
    emb_openai_api_key=dict_['emb_openai_api_key']
    emb_openai_api_version=dict_['emb_openai_api_version']

    # LLM の初期化
    llm     = AzureChatOpenAI(  deployment_name=deployment_name, openai_api_version=openai_api_version, openai_api_key=openai_api_key, azure_endpoint=azure_endpoint, temperature=0 )
    llm_temperature     = AzureChatOpenAI(  deployment_name=deployment_name, openai_api_version=openai_api_version, openai_api_key=openai_api_key, azure_endpoint=azure_endpoint, temperature=0.9 )
    llm_emb = AzureOpenAIEmbeddings( azure_deployment=emb_azure_deployment, openai_api_version=emb_openai_api_version, openai_api_key=emb_openai_api_key, azure_endpoint=emb_azure_endpoint ) 

    list_pdfs=['a80_settei_kana.tsv','a80_settei_kk.tsv','a80_settei_kk_kai.tsv']
    for pdf_file in list_pdfs:


        # 設定ファイルから初期状態データを辞書に読み込む
        import polars as pl
        df1 = pl.read_csv(pdf_file,separator='\t')
        dict1 = df1.to_dict(as_series=False)
        dict2 = {k: v for k, v in dict1.items()}
        dict_settei = dict(zip(dict2['key'], dict2['value']))

        # 初期状態データを変数にセット
        file_pdf = dict_settei['file_pdf']
        page_sta = int(dict_settei['page_sta'])
        # page_end = int(dict_settei['page_end'])
        # midashi1 = dict_settei['midashi1']
        # midashi2 = dict_settei['midashi2']
        # midashi3 = dict_settei['midashi3']
        # midashi4 = dict_settei['midashi4']
        # kajo1 = dict_settei['kajo1']
        # kajo2 = dict_settei['kajo2']
        # kajo3 = dict_settei['kajo3']
        # HeaderFooter1 = dict_settei['HeaderFooter1']
        # HeaderFooter2 = dict_settei['HeaderFooter2']
        # HeaderFooter3 = dict_settei['HeaderFooter3']

        # 初期状態の設定
        state = EmbeddingState(
            file_pdf = file_pdf,
            page_sta = page_sta,
            page_end = 999,
            folder_temp = '',
            folder_db   = '',
            jokyo = '0',
            combined_text = '',
            midashi1 = '',
            midashi2 = '',
            midashi3 = '',
            midashi4 = '',
            kajo1 = '',
            kajo2 = '',
            kajo3 = '',
            df_all= '',
            HeaderFooter1 = ['','','' ] ,
            HeaderFooter2 = ['','','' ] ,
            HeaderFooter3 = ['','','' ] ,
            HeaderFooter_sentaku = '',
            HeaderFooter_bango = 0 ,
            HeaderFooter_riyu = '',
            midashi_kajo_agent1 = '',
            midashi_kajo_agent2 = '',
            midashi_kajo_agent3 = '',
            midashi_kajo_sentaku = '',
            midashi_kajo_sentaku_bango = 0,
            midashi_kajo_sentaku_riyu = ''

        )

        print(state)

        # エージェントの初期化
        agent = EmbeddingAgent(llm=llm, llm_emb=llm_emb , llm_temperature=llm_temperature)

        # エージェントの実行
        final_state = agent.run(state)


        # 結果の表示
        import datetime
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y%m%d_%H%M%S")
        with open('a80_pre_' + formatted_date +'.txt', 'w') as f:
            print('---------------------------------------------------------------------------------------')
            print('tmpフォルダ: ',final_state['folder_temp'], file=f)
            print('PDFファイルのパス: ',final_state['file_pdf'], file=f)
            print('開始ページ: ',final_state['page_sta'], file=f)
            print('終了ページ: ',final_state['page_end'], file=f)
            print('見出し1   : ',final_state['midashi_kajo_sentaku'][0], file=f)
            print('見出し2   : ',final_state['midashi_kajo_sentaku'][1], file=f)
            print('見出し3   : ',final_state['midashi_kajo_sentaku'][2], file=f)
            print('見出し4   : ',final_state['midashi_kajo_sentaku'][3], file=f)
            print('箇条書き1 : ',final_state['midashi_kajo_sentaku'][4], file=f)
            print('箇条書き2 : ',final_state['midashi_kajo_sentaku'][5], file=f)
            print('箇条書き3 : ',final_state['midashi_kajo_sentaku'][6], file=f)
            for HeaderFooter in final_state['HeaderFooter_sentaku']:
                print('ﾍｯﾀﾞ-ﾌｯﾀ- : ', HeaderFooter, file=f)

    print(f'end!  開始から{time.perf_counter() - start_time :.2f}秒 ')




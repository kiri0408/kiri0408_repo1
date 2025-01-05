
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END 
from typing import Any

import a80_009_PDFを1ページごとにテキスト化 as pdf2text
import a80_015_テキストを整えて集約 as text_format
import a80_031_見出しの抽出 as midashi 
import a80_032_チャンク分割 as chunk_bunkatu
import a80_041_df_allをDBへ登録 as emb

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
    HeaderFooter : Any = Field(..., description="ヘッダー・フッターの正規表現")

# エージェントの定義
class EmbeddingAgent:
    # エージェントの初期化
    def __init__(self, llm: AzureChatOpenAI, llm_emb: AzureOpenAIEmbeddings):
        self.pdf2text_ = pdf2text.Pdf2Text(llm)
        self.text_format_ = text_format.HeaderFootersGenerator(llm)
        self.midashi_ = midashi.MidashiGenerator(llm) 
        self.chunk_bunkatu_ = chunk_bunkatu.Chunk_bunkatu()
        self.emb_ = emb.Embedding_jikko(llm_emb)
        self.graph = self._create_graph()

    # グラフの作成
    def _create_graph(self) -> StateGraph:
        graph = StateGraph(EmbeddingState)
        graph.add_node("node_pdf2text", self.node_pdf2text)
        graph.add_node("node_text_format", self.node_text_format)
        graph.add_node("node_midashi", self.node_midashi)
        graph.add_node("node_chunk_bunkatu", self.node_chunk_bunkatu)
        graph.add_node("node_emb", self.node_emb)

        graph.set_entry_point("node_pdf2text")
        graph.add_edge("node_pdf2text", "node_text_format")
        graph.add_conditional_edges("node_text_format",  # 条件によって遷移先を変える。見出しが指定されている場合は、見出し抽出をスキップする
                                     lambda state: state.midashi1 == '',
                                     {True: "node_midashi", False: "node_chunk_bunkatu"}
                                    )
        graph.add_edge("node_midashi", "node_chunk_bunkatu")
        graph.add_edge("node_chunk_bunkatu", "node_emb")
        graph.add_edge("node_emb", END)
        return graph.compile()        

    # ノードの定義
    def node_pdf2text(self, state:EmbeddingState) -> dict[str, Any]:
        folder_temp: str = self.pdf2text_.run(state.file_pdf, state.page_sta, state.page_end)
        return { 'jokyo':'1','folder_temp':folder_temp  }

    def node_text_format(self, state:EmbeddingState) -> dict[str, Any]:
        HeaderFooter , combined_text  = self.text_format_.run(state.folder_temp, state.HeaderFooter)
        return { 'jokyo':'2'
                ,'combined_text':combined_text
                ,'HeaderFooter':HeaderFooter
                }
    
    def node_midashi(self, state:EmbeddingState) -> dict[str, Any]:
        midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3  = self.midashi_.run(state.combined_text, state.folder_temp)
        return { 'jokyo':'3' 
                ,'midashi1':midashi1
                ,'midashi2':midashi2
                ,'midashi3':midashi3
                ,'midashi4':midashi4
                ,'kajo1':kajo1
                ,'kajo2':kajo2
                ,'kajo3':kajo3
                 }
    
    def node_chunk_bunkatu(self, state:EmbeddingState) -> dict[str, Any]:
        df_all = self.chunk_bunkatu_.run(state.combined_text, state.folder_temp ,state.midashi1, state.midashi2, state.midashi3, state.midashi4, state.kajo1, state.kajo2, state.kajo3)
        return { 'jokyo':'4', 'df_all':df_all  }

    def node_emb(self, state:EmbeddingState) -> dict[str, Any]:
        folder_db = self.emb_.run(state.folder_temp, state.df_all)
        return { 'jokyo':'5', 'folder_db':folder_db  }

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
    llm_emb = AzureOpenAIEmbeddings( azure_deployment=emb_azure_deployment, openai_api_version=emb_openai_api_version, openai_api_key=emb_openai_api_key, azure_endpoint=emb_azure_endpoint ) 


    # 設定ファイルから初期状態データを辞書に読み込む
    import polars as pl
    df1 = pl.read_csv('a80_settei_kk.tsv',separator='\t')
    dict1 = df1.to_dict(as_series=False)
    dict2 = {k: v for k, v in dict1.items()}
    dict_settei = dict(zip(dict2['key'], dict2['value']))

    # 初期状態データを変数にセット
    file_pdf = dict_settei['file_pdf']
    page_sta = int(dict_settei['page_sta'])
    page_end = int(dict_settei['page_end'])
    midashi1 = dict_settei['midashi1']
    midashi2 = dict_settei['midashi2']
    midashi3 = dict_settei['midashi3']
    midashi4 = dict_settei['midashi4']
    kajo1 = dict_settei['kajo1']
    kajo2 = dict_settei['kajo2']
    kajo3 = dict_settei['kajo3']
    HeaderFooter1 = dict_settei['HeaderFooter1']
    HeaderFooter2 = dict_settei['HeaderFooter2']
    HeaderFooter3 = dict_settei['HeaderFooter3']

    # 初期状態の設定
    state = EmbeddingState(
        file_pdf = file_pdf,
        page_sta = page_sta,
        page_end = page_end,
        folder_temp = '',
        folder_db   = '',
        jokyo = '0',
        combined_text = '',
        midashi1 = midashi1,
        midashi2 = midashi2,
        midashi3 = midashi3,
        midashi4 = midashi4,
        kajo1 = kajo1,
        kajo2 = kajo2,
        kajo3 = kajo3,
        df_all= '',
        HeaderFooter = [HeaderFooter1, HeaderFooter2, HeaderFooter3] 
    )

    print(state)

    # エージェントの初期化
    agent = EmbeddingAgent(llm=llm, llm_emb=llm_emb)

    # エージェントの実行
    final_state = agent.run(state)

    # 結果の表示
    print('DBフォルダ: ',final_state['folder_db'])
    print('見出し1   : ',final_state['midashi1'])
    print('見出し2   : ',final_state['midashi2'])
    print('見出し3   : ',final_state['midashi3'])
    print('見出し4   : ',final_state['midashi4'])
    print('箇条書き1 : ',final_state['kajo1'])
    print('箇条書き2 : ',final_state['kajo2'])
    print('箇条書き3 : ',final_state['kajo3'])
    for HeaderFooter in final_state['HeaderFooter']:
        print('ﾍｯﾀﾞ-ﾌｯﾀ- : ', HeaderFooter)

    print(f'end!  開始から{time.perf_counter() - start_time :.2f}秒 ')




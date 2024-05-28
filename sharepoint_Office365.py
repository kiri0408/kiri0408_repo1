# https://ensaku1029.com/python-sharepoint-fileupload/

# pip install Office365

from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
import os #絶対パスからファイル名を取得する際に使用します。

site_url = "シェアポイントのURL"


#対象サイトへのアクセス
ctx_auth = AuthenticationContext(site_url)
ctx_auth.acquire_token_for_user(ID,PASSWORD)
ctx = ClientContext(site_url, ctx_auth)

#コンテクスト情報の保存
web = ctx.web
ctx.load(web)
ctx.execute_query()

localfilepath = "アップロードしたいファイルの絶対パス" 
filename = os.path.basename(path)
with open(localfilepath, 'rb') as content_file:
  file_content = content_file.read()

target_folder = ctx.web.get_folder_by_server_relative_url(uploadfolder)

target_file = target_folder.upload_file(name, file_content).execute_query()
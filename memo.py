# https://nets-tip.com/?p=1313
#
# Apache Tomcat の起動と停止
# 起動：「C:{Tomcatインストールディレクトリ}\bin\startup.bat」をダブルクリック
# 停止：「C:{Tomcatインストールディレクトリ}\bin\shutdown.bat」をダブルクリック
#
# Tomcatサービス登録
# C:\tomcat\bin\service.bat install Tomcat9

import os
home_path = os.path.expandvars('%HOMEPATH%')
file_path =  r'C:' + home_path + r'\Desktop\ツール\a.txt'


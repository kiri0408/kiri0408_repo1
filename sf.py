import random

# 1. テキストファイルを読み込み、シャッフルして新たなファイルに保存
def shuffle_text(input_file, shuffled_file, index_file):
    # テキストファイルの読み込み
    with open(input_file, "r", encoding="utf-8") as file:
        original_text = file.read()

    # シャッフルするためのインデックスを作成
    indexes = list(range(len(original_text)))
    random.shuffle(indexes)

    # シャッフルされた文字列を作成
    shuffled_text = ''.join(original_text[i] for i in indexes)

    # シャッフルされた文字列を新しいファイルに保存
    with open(shuffled_file, "w", encoding="utf-8") as file:
        file.write(shuffled_text)

    # シャッフルのインデックスを別ファイルに保存
    with open(index_file, "w", encoding="utf-8") as file:
        file.write(','.join(map(str, indexes)))

    print(f"シャッフルされたテキストが '{shuffled_file}' に保存されました。")
    print(f"シャッフル順のインデックスが '{index_file}' に保存されました。")

# 2. シャッフルされたテキストとインデックスファイルを使って元に戻す
def restore_text(shuffled_file, index_file, restored_file):
    # シャッフルされたテキストファイルの読み込み
    with open(shuffled_file, "r", encoding="utf-8") as file:
        shuffled_text = file.read()

    # インデックスファイルの読み込み
    with open(index_file, "r", encoding="utf-8") as file:
        indexes = list(map(int, file.read().split(',')))

    # 元のテキストに戻すためのリストを作成
    original_text_restored = [''] * len(shuffled_text)
    for i, idx in enumerate(indexes):
        original_text_restored[idx] = shuffled_text[i]

    # リストを文字列に戻す
    original_text_restored = ''.join(original_text_restored)

    # 元に戻したテキストを新しいファイルに保存
    with open(restored_file, "w", encoding="utf-8") as file:
        file.write(original_text_restored)

    print(f"元のテキストが '{restored_file}' に復元されました。")

# 使用例
input_file = "tanazan.txt"  # 読み込むテキストファイル
shuffled_file = "sf1t.txt"  # シャッフルされたテキストを保存するファイル
index_file = "sf1i.txt"  # インデックスを保存するファイル
restored_file = "restored_text.txt"  # 復元されたテキストを保存するファイル

# 文字列のシャッフルと保存
# shuffle_text(input_file, shuffled_file, index_file)

# シャッフルを元に戻してテキストを復元
restore_text(shuffled_file, index_file, restored_file)

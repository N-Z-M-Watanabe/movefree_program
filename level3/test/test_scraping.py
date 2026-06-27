# test_scraping.py

import pytest

from normalize import normalize_address

# --- pytestによるテストケース定義 ---
@pytest.mark.parametrize(
    "text_address, expected",
    [
        # 1. 一般的な住所
        (
            "東京都新宿区西新宿2-8-1", 
            ["東京都", "新宿区西新宿二丁目", "8-1"]
        ),
        # 2. 全角数字・ハイフン
        (
            "東京都新宿区西新宿２－８－１", 
            ["東京都", "新宿区西新宿二丁目", "8-1"]
        ),
        # 3. 漢数字の漢数字表記
        (
            "東京都中央区銀座五丁目2番1号", 
            ["東京都", "中央区銀座五丁目", "2-1"]
        ),
        # 4. 住所ではない文字列 (例外発生を想定: 3つ目の要素に入力文字列がそのまま入る)
        (
            "こんにちは、よろしくおねがいします", 
            ["", "", "こんにちは、よろしくおねがいします"]
        ),
        # 5. 都道府県の省略
        (
            "大阪市北区中之島1-3-20", 
            ["大阪府", "大阪市北区中之島一丁目", "3-20"]
        ),
        # 6. 空文字 (最初のガード句: すべて空文字の3要素)
        (
            "", 
            ["", "", ""]
        ),
        # 7. スペースのみ (最初のガード句: すべて空文字の3要素)
        (
            "   ", 
            ["", "", ""]
        ),
    ],
    ids=[
        "1_standard_address",
        "2_full_width_numbers",
        "3_kanji_numbers",
        "4_not_an_address",
        "5_omit_prefecture",
        "6_empty_string",
        "7_spaces_only"
    ]
)

def test_normalize_address(text_address, expected):
    """すべてのケースにおいて、戻り値が常に「要素数3のリスト」であることを検証"""
    assert normalize_address(text_address) == expected

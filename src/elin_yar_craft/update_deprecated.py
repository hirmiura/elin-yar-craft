#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2024 hirmiura (https://github.com/hirmiura)

from __future__ import annotations

import argparse
import csv
import sys


def procee_args() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="deprecatedファイルを更新する")
    parser.add_argument(
        dest="target",
        metavar="TARGET_FILE",
        help="対象のdeprecatedファイル",
    )
    parser.add_argument(
        dest="reference",
        metavar="REFERENCE_FILE",
        help="参照するファイル",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()

    return args


def main() -> int:
    """メイン関数

    Returns:
        int: 成功時は0を返す
    """
    args = procee_args()

    # 対象ファイルの読み込み
    with open(args.target) as f:
        target_reader = csv.DictReader(f)
        target_list = list(target_reader)

    # 参照ファイルの読み込み
    with open(args.reference) as f:
        ref_reader = csv.DictReader(f)
        ref_list = list(ref_reader)
    ref_id_list = [v for d in ref_list if (v := d.get("id"))]  # idの列挙

    # idの重複を除いた新しいリスト
    new_list = []
    for d in target_list:
        id = d.get("id")
        if id not in ref_id_list:
            # 重複していないければ製造できないように変更して追加
            d["recipeKey"] = ""
            d["factory"] = ""
            new_list.append(d)
        else:
            tag = "重複"
            print(f"{tag}: {id}", file=sys.stderr)

    # 書き出し
    with open(args.target, "w") as f:
        writer = csv.DictWriter(f, target_list[0].keys())
        writer.writeheader()
        writer.writerows(new_list)

    return 0


if __name__ == "__main__":
    sys.exit(main())

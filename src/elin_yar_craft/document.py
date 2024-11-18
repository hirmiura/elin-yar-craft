#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2024 hirmiura (https://github.com/hirmiura)

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Any

type NameDictType = dict[str, list[str]]


def procee_args() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="ドキュメントを生成する")
    parser.add_argument(
        "-d",
        metavar="DIR",
        nargs="?",
        default=".",
        help="入出力ディレクトリ。未指定時はカレント。リポジトリのルートを指定する。",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()

    return args


def craftable_list(dir: str) -> None:
    assert dir
    jp_dir = Path(dir) / "Yar_Craft"
    cn_dir = Path(dir) / "Yar_Craft_CN"
    csv_weapon = "EDEFW_Thing_YarCraft_Weapon.csv"
    csv_armor = "EDEFW_Thing_YarCraft_Armor.csv"
    csv_accessory = "EDEFW_Thing_YarCraft_Accessory.csv"
    temp_path = Path(dir) / "document_template"
    doc_path = Path(dir) / "docs"

    # 日英版
    weapon_name_dict, weapon_name_jp_dict = get_name_dict(jp_dir / csv_weapon, True)
    armor_name_dict, armor_name_jp_dict = get_name_dict(jp_dir / csv_armor, True)
    accessory_name_dict, accessory_name_jp_dict = get_name_dict(jp_dir / csv_accessory, True)
    assert weapon_name_jp_dict and armor_name_jp_dict and accessory_name_jp_dict
    # 日英版を出力
    desc_file = "workshop_desc.txt"
    craftable_jp = gen_craftable_list(
        "近接武器",
        "防具",
        "アクセサリ",
        weapon_name_jp_dict,
        armor_name_jp_dict,
        accessory_name_jp_dict,
    )
    gen_workshop_desc(craftable_jp, temp_path / desc_file, doc_path / desc_file)
    desc_file_en = "workshop_desc_en.txt"
    craftable_jp = gen_craftable_list(
        "Melee", "Armor", "Accessory", weapon_name_dict, armor_name_dict, accessory_name_dict
    )
    gen_workshop_desc(craftable_jp, temp_path / desc_file_en, doc_path / desc_file_en)

    # 中文版
    weapon_name_dict, _ = get_name_dict(cn_dir / csv_weapon)
    armor_name_dict, _ = get_name_dict(cn_dir / csv_armor)
    accessory_name_dict, _ = get_name_dict(cn_dir / csv_accessory)
    # 中文版を出力
    desc_file_cn = "workshop_desc_cn.txt"
    craftable_cn = gen_craftable_list(
        "近战武器", "裝甲", "装饰", weapon_name_dict, armor_name_dict, accessory_name_dict
    )
    gen_workshop_desc(craftable_cn, temp_path / desc_file_cn, doc_path / desc_file_cn)
    return


def get_name_dict(path: Path, need_jp: bool = False) -> tuple[NameDictType, NameDictType | None]:
    """csvファイルを読み込んでカテゴリ毎に分けられたnameの辞書を返す

    Args:
        path (Path): csvファイル
        need_jp (bool, optional): 日本語版も読み込むか? Defaults to False.

    Returns:
        tuple[NameDictType, NameDictType | None]: nameの辞書とname_JPの辞書のタプル
    """
    with path.open() as f:
        reader = csv.DictReader(f)
        data = list(reader)
    name_dict = get_categorized_data(data, "name")
    name_jp_dict = get_categorized_data(data, "name_JP") if need_jp else None
    return name_dict, name_jp_dict


def get_categorized_data(data: list[dict[str, Any]], key: str) -> dict[str, list[str]]:
    assert data
    assert key
    # カテゴリ一覧を取得
    categories = [v for d in data if (v := d.get("category"))]
    categories: list[str] = list(set(categories))
    categories.sort()
    # カテゴリごとに一覧を作る
    result = {}
    for category in categories:
        list_by_key: list[str] = [
            k
            for d in data
            if d.get("category") == category
            and (k := d.get(key))
            and not re.search(r"_q\d$", str(d.get("id")))
        ]
        # 重複を削除
        list_by_key = list(dict.fromkeys(list_by_key))
        # 追加
        result[category] = list_by_key
    return result


def gen_craftable_list(
    weapon_title: str,
    armor_title: str,
    accessory_title: str,
    weapon_dict: dict[str, list[str]],
    armor_dict: dict[str, list[str]],
    accessory_dict: dict[str, list[str]],
) -> str:
    lines: list[str] = ["[list]"]
    for title, dic in zip(
        [weapon_title, armor_title, accessory_title], [weapon_dict, armor_dict, accessory_dict]
    ):
        lines.append(f"[*] {title}")
        lines.extend(gen_item_list(dic))
    lines.append("[/list]")  # 終了タグ

    return "\r\n".join(lines)


def gen_item_list(items: dict) -> list[str]:
    assert items
    spacer = [f"{' '*2}", f"{' '*6}"]
    lines: list[str] = []
    last = len(items) - 1
    for i, (k, v) in enumerate(items.items()):
        if i == 0:
            lines.append(f"{spacer[0]}[list]")  # 開始タグ

        lines.append(f"{spacer[0]}[*] {k}")
        item_line = ", ".join(v)
        lines.append(f"{spacer[1]}{item_line}")

        if i == last:
            lines.append(f"{spacer[0]}[/list]")  # 終了タグ

    return lines


def gen_workshop_desc(craftable: str, template: Path, output: Path) -> None:
    temp = template.read_text()
    text = temp.format(CraftableList=craftable)
    output.write_text(text)
    return


def main() -> int:
    """メイン関数

    Returns:
        int: 成功時は0を返す
    """
    args = procee_args()

    craftable_list(args.d)

    return 0


if __name__ == "__main__":
    sys.exit(main())

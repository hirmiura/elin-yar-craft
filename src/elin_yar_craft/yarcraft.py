#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2024 hirmiura (https://github.com/hirmiura)

from __future__ import annotations

import argparse
import copy
import csv
import re
import sys
import tomllib
from typing import Any, ClassVar

from mergedeep import merge
from pydantic import BaseModel


def procee_args() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="csvファイルをフィルターして出力する")
    parser.add_argument(
        "-i",
        metavar="IN",
        nargs="?",
        type=argparse.FileType("r", encoding="utf-8-sig"),  # BOM付いてるやん!!
        default=sys.stdin,
        help="入力ファイル。未指定時は標準入力",
    )
    parser.add_argument(
        "-o",
        metavar="OUT",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="出力ファイル。未指定時は標準出力",
    )
    parser.add_argument("-c", metavar="CONF", dest="conf", required=True, help="設定ファイル")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()

    return args


class CraftConf(BaseModel):
    key_default: ClassVar[str] = "DEFAULT"
    key_filter: ClassVar[str] = "filter"
    key_recipe: ClassVar[str] = "recipe"
    key_variant: ClassVar[str] = "variant"
    key_id: ClassVar[str] = "id"
    key_prefix: ClassVar[str] = "prefix"
    key_suffix: ClassVar[str] = "suffix"
    default: dict = {}
    rules: dict[str, dict] = {}

    @classmethod
    def load(cls, file) -> CraftConf:
        # ファイル読み込み
        with open(file, "rb") as f:
            toml = tomllib.load(f)
        # オブジェクト生成
        self = cls()
        # デフォルト設定を取得(あれば)
        key_default = cls.key_default
        if key_default in toml:
            self.default = toml[key_default]
            del toml[key_default]
        # 残りを取り込む
        self.rules = toml
        return self

    def check_and_create(self, line: dict[str, Any]) -> list[dict[str, Any]]:
        result = []
        if len(self.rules):
            for rule_name in self.rules:
                if self.check(line, rule_name):
                    result.extend(self.create_variant(line, rule_name))
        else:
            # デフォルトルールのみの場合
            if self.check(line, "", True):
                return self.create_variant(line, "", True)
        return result

    def check(self, line: dict[str, Any], rule_name: str, only_default: bool = False) -> bool:
        assert only_default or rule_name in self.rules
        key_filter = CraftConf.key_filter
        # 共通ルールと個別ルールをマージ
        default_rule = self.default.get(key_filter) or {}
        own_rule = (self.rules[rule_name].get(key_filter) or {}) if not only_default else {}
        rule = merge({}, default_rule, own_rule)
        # マッチング
        satisfy = False
        for key, pattern in rule.items():
            mat = re.search(pattern, line[key])
            if not mat:
                return False
            satisfy = True
        return satisfy

    def create_variant(
        self, line: dict[str, Any], rule_name: str, only_default: bool = False
    ) -> list[dict[str, Any]]:
        assert only_default or rule_name in self.rules
        key_recipe = CraftConf.key_recipe
        # 共通ルールと個別ルールをマージ
        default_recipe = self.default.get(key_recipe) or {}
        own_recipe = (self.rules[rule_name].get(key_recipe) or {}) if not only_default else {}
        recipe: dict[str, Any] = dict(merge({}, default_recipe, own_recipe))
        # 生成
        key_variant = CraftConf.key_variant
        key_id = CraftConf.key_id
        result: list[dict[str, Any]] = []
        for index, variant in enumerate(recipe[key_variant]):  # 各バリアント
            new = copy.deepcopy(line)
            new[key_id] = CraftConf.create_id(line[key_id], recipe, index)
            for recipe_key, recipe_item in recipe.items():
                if recipe_key == key_id or recipe_key == key_variant:
                    # idとvariantのレシピはスキップする
                    continue
                item = CraftConf.get_value_by_index_or_own(recipe_item, index)
                item = eval(f'f"""{item}"""')
                item = re.sub(r"/1\b", "", item)  # 1つのみ指定は消しておく
                new[recipe_key] = item
            result.append(new)

        return result

    @staticmethod
    def create_id(old_id: str, recipe: dict[str, Any], index: int) -> str:
        key_id = CraftConf.key_id
        key_prefix = CraftConf.key_prefix
        key_suffix = CraftConf.key_suffix

        prefix = ""
        suffix = ""
        # 設定を取得する
        if key_id in recipe:
            recipe_id = recipe[key_id]
            match recipe_id:
                case dict():
                    prefix = (
                        CraftConf.get_value_by_index_or_own(recipe_id[key_prefix], index)
                        if key_prefix in recipe_id
                        else ""
                    )
                    suffix = (
                        CraftConf.get_value_by_index_or_own(recipe_id[key_suffix], index)
                        if key_suffix in recipe_id
                        else ""
                    )
                case str():
                    # id指定があれば他を無視して返す
                    return recipe_id
                case list():
                    # id指定があれば他を無視して返す(リストの場合)
                    return CraftConf.get_value_by_index_or_own(recipe_id, index)
                case _:
                    raise TypeError("サポート対象外の型です")
        # 新しいidを生成する
        new_id = prefix + "_" if prefix else ""
        new_id += old_id
        new_id += "_" + suffix if suffix else ""
        return new_id

    @staticmethod
    def get_value_by_index_or_own(target: Any, index: int) -> Any:
        match target:
            case list():
                return target[index]
            case dict():
                return list(target.values())[index]
            case _:
                return target


def main() -> int:
    """メイン関数

    Returns:
        int: 成功時は0を返す
    """
    args = procee_args()

    # 設定ファイルの読み込み
    craft_conf = CraftConf.load(args.conf)

    # 入力csvファイルの読み込み
    reader = csv.DictReader(args.i)
    data = list(reader)
    header = data[0].keys()

    # 生成
    result = []
    for line in data:
        result.extend(craft_conf.check_and_create(line))

    # 書き出し
    writer = csv.DictWriter(args.o, header)
    writer.writeheader()
    writer.writerows(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())

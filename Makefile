# SPDX-License-Identifier: MIT
# Copyright 2024 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ/ファイル
D_ElinSrc	:= ElinSrc
F_CN_Thing	:= CN_Thing.xlsx
# 実行ファイル
E_YarCraft	:= poetry run src/elin_yar_craft/yarcraft.py
E_UpdateDep	:= poetry run src/elin_yar_craft/update_deprecated.py
E_Translate	:= poetry run src/elin_yar_craft/translate.py
E_Document	:= poetry run src/elin_yar_craft/document.py


#==============================================================================
# カラーコード
# ヘルプ表示
#==============================================================================
include ColorCode.mk
include Help.mk


#==============================================================================
# 各種確認
#==============================================================================
.PHONY: check
check: ## 事前にチェック項目を確認します
check: check_link check_link_cn


#==============================================================================
# Elin_source へのリンク/ディレクトリを確認
# Source Extractor の出力ディレクトリをチェックします
#==============================================================================
.PHONY: check_link
check_link: ## Elin_sourceへのリンク/ディレクトリを確認します
check_link:
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	@echo '"$(D_ElinSrc)" をチェックしています'
	@if [[ -L $(D_ElinSrc) && `readlink $(D_ElinSrc) ` ]] ; then \
		echo -e '    $(CC_BrGreen)SUCCESS$(CC_Reset): リンクです' ; \
	elif [[ -d $(D_ElinSrc) ]] ; then \
		echo -e '    $(CC_BrGreen)SUCCESS$(CC_Reset): ディレクトリです' ; \
	else \
		echo -e '    \a$(CC_BrRed)ERROR: "$(D_ElinSrc)" に "Elin_source/version" へのリンクを張って下さい$(CC_Reset)' ; \
		echo -e '    $(CC_BrRed)例: ln -s "/mnt/c/Elin_source/EA 23.23 fix 1" $(D_ElinSrc)$(CC_Reset)' ; \
		exit 1 ; \
	fi


#==============================================================================
# Elin/Package/_Lang_Chinese/Lang/CN/Game/Thing.xlsx へのリンク/ディレクトリを確認
#==============================================================================
.PHONY: check_link_cn
check_link_cn: ## Elin/Package/_Lang_Chinese/Lang/CN/Game/Thing.xlsxへのリンク/ディレクトリを確認します
check_link_cn:
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	@echo '"$(F_CN_Thing)" をチェックしています'
	@if [[ -L $(F_CN_Thing) && `readlink $(F_CN_Thing) ` ]] ; then \
		echo -e '    $(CC_BrGreen)SUCCESS$(CC_Reset): リンクです' ; \
	elif [[ -d $(F_CN_Thing) ]] ; then \
		echo -e '    $(CC_BrGreen)SUCCESS$(CC_Reset): ディレクトリです' ; \
	else \
		echo -e '    \a$(CC_BrRed)ERROR: "$(F_CN_Thing)" に "Elin/Package/_Lang_Chinese/Lang/CN/Game/Thing.xlsx" へのリンクを張って下さい$(CC_Reset)' ; \
		echo -e '    $(CC_BrRed)例: ln -s "/mnt/c/SteamLibrary/steamapps/common/Elin/Package/_Lang_Chinese/Lang/CN/Game/Thing.xlsx" $(F_CN_Thing)$(CC_Reset)' ; \
		exit 1 ; \
	fi


#==============================================================================
# 生成
#==============================================================================
.PHONY: generate update_deprecated
generate: ## csvファイルを生成します
generate: Yar_Craft/EDEFW_Thing_YarCraft_Weapon.csv Yar_Craft/EDEFW_Thing_YarCraft_Armor.csv update_deprecated

Yar_Craft/EDEFW_Thing_YarCraft_Weapon.csv: $(D_ElinSrc)/things.csv yarcraft_weapon.toml
	$(E_YarCraft) -i $< -o $@ -c yarcraft_weapon.toml

Yar_Craft/EDEFW_Thing_YarCraft_Armor.csv: $(D_ElinSrc)/things.csv yarcraft_armor.toml
	$(E_YarCraft) -i $< -o $@ -c yarcraft_armor.toml

update_deprecated: Yar_Craft/EDEFW_Thing_YarCraft_deprecated.csv Yar_Craft/EDEFW_Thing_YarCraft_Weapon.csv Yar_Craft/EDEFW_Thing_YarCraft_Armor.csv
	$(E_UpdateDep) $< Yar_Craft/EDEFW_Thing_YarCraft_Weapon.csv
	$(E_UpdateDep) $< Yar_Craft/EDEFW_Thing_YarCraft_Armor.csv


#==============================================================================
# 生成(中国語版)
#==============================================================================
.PHONY: generate_cn
generate_cn: ## 中国語版csvファイルを生成します
generate_cn: Yar_Craft_CN/EDEFW_Thing_YarCraft_Weapon.csv Yar_Craft_CN/EDEFW_Thing_YarCraft_Armor.csv Yar_Craft_CN/EDEFW_Thing_YarCraft_deprecated.csv

Yar_Craft_CN/%.csv: Yar_Craft/%.csv
	$(E_Translate) -i $< -o $@ -t CN_Thing.xlsx


#==============================================================================
# ドキュメント生成
#==============================================================================
.PHONY: docs
docs: ## ドキュメントを生成します
docs:
	$(E_Document)


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build
build: ## ビルドします
build: generate generate_cn docs


#==============================================================================
# 全ての作業を一括で実施する
#==============================================================================
.PHONY: all
all: ## 全ての作業を一括で実施します
all: check build


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-cn clean-docs clean-all
clean: ## クリーンアップします
clean: clean-cn clean-docs
	rm -f Yar_Craft/EDEFW_Thing_YarCraft_Weapon.csv Yar_Craft/EDEFW_Thing_YarCraft_Armor.csv

clean-cn:
	rm -f Yar_Craft_CN/*.csv

clean-docs:
	rm -f docs/workshop_desc*.txt

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean

# Yar Craft

装備を製作できるようにします。

## Elin Data Expanded Framework

このModの動作にはEDEFWが必須です。
以下をサブスクライブしてください。

[Elin Data Expanded Framework](https://steamcommunity.com/sharedfiles/filedetails/?id=3363033460)

## レシピ

低位の装備は最初から習得していますが、高位(内部Lvが10以上)の装備は閃く必要があります。

## ゲーム途中からの追加

問題ありません。

## ゲーム途中からの削除

問題あります。  
各アイテムは本来の物とは別IDとなっている為です。  
これは素材と作業台を作り分ける為の措置です。

具体的には、作成したアイテムがジャンクに化けます(elonaでいう金塊みたいなもの)。

## 他Modとの競合

アイテムデータを独自idで追加しているだけなので、無いはずなのですが……

[KK With My Sister と併用するとフィートが取得できなくなる](https://github.com/hirmiura/elin-yar-craft/issues/2)現象が起きます。  
[KK With My Sister](https://steamcommunity.com/sharedfiles/filedetails/?id=3358081949)

Modの読み込み順を KK With My Sister を先にすることで治ります。

1. KK With My Sister
2. Elin Data Expanded Framework

## 製作できる装備

現バージョンでは以下の装備が製作できます。

* 近接武器(金属/木/石)
  * 包丁
  * 忍刀
  * 海賊刀
  * 短剣
  * 大剣
  * 刀
  * 長剣
  * 大斧
  * 戦斧
  * 手斧
  * 機械斧
  * 大槌
  * 棍棒
  * メイス
  * 鉾槍
  * 三叉槍
  * 長槍
  * 大鎌
  * 戦鎌
  * 長棒
  * 杖
  * 爪
* 近接武器(布のみ)
  * グローブ
* 盾(金属/木/石)
  * 小盾
  * 丸型盾
  * 盾
  * 合成盾
  * 騎士盾
  * 重層盾
* 頭防具(金属/木/石/布)
  * 兜
  * 羽帽子
  * 魔法帽
  * 騎士兜
  * 重兜
  * フェアリーハット
  * 合金兜
  * 大兜
* 胴体防具(金属/木/石/布)
  * 法衣
  * 胸甲
  * 服
  * 軽鎧
  * 厚鎧
  * 防護服
  * 輪鎧
  * 大鎧
  * 合成鎧
  * 防弾服
  * 綴り鎧
  * 法王衣
  * 重層鎧
* 腰防具(金属/木/石/布)
  * 腰当
  * 合成腰当
  * 重層腰当

## ソース

[github](https://github.com/hirmiura/elin-yar-craft)

## 変更履歴

* 2024/11/12  
スクリプトによる生成に切り替えました。  
旧データは退避しているので後方互換は問題ないはずです。

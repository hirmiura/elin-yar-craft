# コストデザイン

- 重さ(weight)に応じて主材料(variant)を増やす
- 魔石(magic_stone)とルーン(rune)は取り敢えず消す
- 価値(value)に応じてオレン(money)を費やす
- 通貨を利用する
  - オレン (money)
  - 金塊 (money2)
  - プラチナ硬貨 (plat)
  - 小さなメダル (medal)
- 高位品は低位品を材料にする

| Q | 品質   | スキルLv | プラチナ |
|---|--------|---------:|---------:|
| 1 | 高品質 | +10      | +1       |
| 2 | 奇跡   | +30      | +5       |
| 3 | 神器   | +50      | +10      |
| 4 | 特別製 | +100     | +100     |

- 重さ   `(w:=int(line['weight']))`  
主材料:  `int((w:=int(line['weight']))/500+1)`  
副材料1: `int(w/1000+1)`  
副材料2: `int(w/2000+1)`
- 価値   `(v:=int(line['value']))`  
オレン:  `int((v:=int(line['value']))/100+1)`

## 近接武器

`{variant}/{int((w:=int(line['weight']))/500+1)},resin/{int(w/1000+1)},string/{int(w/2000+1)},money/{int((v:=int(line['value']))/100+1)}`

- axe  
大斧, 戦斧, 手斧, 機械斧
- blunt  
大槌, 棍棒, メイス
- dagger  
包丁, 忍刀, 海賊刀, 短剣
- martial  
爪, グローブ
- polearm  
鉾槍, 三叉槍, 長槍
- scythe  
大鎌, 戦鎌
- shield  
小盾, 丸型盾, 盾, 合成盾, 騎士盾, 重層盾
- staff  
長棒, 杖
- sword  
大剣, 刀, 長剣

## 防具

`{variant}/{int((w:=int(line['weight']))/500+1)},texture/{int(w/1000+1)},string/{int(w/2000+1)},needle/{int(w/2000+1)},money/{int((v:=int(line['value']))/100+1)}`

- arm  
軽手袋, 厚篭手, 合成篭手, 手袋, 重層篭手, 細工篭手, 大篭手
- back  
軽外套, 翼, 外套, 陣羽織, 防護外套, 羽
- foot  
履物, 靴, 重靴, 厚靴, 合成靴, 装甲靴, 大靴
- head  
兜, 羽帽子, 魔法帽, 騎士兜, 重兜, フェアリーハット, 合金兜, 大兜
- torso  
法衣, 胸甲, 服, 軽鎧, 厚鎧, 防護服, 輪鎧, 大鎧, 合成鎧, 防弾服, 綴り鎧, 法王衣, 重層鎧
- waist  
腰当, 合成腰当, 重層腰当

## アクセサリ

`{variant}/{int((w:=int(line['weight']))/20+1)},gem/{int(w/50+1)},money/{int((v:=int(line['value']))/50+1)}`

- amulet  
結婚首輪, 装飾首輪, ネックレス, 細工首輪, お守り, 首当て, 護符, ペリドット
- ring  
結婚指輪, 装飾の指輪, 指輪, 指当て, 合金指輪
- ring (special)
スピードの指輪, オーロラリング  
`{variant}/{int((w:=int(line['weight']))/20+1)},gem/{int(w/50+1)},money/{int((v:=int(line['value']))/50+1),money2/{int((v:=int(line['value']))/10+1)}`

// SPDX-License-Identifier: MIT
// Copyright 2024 hirmiura (https://github.com/hirmiura)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

using ResultPair = (object before, object after);

namespace YarCraft;
using WalkArgFunc = Func<Card, ResultPair>;

public static class Walker
{
    public static List<ResultPair> WalkAllCard(WalkArgFunc func)
    {
        List<ResultPair> result = [];
        var eClassCards = EClass.game.cards;

        // キャラ
        Plugin.Logger.LogDebug("Search globalCharas");
        foreach (var chara in eClassCards.globalCharas.Values)
        {
            Plugin.Logger.LogDebug($"Chara id:{chara.id}, uid:{chara.uid}, {chara.Name}");
            result.AddRange(chara.Walk(func));
        }

        // 配達
        Plugin.Logger.LogDebug("Search container_deliver");
        result.AddRange(eClassCards.container_deliver.Walk(func));
        Plugin.Logger.LogDebug("Search container_deposit");
        result.AddRange(eClassCards.container_deposit.Walk(func));
        Plugin.Logger.LogDebug("Search container_shipping");
        result.AddRange(eClassCards.container_shipping.Walk(func));

        // ゾーン
        Plugin.Logger.LogDebug("Search Zones");
        foreach (var zone in EClass.game.spatials.Zones)
        {
            Plugin.Logger.LogDebug($"Zone id:{zone.id}, uid:{zone.uid}");
            if (zone.map is null) continue;
            foreach (var cell in zone.map.cells)
            {
                result.AddRange(cell.Things.Walk(func));
            }

        }
        return result;
    }

    public static List<ResultPair> Walk(this Card card, WalkArgFunc func)
    {
        Plugin.Logger.LogDebug($"Card id:{card.id}, uid:{card.uid}, {card.Name}");
        List<ResultPair> result = func is null ? [] : [func(card)];
        result.AddRange(card.things.Walk(func));
        return result;
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static List<ResultPair> Walk(this IEnumerable<Card> cards, WalkArgFunc func)
    {
        return cards.SelectMany(c => c.Walk(func)).ToList();
    }
}

// SPDX-License-Identifier: MIT
// Copyright 2024 hirmiura (https://github.com/hirmiura)
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace YarCraft;

public static class IdReplacer
{
    public static Regex FirstMatchV1 = new(@"^YarCraft_", RegexOptions.Compiled);
    public static Regex FirstMatchV2 = new(@"^YarCraft_.+_YarCraft", RegexOptions.Compiled);
    public static Regex[] RuleV1 = [
        new(@"^YarCraft_", RegexOptions.Compiled),
        new(@"_q\d$", RegexOptions.Compiled),
        new(@"_(wood|stone|metal|cloth)?$", RegexOptions.Compiled),
    ];
    public static Regex[] RuleV2 = [
        new(@"^YarCraft_", RegexOptions.Compiled),
        new(@"_YarCraft.*$", RegexOptions.Compiled),
    ];
    public static (Regex, string)[] RuleException = [
        (new(@"^(ring|amulet)_of_(fire_cold|music)$", RegexOptions.Compiled), @"\1_decorative"),
    ];

    public static string Clean(string id)
    {
        if (!FirstMatchV1.IsMatch(id)) return id;

        var result = id;
        result = CleanV2(result);
        if (result == id)
            result = CleanV1(result);
        return result;
    }

    public static string CleanV1(string id)
    {
        if (!FirstMatchV1.IsMatch(id)) return id;
        var newId = CleanUtil(id, RuleV1);
        Plugin.Logger.LogInfo($"IdReplacer match V1: {id} -> {newId}");
        newId = ReplaceException(newId);
        return newId;
    }

    public static string CleanV2(string id)
    {
        if (!FirstMatchV2.IsMatch(id)) return id;
        var newId = CleanUtil(id, RuleV2);
        Plugin.Logger.LogInfo($"IdReplacer match V2: {id} -> {newId}");
        newId = ReplaceException(newId);
        return newId;
    }

    public static string CleanUtil(string id, IReadOnlyList<Regex> rules)
    {
        var result = id;
        foreach (var rule in rules)
        {
            result = rule.Replace(result, "");
        }
        return result;
    }

    public static string ReplaceException(string id)
    {
        foreach (var (rgx, repl) in RuleException)
        {
            if (rgx.IsMatch(id))
            {
                var newId = rgx.Replace(id, repl);
                Plugin.Logger.LogInfo($"IdReplacer match Exception: {id} -> {newId}");
                return newId;
            }
        }
        return id;
    }
}

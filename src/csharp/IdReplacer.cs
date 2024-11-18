// SPDX-License-Identifier: MIT
// Copyright 2024 hirmiura (https://github.com/hirmiura)
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace YarCraft;

public static class IdReplacer
{
    public static Regex FirstMatch = new(@"^YarCraft", RegexOptions.Compiled);
    public static Regex[] RuleV1 = [
        new(@"^YarCraft_", RegexOptions.Compiled),
        new(@"_q\d$", RegexOptions.Compiled),
        new(@"_(wood|stone|metal|cloth)?$", RegexOptions.Compiled),
    ];
    public static Regex[] RuleV2 = [
        new(@"^YarCraft_", RegexOptions.Compiled),
        new(@"_YarCraft.*$", RegexOptions.Compiled),
    ];

    public static string Clean(string id)
    {
        if (!FirstMatch.IsMatch(id)) return id;

        var result = id;
        result = CleanV2(result);
        result = CleanV1(result);
        return result;
    }

    public static string CleanV1(string id)
    {
        return CleanUtil(id, RuleV1);
    }
    public static string CleanV2(string id)
    {
        return CleanUtil(id, RuleV2);
    }

    public static string CleanUtil(string id, IReadOnlyList<Regex> rules)
    {
        if (!FirstMatch.IsMatch(id)) return id;

        var result = id;
        foreach (var rule in rules)
        {
            result = rule.Replace(result, "");
        }
        return result;
    }
}

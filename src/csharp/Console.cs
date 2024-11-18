// SPDX-License-Identifier: MIT
// Copyright 2024 hirmiura (https://github.com/hirmiura)
using System.Collections.Generic;
using System.IO;
using System.Linq;
using ReflexCLI.Attributes;

namespace YarCraft;

[ConsoleCommandClassCustomizer("")]
public static class Console
{
    public static string DebugFile = "debug.txt";
    public static readonly string[] CompleteMessage = {
            "Completed the clean up of IDs related Yar Craft.",
            "Yar Craft に関連するIDの浄化が完了しました"
        };

    [ConsoleCommand("")]
    public static string YarCraftCleanID()
    {
        var message = new List<string>(CompleteMessage);

        // 全カードを走査(たぶん)
        var result = Walker.WalkAllCard(c =>
        {
            var oldId = c.id;
            var newId = IdReplacer.Clean(c.id);
            c.id = newId;
            return (oldId, newId);
        });
        result.Sort();
        // デバッグ用に出力
        var file = Path.Combine(Plugin.ModDirectory, DebugFile);
        File.WriteAllText(file, string.Join("\n", result));

        // 変更されたものだけを抽出
        var changed = from r in result where r.before != r.after select r;

        // 表示用に整形
        var output = from c in changed select $"{c.before} -> {c.after}";
        message.AddRange(output);

        return string.Join("\n", message);
    }
}

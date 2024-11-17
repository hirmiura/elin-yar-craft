using System.Collections.Generic;
using ReflexCLI.Attributes;

namespace YarCraft;

[ConsoleCommandClassCustomizer("")]
public static class Console
{
    public static readonly string[] completeMessage = {
            "Completed the clean up of IDs related Yar Craft.",
            "Yar Craft に関連するIDの浄化が完了しました"
        };

    [ConsoleCommand("")]
    public static string YarCraftCleanID()
    {
        List<string> message = new List<string>(completeMessage);
        List<string> ids = new List<string>();

        var packages = EClass.game.cards.listPackage;
        foreach (var thing in packages)
        {
            var id = thing.id;
            var uid = thing.uid;
            var text = $"id:{id}, uid:{uid}";
            ids.Add(text);
            Plugin.Logger.LogDebug(text);
        }

        ids.Sort();
        message.AddRange(ids);
        return string.Join("\n", message);
    }
}

// SPDX-License-Identifier: MIT
// Copyright 2024 hirmiura (https://github.com/hirmiura)
using System.IO;
using System.Reflection;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using ReflexCLI;

namespace YarCraft;

public static class MyPluginInfo
{
    public const string PLUGIN_GUID = "yararezon.yar_craft";
    public const string PLUGIN_NAME = "Yar Craft";
    public const string PLUGIN_VERSION = "0.2.7";
}


[BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
public class Plugin : BaseUnityPlugin
{
    internal static new ManualLogSource Logger;
    public static string ModDirectory = "";

    private void Awake()
    {
        Logger = base.Logger;

        // 設定ファイル
        var executingAssembly = Assembly.GetExecutingAssembly();
        ModDirectory = Path.GetDirectoryName(executingAssembly.Location);
        // var configFile = new ConfigFile(Path.Combine(ModDirectory, "plugin.cfg"), true);

        // ハーモニーパッチ
        var harmony = new Harmony(MyPluginInfo.PLUGIN_GUID);
        harmony.PatchAll();

        // コマンドの登録
        CommandRegistry.assemblies.Add(executingAssembly);
    }
}


[HarmonyPatch(typeof(ThingGen))]
[HarmonyPatch(nameof(ThingGen._Create))]
public class ThingGenPatch
{
    public static Thing Postfix(Thing __result)
    {
        __result.id = IdReplacer.Clean(__result.id);
        return __result;
    }
}

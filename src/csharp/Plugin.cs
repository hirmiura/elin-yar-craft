using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using ReflexCLI;
using UnityEngine;

namespace YarCraft;

public static class MyPluginInfo
{
    public const string PLUGIN_GUID = "yararezon.yar_craft";
    public const string PLUGIN_NAME = "Yar Craft";
    public const string PLUGIN_VERSION = "0.2.3";
}


[BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
public class Plugin : BaseUnityPlugin
{
    internal static new ManualLogSource Logger;
    public static string ModDirectory = "";
    public static Regex Rgx { get; private set; }
    public static Regex RgxUnderbar { get; private set; }
    public static string Replacement { get; private set; }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static string Replace(string input)
    {
        return Plugin.RgxUnderbar.Replace(Plugin.Rgx.Replace(input, Plugin.Replacement), "");
    }

    private void Awake()
    {
        Logger = base.Logger;
        // 設定ファイル
        var executingAssembly = Assembly.GetExecutingAssembly();
        var directoryName = Path.GetDirectoryName(executingAssembly.Location);
        var configFile = new ConfigFile(Path.Combine(directoryName, "plugin.cfg"), true);
        //lang=regex
        var pattern = configFile.Bind("General", "Pattern", @"^YarCraft_(?<id>.+?)(_(wood|stone|metal|cloth)?)?(_q\d)?$", "正規表現パターン").Value;
        Plugin.Rgx = new Regex(pattern, RegexOptions.Compiled);
        Plugin.RgxUnderbar = new Regex("_+$", RegexOptions.Compiled);
        //lang=regex
        Plugin.Replacement = configFile.Bind("General", "Replace", @"${id}", "正規表現置換").Value;

        Logger.LogInfo($"Plugin {MyPluginInfo.PLUGIN_GUID} is loaded!");  // BepInExとElin両方のログ
        // コマンドの登録
        CommandRegistry.assemblies.Add(executingAssembly);
    }

    private void Start()
    {
        Debug.Log(MyPluginInfo.PLUGIN_NAME + " Start");  // Elinのログ
        var harmony = new Harmony(MyPluginInfo.PLUGIN_NAME);
        harmony.PatchAll();
    }
}


[HarmonyPatch(typeof(ThingGen))]
[HarmonyPatch(nameof(ThingGen._Create))]
public class ThingGenPatch
{
    public static Thing Postfix(Thing __result)
    {
        var old_id = __result.id;
        if (Plugin.Rgx.IsMatch(old_id))
        {
            var new_id = Plugin.Replace(old_id);
            __result.id = new_id;
            Plugin.Logger.LogDebug($" ThingGenPatch Postfix: Replace from {old_id} to {new_id}");
        }
        return __result;
    }
}

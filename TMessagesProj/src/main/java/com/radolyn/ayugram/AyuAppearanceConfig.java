/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram;

import android.app.Activity;
import android.content.SharedPreferences;

import org.telegram.messenger.ApplicationLoader;

public class AyuAppearanceConfig {

    private static final Object sync = new Object();
    private static boolean configLoaded;

    public static SharedPreferences preferences;
    public static SharedPreferences.Editor editor;

    // Appearance flags used by core telegram/* files
    public static boolean hideActionBarStatus;
    public static boolean alternativeOpenAnimation;
    public static boolean useSolarIcons;
    public static int tabIcons; // 0 = icons+titles, 1 = titles, 2 = icons
    public static int titleText;

    static {
        loadConfig();
    }

    public static void loadConfig() {
        synchronized (sync) {
            if (configLoaded) {
                return;
            }

            preferences = ApplicationLoader.applicationContext.getSharedPreferences("exteraconfig", Activity.MODE_PRIVATE);
            editor = preferences.edit();

            hideActionBarStatus = preferences.getBoolean("hideActionBarStatus", false);
            alternativeOpenAnimation = preferences.getBoolean("alternativeOpenAnimation", true);
            useSolarIcons = preferences.getBoolean("useSolarIcons", true);
            tabIcons = preferences.getInt("tabIcons", 1);
            titleText = preferences.getInt("titleText", 2);

            configLoaded = true;
        }
    }

    public static void setHideActionBarStatus(boolean value) {
        hideActionBarStatus = value;
        editor.putBoolean("hideActionBarStatus", value).apply();
    }

    public static void setAlternativeOpenAnimation(boolean value) {
        alternativeOpenAnimation = value;
        editor.putBoolean("alternativeOpenAnimation", value).apply();
    }

    public static void setUseSolarIcons(boolean value) {
        useSolarIcons = value;
        editor.putBoolean("useSolarIcons", value).apply();
    }

    public static void setTabIcons(int value) {
        tabIcons = value;
        editor.putInt("tabIcons", value).apply();
    }

    public static void setTitleText(int value) {
        titleText = value;
        editor.putInt("titleText", value).apply();
    }
}

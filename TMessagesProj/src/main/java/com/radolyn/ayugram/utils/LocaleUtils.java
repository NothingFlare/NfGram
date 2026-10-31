/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.utils;

import org.telegram.messenger.LocaleController;

public class LocaleUtils {

    public static String getString(String key) {
        return LocaleController.getString(key);
    }

    public static String getString(String key, int res) {
        return LocaleController.getString(key, res);
    }

    public static String formatString(String key, int res, Object... args) {
        return LocaleController.formatString(key, res, args);
    }

    public static String formatPluralString(String key, int plural) {
        return LocaleController.formatPluralString(key, plural);
    }

    public static CharSequence formatWithURLs(CharSequence text) {
        return text;
    }
}
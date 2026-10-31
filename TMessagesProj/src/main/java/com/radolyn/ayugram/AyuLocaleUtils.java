/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram;

import android.text.TextUtils;

import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.messenger.UserConfig;
import org.telegram.messenger.UserObject;
import org.telegram.tgnet.TLRPC;

public class AyuLocaleUtils {

    public static String getActionBarTitle() {
        String title;
        int actionBarTitle = AyuAppearanceConfig.titleText;
        switch (actionBarTitle) {
            case 0:
                title = LocaleController.getString("exteraAppName", R.string.exteraAppName);
                break;
            case 3:
                title = LocaleController.getString(R.string.FilterChats);
                break;
            default:
                TLRPC.User user = UserConfig.getInstance(UserConfig.selectedAccount).getCurrentUser();
                title = actionBarTitle == 1 && !TextUtils.isEmpty(UserObject.getPublicUsername(user)) ? UserObject.getPublicUsername(user) : UserObject.getFirstName(user);
                break;
        }
        return title;
    }

    public static String getAppName() {
        try {
            return org.telegram.messenger.ApplicationLoader.applicationContext.getString(R.string.exteraAppName);
        } catch (Exception e) {
            return "AyuGram";
        }
    }
}

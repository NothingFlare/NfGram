/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

import org.telegram.tgnet.ConnectionsManager;

public class ScreenReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals(Intent.ACTION_SCREEN_OFF)) {
            if (BuildVars.LOGS_ENABLED) {
                FileLog.d("screen off");
            }
            ConnectionsManager.getInstance(UserConfig.selectedAccount).setAppPaused(true, true);
            ApplicationLoader.isScreenOn = false;
        } else if (intent.getAction().equals(Intent.ACTION_SCREEN_ON)) {
            if (BuildVars.LOGS_ENABLED) {
                FileLog.d("screen on");
            }
            ConnectionsManager.getInstance(UserConfig.selectedAccount).setAppPaused(false, true);
            ApplicationLoader.isScreenOn = true;
        }
        NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.screenStateChanged);
    }
}

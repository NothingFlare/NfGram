/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class NotificationCallbackReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null) {
            return;
        }
        ApplicationLoader.postInitApplication();
        int currentAccount = intent.getIntExtra("currentAccount", UserConfig.selectedAccount);
        if (!UserConfig.isValidAccount(currentAccount)) {
            return;
        }
        long did = intent.getLongExtra("did", 777000);
        byte[] data = intent.getByteArrayExtra("data");
        int mid = intent.getIntExtra("mid", 0);
        SendMessagesHelper.getInstance(currentAccount).sendNotificationCallback(did, mid, data);
    }
}

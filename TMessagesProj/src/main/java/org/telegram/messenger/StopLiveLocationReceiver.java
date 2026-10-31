/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class StopLiveLocationReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        for (int a = 0; a < UserConfig.MAX_ACCOUNT_COUNT; a++) {
            LocationController.getInstance(a).removeAllLocationSharings();
        }
    }
}

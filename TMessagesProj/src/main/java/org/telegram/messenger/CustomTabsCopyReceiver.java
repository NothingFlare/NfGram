/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class CustomTabsCopyReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        String url = intent.getDataString();
        if (url != null) {
            AndroidUtilities.addToClipboard(url);
            Toast.makeText(context, LocaleController.getString(R.string.LinkCopied), Toast.LENGTH_SHORT).show();
        }
    }
}

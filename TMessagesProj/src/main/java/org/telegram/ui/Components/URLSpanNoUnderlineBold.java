/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.text.TextPaint;

import org.telegram.messenger.AndroidUtilities;

public class URLSpanNoUnderlineBold extends URLSpanNoUnderline {

    public URLSpanNoUnderlineBold(String url) {
        super(url != null ? url.replace('\u202E', ' ') : url);
    }

    @Override
    public void updateDrawState(TextPaint ds) {
        super.updateDrawState(ds);
        ds.setTypeface(AndroidUtilities.bold());
        ds.setUnderlineText(false);
    }
}

/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.text.TextPaint;
import android.view.View;

import org.telegram.ui.ActionBar.Theme;

public class URLSpanUserMention extends URLSpanNoUnderline {

    private int currentType;
    private TextStyleSpan.TextStyleRun style;

    public URLSpanUserMention(String url, int type) {
        this(url, type, null);
    }

    public URLSpanUserMention(String url, int type, TextStyleSpan.TextStyleRun run) {
        super(url);
        currentType = type;
        style = run;
    }

    @Override
    public void onClick(View widget) {
        super.onClick(widget);
    }

    @Override
    public void updateDrawState(TextPaint p) {
        super.updateDrawState(p);
        if (currentType == 3) {
            p.setColor(Theme.getColor(Theme.key_windowBackgroundWhiteLinkText));
        } else if (currentType == 2) {
            p.setColor(0xffffffff);
        } else if (currentType == 1) {
            p.setColor(Theme.getColor(Theme.key_chat_messageLinkOut));
        } else {
            p.setColor(Theme.getColor(Theme.key_chat_messageLinkIn));
        }
        if (style != null) {
            style.applyStyle(p);
        } else {
            p.setUnderlineText(false);
        }
    }
}

/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.net.Uri;
import android.text.TextPaint;
import android.text.style.URLSpan;
import android.view.View;

import org.telegram.messenger.browser.Browser;
import org.telegram.ui.LaunchActivity;

public class URLSpanReplacement extends URLSpan {

    private TextStyleSpan.TextStyleRun style;
    private boolean navigateToPremiumBot;

    public URLSpanReplacement(String url) {
        this(url, null);
    }

    public URLSpanReplacement(String url, TextStyleSpan.TextStyleRun run) {
        super(url != null ? url.replace('\u202E', ' ') : url);
        style = run;
    }

    public void setNavigateToPremiumBot(boolean navigateToPremiumBot) {
        this.navigateToPremiumBot = navigateToPremiumBot;
    }

    public TextStyleSpan.TextStyleRun getTextStyleRun() {
        return style;
    }

    @Override
    public void onClick(View widget) {
        if (navigateToPremiumBot && widget.getContext() instanceof LaunchActivity) {
            ((LaunchActivity) widget.getContext()).setNavigateToPremiumBot(true);
        }
        Uri uri = Uri.parse(getURL());
        Browser.openUrl(widget.getContext(), uri);
    }

    @Override
    public void updateDrawState(TextPaint p) {
        int color = p.getColor();
        super.updateDrawState(p);
        if (style != null) {
            style.applyStyle(p);
            p.setUnderlineText(p.linkColor == color);
        }
    }
}

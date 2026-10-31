/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.text.TextPaint;
import android.text.style.ForegroundColorSpan;

public class ColorSpanUnderline extends ForegroundColorSpan {

    public ColorSpanUnderline(int color) {
        super(color);
    }

    @Override
    public void updateDrawState(TextPaint ds) {
        super.updateDrawState(ds);
        ds.setUnderlineText(true);
    }
}

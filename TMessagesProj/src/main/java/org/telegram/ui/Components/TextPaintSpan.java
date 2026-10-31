/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.text.TextPaint;
import android.text.style.MetricAffectingSpan;

public class TextPaintSpan extends MetricAffectingSpan {

    private TextPaint textPaint;

    public TextPaintSpan(TextPaint paint) {
        textPaint = paint;
    }

    @Override
    public void updateMeasureState(TextPaint p) {
        p.setColor(textPaint.getColor());
        p.setTypeface(textPaint.getTypeface());
        p.setFlags(textPaint.getFlags());
        p.setTextSize(textPaint.getTextSize());
        p.baselineShift = textPaint.baselineShift;
        p.bgColor = textPaint.bgColor;
    }

    @Override
    public void updateDrawState(TextPaint p) {
        p.setColor(textPaint.getColor());
        p.setTypeface(textPaint.getTypeface());
        p.setFlags(textPaint.getFlags());
        p.setTextSize(textPaint.getTextSize());
        p.baselineShift = textPaint.baselineShift;
        p.bgColor = textPaint.bgColor;
    }
}

/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.text.TextPaint;
import android.text.style.MetricAffectingSpan;

public class AnchorSpan extends MetricAffectingSpan {

    private String name;

    public AnchorSpan(String n) {
         name = n.toLowerCase();
    }

    public String getName() {
        return name;
    }

    @Override
    public void updateMeasureState(TextPaint p) {

    }

    @Override
    public void updateDrawState(TextPaint tp) {

    }
}

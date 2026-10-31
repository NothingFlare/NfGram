/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Cells;

import android.content.Context;
import android.graphics.Canvas;
import android.util.TypedValue;
import android.view.Gravity;
import android.widget.TextView;

import org.telegram.messenger.AndroidUtilities;
import org.telegram.ui.ActionBar.Theme;

public class HashtagSearchCell extends TextView {

    private boolean needDivider;

    public HashtagSearchCell(Context context) {
        super(context);
        setGravity(Gravity.CENTER_VERTICAL);
        setPadding(AndroidUtilities.dp(16), 0, AndroidUtilities.dp(16), 0);
        setTextSize(TypedValue.COMPLEX_UNIT_DIP, 17);
        setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText));
    }

    public void setNeedDivider(boolean value) {
        needDivider = value;
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        setMeasuredDimension(MeasureSpec.getSize(widthMeasureSpec), AndroidUtilities.dp(48) + 1);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (needDivider) {
            canvas.drawLine(0, getHeight() - 1, getWidth(), getHeight() - 1, Theme.dividerPaint);
        }
    }
}

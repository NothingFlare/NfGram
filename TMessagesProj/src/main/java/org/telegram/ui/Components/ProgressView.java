/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.graphics.Canvas;
import android.graphics.Paint;

import org.telegram.messenger.AndroidUtilities;

public class ProgressView {
    
    private Paint innerPaint;
    private Paint outerPaint;

    public float currentProgress = 0;
    public int width;
    public int height;
    public float progressHeight = AndroidUtilities.dp(2.0f);

    public ProgressView() {
        innerPaint = new Paint();
        outerPaint = new Paint();
    }

    public void setProgressColors(int innerColor, int outerColor) {
        innerPaint.setColor(innerColor);
        outerPaint.setColor(outerColor);
    }

    public void setProgress(float progress) {
        currentProgress = progress;
        if (currentProgress < 0) {
            currentProgress = 0;
        } else if (currentProgress > 1) {
            currentProgress = 1;
        }
    }

    public void draw(Canvas canvas) {
        canvas.drawRect(0, height / 2 - progressHeight / 2.0f, width, height / 2 + progressHeight / 2.0f, innerPaint);
        canvas.drawRect(0, height / 2 - progressHeight / 2.0f, width * currentProgress, height / 2 + progressHeight / 2.0f, outerPaint);
    }
}

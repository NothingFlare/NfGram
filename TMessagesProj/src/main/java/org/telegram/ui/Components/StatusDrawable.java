/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.graphics.Paint;
import android.graphics.drawable.Drawable;

public abstract class StatusDrawable extends Drawable {
    public abstract void start();
    public abstract void stop();
    public abstract void setIsChat(boolean value);
    public abstract void setColor(int color);
}

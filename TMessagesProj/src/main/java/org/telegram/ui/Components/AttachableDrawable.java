/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

import android.view.View;

import org.telegram.messenger.ImageReceiver;

public interface AttachableDrawable {
    void onAttachedToWindow(ImageReceiver parent);
    void onDetachedFromWindow(ImageReceiver parent);

    default void setParent(View view) {}
}

/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.utils;

public class AyuStateVariable {
    private final Object sync = new Object();

    public volatile boolean val;
    public volatile int resetAfter;

    public void set(boolean val, int resetAfter) {
        synchronized (sync) {
            this.val = val;
            this.resetAfter = resetAfter;
        }
    }

    public boolean process() {
        synchronized (sync) {
            if (resetAfter == -1) {
                return val;
            }

            resetAfter -= 1;
            var currentVal = val;

            if (resetAfter == 0) {
                val = false;
            }

            return currentVal;
        }
    }
}

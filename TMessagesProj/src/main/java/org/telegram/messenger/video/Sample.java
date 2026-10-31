/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger.video;

public class Sample {
    private long offset;
    private long size;

    public Sample(long offset, long size) {
        this.offset = offset;
        this.size = size;
    }

    public long getOffset() {
        return offset;
    }

    public long getSize() {
        return size;
    }
}

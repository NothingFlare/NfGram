/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.sync;

public class AyuSyncControllerEmpty extends AyuSyncController {
    @Override
    public void connect() {
        // nah
    }

    @Override
    public void forceSync() {
        // nah
    }

    @Override
    public void syncRead(int accountId, long dialogId, int untilId) {
        // nah
    }
}

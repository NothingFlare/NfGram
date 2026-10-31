/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.sync.models;

public interface SyncEvent {
    String type = "sync_unspecified";
    long userId = 0;
}

/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.sync.models;

public class SyncForce implements SyncEvent {
    public String type = "sync_force";
    public long userId;
    public SyncForce.SyncForceArgs args;

    public static class SyncForceArgs {
        public int fromDate;
    }
}

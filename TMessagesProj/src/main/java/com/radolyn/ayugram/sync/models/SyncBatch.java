/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.sync.models;

import java.util.ArrayList;

public class SyncBatch implements SyncEvent {
    public String type = "sync_batch";
    public long userId;
    public SyncBatch.SyncBatchArgs args;

    public static class SyncBatchArgs {
        public ArrayList<SyncEvent> events = new ArrayList<>();
    }
}

/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.sync.models;

public class SyncRead implements SyncEvent {
    public String type = "sync_read";
    public long userId;
    public SyncReadArgs args;

    public static class SyncReadArgs {
        public long dialogId;
        public int untilId;
        public int unread;
    }
}

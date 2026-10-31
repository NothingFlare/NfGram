/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.sync.models;

public class SyncForceFinish implements SyncEvent {
    public String type = "sync_force_finish";
    public long userId;
    public SyncForceFinish.SyncForceFinishArgs args;

    public static class SyncForceFinishArgs {
    }
}

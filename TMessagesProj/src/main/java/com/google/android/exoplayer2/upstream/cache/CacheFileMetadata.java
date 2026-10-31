/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream.cache;

/** Metadata associated with a cache file. */
/* package */ final class CacheFileMetadata {

  public final long length;
  public final long lastTouchTimestamp;

  public CacheFileMetadata(long length, long lastTouchTimestamp) {
    this.length = length;
    this.lastTouchTimestamp = lastTouchTimestamp;
  }
}

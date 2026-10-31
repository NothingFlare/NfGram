/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream.cache;

/**
 * Evictor that doesn't ever evict cache files.
 *
 * <p>Warning: Using this evictor might have unforeseeable consequences if cache size is not managed
 * elsewhere.
 */
public final class NoOpCacheEvictor implements CacheEvictor {

  @Override
  public boolean requiresCacheSpanTouches() {
    return false;
  }

  @Override
  public void onCacheInitialized() {
    // Do nothing.
  }

  @Override
  public void onStartFile(Cache cache, String key, long position, long length) {
    // Do nothing.
  }

  @Override
  public void onSpanAdded(Cache cache, CacheSpan span) {
    // Do nothing.
  }

  @Override
  public void onSpanRemoved(Cache cache, CacheSpan span) {
    // Do nothing.
  }

  @Override
  public void onSpanTouched(Cache cache, CacheSpan oldSpan, CacheSpan newSpan) {
    // Do nothing.
  }
}

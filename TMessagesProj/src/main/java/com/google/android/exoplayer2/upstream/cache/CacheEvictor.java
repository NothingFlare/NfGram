/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream.cache;

import com.google.android.exoplayer2.C;

/**
 * Evicts data from a {@link Cache}. Implementations should call {@link Cache#removeSpan(CacheSpan)}
 * to evict cache entries based on their eviction policies.
 */
public interface CacheEvictor extends Cache.Listener {

  /**
   * Returns whether the evictor requires the {@link Cache} to touch {@link CacheSpan CacheSpans}
   * when it accesses them. Implementations that do not use {@link CacheSpan#lastTouchTimestamp}
   * should return {@code false}.
   */
  boolean requiresCacheSpanTouches();

  /** Called when cache has been initialized. */
  void onCacheInitialized();

  /**
   * Called when a writer starts writing to the cache.
   *
   * @param cache The source of the event.
   * @param key The key being written.
   * @param position The starting position of the data being written.
   * @param length The length of the data being written, or {@link C#LENGTH_UNSET} if unknown.
   */
  void onStartFile(Cache cache, String key, long position, long length);
}

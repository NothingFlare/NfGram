/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.drm;

import com.google.android.exoplayer2.MediaItem;

/**
 * A provider to obtain a {@link DrmSessionManager} suitable for playing the content described by a
 * {@link MediaItem}.
 */
public interface DrmSessionManagerProvider {

  /**
   * Returns a {@link DrmSessionManager} for the given media item.
   *
   * <p>The caller is responsible for {@link DrmSessionManager#prepare() preparing} the {@link
   * DrmSessionManager} before use, and subsequently {@link DrmSessionManager#release() releasing}
   * it.
   */
  DrmSessionManager get(MediaItem mediaItem);
}

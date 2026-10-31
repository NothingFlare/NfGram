/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.MediaItem;
import com.google.android.exoplayer2.drm.DrmSessionManagerProvider;
import com.google.android.exoplayer2.upstream.LoadErrorHandlingPolicy;

/**
 * @deprecated Use {@link MediaSource.Factory}.
 */
@Deprecated
public interface MediaSourceFactory extends MediaSource.Factory {

  /**
   * An instance that throws {@link UnsupportedOperationException} from {@link #createMediaSource}
   * and {@link #getSupportedTypes()}.
   */
  MediaSourceFactory UNSUPPORTED =
      new MediaSourceFactory() {
        @Override
        public MediaSourceFactory setDrmSessionManagerProvider(
            @Nullable DrmSessionManagerProvider drmSessionManagerProvider) {
          return this;
        }

        @Override
        public MediaSourceFactory setLoadErrorHandlingPolicy(
            @Nullable LoadErrorHandlingPolicy loadErrorHandlingPolicy) {
          return this;
        }

        @Override
        public @C.ContentType int[] getSupportedTypes() {
          throw new UnsupportedOperationException();
        }

        @Override
        public MediaSource createMediaSource(MediaItem mediaItem) {
          throw new UnsupportedOperationException();
        }
      };
}

/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.drm.DrmSession;

/** Holds a {@link Format}. */
public final class FormatHolder {

  /** An accompanying context for decrypting samples in the format. */
  @Nullable public DrmSession drmSession;

  /** The held {@link Format}. */
  @Nullable public Format format;

  /** Clears the holder. */
  public void clear() {
    drmSession = null;
    format = null;
  }
}

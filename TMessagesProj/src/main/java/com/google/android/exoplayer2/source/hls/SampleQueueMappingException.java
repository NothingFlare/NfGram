/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.source.SampleQueue;
import com.google.android.exoplayer2.source.TrackGroup;
import java.io.IOException;

/** Thrown when it is not possible to map a {@link TrackGroup} to a {@link SampleQueue}. */
public final class SampleQueueMappingException extends IOException {

  /**
   * @param mimeType The mime type of the track group whose mapping failed.
   */
  public SampleQueueMappingException(@Nullable String mimeType) {
    super("Unable to bind a sample queue to TrackGroup with mime type " + mimeType + ".");
  }
}

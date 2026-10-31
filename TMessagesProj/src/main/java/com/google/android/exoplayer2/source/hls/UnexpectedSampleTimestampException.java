/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.source.SampleQueue;
import com.google.android.exoplayer2.source.chunk.MediaChunk;
import com.google.android.exoplayer2.util.Util;
import java.io.IOException;

/**
 * Thrown when an attempt is made to write a sample to a {@link SampleQueue} whose timestamp is
 * inconsistent with the chunk from which it originates.
 */
/* package */ final class UnexpectedSampleTimestampException extends IOException {

  /** The {@link MediaChunk} that contained the rejected sample. */
  public final MediaChunk mediaChunk;

  /**
   * The timestamp of the last sample that was loaded from {@link #mediaChunk} and successfully
   * written to the {@link SampleQueue}, in microseconds. {@link C#TIME_UNSET} if the first sample
   * in the chunk was rejected.
   */
  public final long lastAcceptedSampleTimeUs;

  /** The timestamp of the rejected sample, in microseconds. */
  public final long rejectedSampleTimeUs;

  /**
   * Constructs an instance.
   *
   * @param mediaChunk The {@link MediaChunk} with the unexpected sample timestamp.
   * @param lastAcceptedSampleTimeUs The timestamp of the last sample that was loaded from the chunk
   *     and successfully written to the {@link SampleQueue}, in microseconds. {@link C#TIME_UNSET}
   *     if the first sample in the chunk was rejected.
   * @param rejectedSampleTimeUs The timestamp of the rejected sample, in microseconds.
   */
  public UnexpectedSampleTimestampException(
      MediaChunk mediaChunk, long lastAcceptedSampleTimeUs, long rejectedSampleTimeUs) {
    super(
        "Unexpected sample timestamp: "
            + Util.usToMs(rejectedSampleTimeUs)
            + " in chunk ["
            + mediaChunk.startTimeUs
            + ", "
            + mediaChunk.endTimeUs
            + "]");
    this.mediaChunk = mediaChunk;
    this.lastAcceptedSampleTimeUs = lastAcceptedSampleTimeUs;
    this.rejectedSampleTimeUs = rejectedSampleTimeUs;
  }
}

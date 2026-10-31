/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.chunk;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.extractor.DummyTrackOutput;
import com.google.android.exoplayer2.extractor.TrackOutput;
import com.google.android.exoplayer2.source.SampleQueue;
import com.google.android.exoplayer2.source.chunk.ChunkExtractor.TrackOutputProvider;
import com.google.android.exoplayer2.util.Log;

/**
 * A {@link TrackOutputProvider} that provides {@link TrackOutput TrackOutputs} based on a
 * predefined mapping from track type to output.
 */
public final class BaseMediaChunkOutput implements TrackOutputProvider {

  private static final String TAG = "BaseMediaChunkOutput";

  private final @C.TrackType int[] trackTypes;
  private final SampleQueue[] sampleQueues;

  /**
   * @param trackTypes The track types of the individual track outputs.
   * @param sampleQueues The individual sample queues.
   */
  public BaseMediaChunkOutput(int[] trackTypes, SampleQueue[] sampleQueues) {
    this.trackTypes = trackTypes;
    this.sampleQueues = sampleQueues;
  }

  @Override
  public TrackOutput track(int id, @C.TrackType int type) {
    for (int i = 0; i < trackTypes.length; i++) {
      if (type == trackTypes[i]) {
        return sampleQueues[i];
      }
    }
    Log.e(TAG, "Unmatched track of type: " + type);
    return new DummyTrackOutput();
  }

  /** Returns the current absolute write indices of the individual sample queues. */
  public int[] getWriteIndices() {
    int[] writeIndices = new int[sampleQueues.length];
    for (int i = 0; i < sampleQueues.length; i++) {
      writeIndices[i] = sampleQueues[i].getWriteIndex();
    }
    return writeIndices;
  }

  /**
   * Sets an offset that will be added to the timestamps (and sub-sample timestamps) of samples
   * subsequently written to the sample queues.
   */
  public void setSampleOffsetUs(long sampleOffsetUs) {
    for (SampleQueue sampleQueue : sampleQueues) {
      sampleQueue.setSampleOffsetUs(sampleOffsetUs);
    }
  }
}

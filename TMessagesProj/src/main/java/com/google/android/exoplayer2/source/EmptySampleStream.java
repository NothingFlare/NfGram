/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.FormatHolder;
import com.google.android.exoplayer2.decoder.DecoderInputBuffer;

/** An empty {@link SampleStream}. */
public final class EmptySampleStream implements SampleStream {

  @Override
  public boolean isReady() {
    return true;
  }

  @Override
  public void maybeThrowError() {
    // Do nothing.
  }

  @Override
  public int readData(
      FormatHolder formatHolder, DecoderInputBuffer buffer, @ReadFlags int readFlags) {
    buffer.setFlags(C.BUFFER_FLAG_END_OF_STREAM);
    return C.RESULT_BUFFER_READ;
  }

  @Override
  public int skipData(long positionUs) {
    return 0;
  }
}

/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream;

import static com.google.android.exoplayer2.util.Util.castNonNull;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.util.Assertions;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import org.checkerframework.checker.nullness.qual.MonotonicNonNull;

/** A {@link DataSink} for writing to a byte array. */
public final class ByteArrayDataSink implements DataSink {

  private @MonotonicNonNull ByteArrayOutputStream stream;

  @Override
  public void open(DataSpec dataSpec) {
    if (dataSpec.length == C.LENGTH_UNSET) {
      stream = new ByteArrayOutputStream();
    } else {
      Assertions.checkArgument(dataSpec.length <= Integer.MAX_VALUE);
      stream = new ByteArrayOutputStream((int) dataSpec.length);
    }
  }

  @Override
  public void close() throws IOException {
    castNonNull(stream).close();
  }

  @Override
  public void write(byte[] buffer, int offset, int length) {
    castNonNull(stream).write(buffer, offset, length);
  }

  /**
   * Returns the data written to the sink since the last call to {@link #open(DataSpec)}, or null if
   * {@link #open(DataSpec)} has never been called.
   */
  @Nullable
  public byte[] getData() {
    return stream == null ? null : stream.toByteArray();
  }
}

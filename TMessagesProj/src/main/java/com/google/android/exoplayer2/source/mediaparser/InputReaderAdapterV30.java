/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.mediaparser;

import android.annotation.SuppressLint;
import android.media.MediaParser;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.upstream.DataReader;
import com.google.android.exoplayer2.util.Util;
import java.io.IOException;

/** {@link MediaParser.SeekableInputReader} implementation wrapping a {@link DataReader}. */
@RequiresApi(30)
@SuppressLint("Override") // TODO: Remove once the SDK becomes stable.
public final class InputReaderAdapterV30 implements MediaParser.SeekableInputReader {

  @Nullable private DataReader dataReader;
  private long resourceLength;
  private long currentPosition;
  private long lastSeekPosition;

  /**
   * Sets the wrapped {@link DataReader}.
   *
   * @param dataReader The {@link DataReader} to wrap.
   * @param length The length of the resource from which {@code dataReader} reads.
   */
  public void setDataReader(DataReader dataReader, long length) {
    this.dataReader = dataReader;
    resourceLength = length;
    lastSeekPosition = C.POSITION_UNSET;
  }

  /** Sets the absolute position in the resource from which the wrapped {@link DataReader} reads. */
  public void setCurrentPosition(long position) {
    currentPosition = position;
  }

  /**
   * Returns the last value passed to {@link #seekToPosition(long)} and sets the stored value to
   * {@link C#POSITION_UNSET}.
   */
  public long getAndResetSeekPosition() {
    long lastSeekPosition = this.lastSeekPosition;
    this.lastSeekPosition = C.POSITION_UNSET;
    return lastSeekPosition;
  }

  // SeekableInputReader implementation.

  @Override
  public void seekToPosition(long position) {
    lastSeekPosition = position;
  }

  @Override
  public int read(byte[] bytes, int offset, int readLength) throws IOException {
    int bytesRead = Util.castNonNull(dataReader).read(bytes, offset, readLength);
    currentPosition += bytesRead;
    return bytesRead;
  }

  @Override
  public long getPosition() {
    return currentPosition;
  }

  @Override
  public long getLength() {
    return resourceLength;
  }
}

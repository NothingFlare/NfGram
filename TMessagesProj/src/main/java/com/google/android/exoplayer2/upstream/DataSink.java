/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream;

import java.io.IOException;

/** A component to which streams of data can be written. */
public interface DataSink {

  /** A factory for {@link DataSink} instances. */
  interface Factory {

    /** Creates a {@link DataSink} instance. */
    DataSink createDataSink();
  }

  /**
   * Opens the sink to consume the specified data.
   *
   * <p>Note: If an {@link IOException} is thrown, callers must still call {@link #close()} to
   * ensure that any partial effects of the invocation are cleaned up.
   *
   * @param dataSpec Defines the data to be consumed.
   * @throws IOException If an error occurs opening the sink.
   */
  void open(DataSpec dataSpec) throws IOException;

  /**
   * Consumes the provided data.
   *
   * @param buffer The buffer from which data should be consumed.
   * @param offset The offset of the data to consume in {@code buffer}.
   * @param length The length of the data to consume, in bytes.
   * @throws IOException If an error occurs writing to the sink.
   */
  void write(byte[] buffer, int offset, int length) throws IOException;

  /**
   * Closes the sink.
   *
   * <p>Note: This method must be called even if the corresponding call to {@link #open(DataSpec)}
   * threw an {@link IOException}. See {@link #open(DataSpec)} for more details.
   *
   * @throws IOException If an error occurs closing the sink.
   */
  void close() throws IOException;
}

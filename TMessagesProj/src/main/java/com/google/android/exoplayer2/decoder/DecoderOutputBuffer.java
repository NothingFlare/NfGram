/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.decoder;

/** Output buffer decoded by a {@link Decoder}. */
public abstract class DecoderOutputBuffer extends Buffer {

  /** Buffer owner. */
  public interface Owner<S extends DecoderOutputBuffer> {

    /**
     * Releases the buffer.
     *
     * @param outputBuffer Output buffer.
     */
    void releaseOutputBuffer(S outputBuffer);
  }

  /** The presentation timestamp for the buffer, in microseconds. */
  public long timeUs;

  /**
   * The number of buffers immediately prior to this one that were skipped in the {@link Decoder}.
   */
  public int skippedOutputBufferCount;

  /** Releases the output buffer for reuse. Must be called when the buffer is no longer needed. */
  public abstract void release();
}

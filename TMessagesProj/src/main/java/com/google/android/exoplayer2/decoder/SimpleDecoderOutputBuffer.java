/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.decoder;

import androidx.annotation.Nullable;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/** Buffer for {@link SimpleDecoder} output. */
public class SimpleDecoderOutputBuffer extends DecoderOutputBuffer {

  private final Owner<SimpleDecoderOutputBuffer> owner;

  @Nullable public ByteBuffer data;

  public SimpleDecoderOutputBuffer(Owner<SimpleDecoderOutputBuffer> owner) {
    this.owner = owner;
  }

  /**
   * Initializes the buffer.
   *
   * @param timeUs The presentation timestamp for the buffer, in microseconds.
   * @param size An upper bound on the size of the data that will be written to the buffer.
   * @return The {@link #data} buffer, for convenience.
   */
  public ByteBuffer init(long timeUs, int size) {
    this.timeUs = timeUs;
    if (data == null || data.capacity() < size) {
      data = ByteBuffer.allocateDirect(size).order(ByteOrder.nativeOrder());
    }
    data.position(0);
    data.limit(size);
    return data;
  }

  @Override
  public void clear() {
    super.clear();
    if (data != null) {
      data.clear();
    }
  }

  @Override
  public void release() {
    owner.releaseOutputBuffer(this);
  }
}

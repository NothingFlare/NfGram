/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.util.Assertions;
import java.nio.ByteBuffer;

/**
 * A {@link MetadataDecoder} base class that validates input buffers and discards any for which
 * {@link MetadataInputBuffer#isDecodeOnly()} is {@code true}.
 */
public abstract class SimpleMetadataDecoder implements MetadataDecoder {

  @Override
  @Nullable
  public final Metadata decode(MetadataInputBuffer inputBuffer) {
    ByteBuffer buffer = Assertions.checkNotNull(inputBuffer.data);
    Assertions.checkArgument(
        buffer.position() == 0 && buffer.hasArray() && buffer.arrayOffset() == 0);
    return inputBuffer.isDecodeOnly() ? null : decode(inputBuffer, buffer);
  }

  /**
   * Called by {@link #decode(MetadataInputBuffer)} after input buffer validation has been
   * performed, except in the case that {@link MetadataInputBuffer#isDecodeOnly()} is {@code true}.
   *
   * @param inputBuffer The input buffer to decode.
   * @param buffer The input buffer's {@link MetadataInputBuffer#data data buffer}, for convenience.
   *     Validation by {@link #decode} guarantees that {@link ByteBuffer#hasArray()}, {@link
   *     ByteBuffer#position()} and {@link ByteBuffer#arrayOffset()} are {@code true}, {@code 0} and
   *     {@code 0} respectively.
   * @return The decoded metadata object, or {@code null} if the metadata could not be decoded.
   */
  @Nullable
  protected abstract Metadata decode(MetadataInputBuffer inputBuffer, ByteBuffer buffer);
}

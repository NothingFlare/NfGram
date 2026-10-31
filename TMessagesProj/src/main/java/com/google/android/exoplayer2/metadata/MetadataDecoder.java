/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata;

import androidx.annotation.Nullable;
import java.nio.ByteBuffer;

/** Decodes metadata from binary data. */
public interface MetadataDecoder {

  /**
   * Decodes a {@link Metadata} element from the provided input buffer.
   *
   * <p>Respects {@link ByteBuffer#limit()} of {@code inputBuffer.data}, but assumes {@link
   * ByteBuffer#position()} and {@link ByteBuffer#arrayOffset()} are both zero and {@link
   * ByteBuffer#hasArray()} is true.
   *
   * @param inputBuffer The input buffer to decode.
   * @return The decoded metadata object, or {@code null} if the metadata could not be decoded or if
   *     {@link MetadataInputBuffer#isDecodeOnly()} was set on the input buffer.
   */
  @Nullable
  Metadata decode(MetadataInputBuffer inputBuffer);
}

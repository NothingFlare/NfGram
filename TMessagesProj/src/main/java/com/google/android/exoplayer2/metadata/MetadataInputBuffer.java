/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata;

import com.google.android.exoplayer2.Format;
import com.google.android.exoplayer2.decoder.DecoderInputBuffer;

/** A {@link DecoderInputBuffer} for a {@link MetadataDecoder}. */
public final class MetadataInputBuffer extends DecoderInputBuffer {

  /**
   * An offset that must be added to the metadata's timestamps after it's been decoded, or {@link
   * Format#OFFSET_SAMPLE_RELATIVE} if {@link #timeUs} should be added.
   */
  public long subsampleOffsetUs;

  public MetadataInputBuffer() {
    super(DecoderInputBuffer.BUFFER_REPLACEMENT_MODE_NORMAL);
  }
}

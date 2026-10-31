/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor.avi;

import com.google.android.exoplayer2.util.ParsableByteArray;

/** Parses and contains the name from the STRN chunk. */
/* package */ final class StreamNameChunk implements AviChunk {

  public static StreamNameChunk parseFrom(ParsableByteArray body) {
    return new StreamNameChunk(body.readString(body.bytesLeft()));
  }

  public final String name;

  private StreamNameChunk(String name) {
    this.name = name;
  }

  @Override
  public int getType() {
    return AviExtractor.FOURCC_strn;
  }
}

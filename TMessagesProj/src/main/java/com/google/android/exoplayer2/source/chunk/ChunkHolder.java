/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.chunk;

import androidx.annotation.Nullable;

/** Holds a chunk or an indication that the end of the stream has been reached. */
public final class ChunkHolder {

  /** The chunk. */
  @Nullable public Chunk chunk;

  /** Indicates that the end of the stream has been reached. */
  public boolean endOfStream;

  /** Clears the holder. */
  public void clear() {
    chunk = null;
    endOfStream = false;
  }
}

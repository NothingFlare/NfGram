/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata.id3;

import com.google.android.exoplayer2.metadata.Metadata;

/** Base class for ID3 frames. */
public abstract class Id3Frame implements Metadata.Entry {

  /** The frame ID. */
  public final String id;

  public Id3Frame(String id) {
    this.id = id;
  }

  @Override
  public String toString() {
    return id;
  }

  @Override
  public int describeContents() {
    return 0;
  }
}

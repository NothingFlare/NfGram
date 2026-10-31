/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata;


/** Receives metadata output. */
public interface MetadataOutput {

  /**
   * Called when there is metadata associated with current playback time.
   *
   * @param metadata The metadata.
   */
  void onMetadata(Metadata metadata);
}

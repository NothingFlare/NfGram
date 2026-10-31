/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

import java.io.IOException;

/** Thrown when a live playback falls behind the available media window. */
public final class BehindLiveWindowException extends IOException {

  public BehindLiveWindowException() {
    super();
  }
}

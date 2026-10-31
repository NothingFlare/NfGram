/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.offline;

import java.io.IOException;

/** Thrown on an error during downloading. */
public final class DownloadException extends IOException {

  /**
   * @param message The message for the exception.
   */
  public DownloadException(String message) {
    super(message);
  }

  /**
   * @param cause The cause for the exception.
   */
  public DownloadException(Throwable cause) {
    super(cause);
  }
}

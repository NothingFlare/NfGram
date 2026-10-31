/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

import android.net.Uri;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.ParserException;

/** Thrown if the input format was not recognized. */
public class UnrecognizedInputFormatException extends ParserException {

  /** The {@link Uri} from which the unrecognized data was read. */
  public final Uri uri;

  /**
   * @param message The detail message for the exception.
   * @param uri The {@link Uri} from which the unrecognized data was read.
   */
  public UnrecognizedInputFormatException(String message, Uri uri) {
    super(message, /* cause= */ null, /* contentIsMalformed= */ false, C.DATA_TYPE_MEDIA);
    this.uri = uri;
  }
}

/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.database;

import android.database.SQLException;
import java.io.IOException;

/** An {@link IOException} whose cause is an {@link SQLException}. */
public final class DatabaseIOException extends IOException {

  public DatabaseIOException(SQLException cause) {
    super(cause);
  }

  public DatabaseIOException(SQLException cause, String message) {
    super(message, cause);
  }
}

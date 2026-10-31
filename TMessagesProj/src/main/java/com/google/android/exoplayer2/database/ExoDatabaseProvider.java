/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.database;

import android.content.Context;

/**
 * @deprecated Use {@link StandaloneDatabaseProvider}.
 */
@Deprecated
public final class ExoDatabaseProvider extends StandaloneDatabaseProvider {

  public ExoDatabaseProvider(Context context) {
    super(context);
  }
}

/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.database;

import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

/** A {@link DatabaseProvider} that provides instances obtained from a {@link SQLiteOpenHelper}. */
public final class DefaultDatabaseProvider implements DatabaseProvider {

  private final SQLiteOpenHelper sqliteOpenHelper;

  /**
   * @param sqliteOpenHelper An {@link SQLiteOpenHelper} from which to obtain database instances.
   */
  public DefaultDatabaseProvider(SQLiteOpenHelper sqliteOpenHelper) {
    this.sqliteOpenHelper = sqliteOpenHelper;
  }

  @Override
  public SQLiteDatabase getWritableDatabase() {
    return sqliteOpenHelper.getWritableDatabase();
  }

  @Override
  public SQLiteDatabase getReadableDatabase() {
    return sqliteOpenHelper.getReadableDatabase();
  }
}
